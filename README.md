# lambdadeploytos3
Lambda function to deploy a static website to s3 from git.

1. Create a CodeBuild project:
	- Choose project name, source and environment specific to your needs;
	- In Artifacts, select type = s3, name = replaceBuildArchive.zip, bucket name = replaceBuildBucketS3Name, artifact packaging - zip 

