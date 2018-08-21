import boto3
import StringIO
import zipfile
import mimetypes
from botocore.client import Config
def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('ReplaceARN')

    location = {
        "bucketName": "replaceBuildBucketS3Name",
        "objectKey": "replaceBuildArchive.zip"
    }

    try:
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]
        print "Building from " + str(location)
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

        build_bucket = s3.Bucket(location["bucketName"])
        web_bucket = s3.Bucket('replaceHostingBucketS3Name')

        web_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], web_zip)

        with zipfile.ZipFile(web_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                web_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                web_bucket.Object(nm).Acl().put(ACL='public-read')
        print 'Job Done'
        topic.publish(Subject="Deploy Success", Message="Website deployed succesfully.")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Deploy Fail", Message="Website failed to deploy.")
        raise
