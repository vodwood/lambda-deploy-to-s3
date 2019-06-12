BEFORE S3 DEPLOYMENT ACTIONS IN CODE PIPELINE WERE A THING

# lambda deploy to s3

Lambda function to deploy a static website from CodeBuild artifact to s3.

0. Create an S3 bucket for hosting and an S3 bucket for build artifacts;
1. Create a CodeBuild project:
	- Choose project name, source and environment;
	- In Artifacts, select type = s3, name = replaceBuildArchive.zip, bucket name = replaceBuildBucketS3Name, artifact packaging - zip;
	- Create a new role from templates, name the role and proceed.

2. Create a Lambda function:
	- Runtime: Python 2.7;
	- Default service role;
	- Time out of 30 seconds at least.
3. Edit the above Lambda service role in IAM to include:
	- Publish to SNS topic policy (if needed);
	- S3 policy to get items from the build bucket;
	- S3 policty to put items in the hosting bucket.
4. Create a CodePipeline project with the following steps:
	- Source - github or codecommit;
	- Build - CodeBuild project created in step 1;
	- Deploy - choose no deploy.
5. Manually add a stage in CodePipeline:
	- Action category: invoke;
	- Provide: AWS Lambda;
	- Function name - choose the created function;
	- Input artifact - MyAppBuild (or other build artifact name).
	
