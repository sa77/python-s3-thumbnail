import boto3
import cStringIO
from PIL import Image, ImageOps
import os

s3 = boto3.client('s3')
size = int(os.environ['THUMBNAIL_SIZE'])


def s3_thumbnail_generator(event, context):
    # parse event
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    if (not key.endswith("_thumbnail.png")):
        # get image
        image = get_s3_image(bucket, key)
        # resize the image
        thumbnail = image_to_thumbnail(image)
        # get the new filename
        thumbnail_key = new_filename(key)
        # upload the file
        url = upload_to_s3(bucket, thumbnail_key, thumbnail)
        return url


def get_s3_image(bucket, key):
    response = s3.get_object(Bucket=bucket, Key=key)
    imagecontent = response['Body'].read()

    file = cStringIO.StringIO(imagecontent)
    img = Image.open(file)
    return img


def image_to_thumbnail(image):
    return ImageOps.fit(image, (size, size), Image.ANTIALIAS)


def new_filename(key):
    key_split = key.rsplit('.', 1)[0]
    return key_split + "_thumbnail.png"


def upload_to_s3(bucket, key, image):
    # saving the image into a cStringIO object to avoid writing to disk
    out_thumbnail = cStringIO.StringIO()
    # file type must be specified
    image.save(out_thumbnail, 'PNG')
    out_thumbnail.seek(0)

    response = s3.put_object(
        ACL='public-read',
        Body=out_thumbnail,
        Bucket=bucket,
        ContentType='image/png',
        Key=key
    )
    print(response)

    url = '{}/{}/{}'.format(s3.meta.endpoint_url, bucket, key)
    return url
