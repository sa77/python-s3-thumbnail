S3 Thumbnail generator service
===

- AWS resources - lambda, S3, IAM
- docker (to containerize python libraries)
- serverless framework


## steps

1. install docker (https://hub.docker.com/search/?type=edition&offering=community)

2. install plugins

    `npm install serverless-python-requirements`

3. update serverless.yml with your own provider.profile, provider.region and custom.bucket values

4. deploy

    `serverless deploy -v`

    deploy update code changes on handler.py

    `sls deploy function -f s3-thumbnail-generator`

5. go to your S3 dash and upload a png file inside the bucket configured in (3)



