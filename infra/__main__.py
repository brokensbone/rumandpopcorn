"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3
from pulumi_aws import amplify

# Create an AWS resource (S3 Bucket)
bucket = s3.BucketV2('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

# Amplify App - build config
with open("amplify.yml", "r") as file:
    amplify_yml = file.read()

# Amplify App
conf = pulumi.Config()
github_tok = conf.require_secret("github_token2")
amplify_app = amplify.App('CrumAndPoppedHorn',
    name='crumandpoppedhorn',
    repository='https://github.com/brokensbone/rumandpopcorn',
    build_spec=amplify_yml,
    access_token=github_tok

)

main = amplify.Branch("main",
    app_id=amplify_app.id,
    branch_name="hugo",
    stage="PRODUCTION",
    enable_auto_build=True
)

pulumi.export('Domain', amplify_app.default_domain)