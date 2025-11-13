"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3
from pulumi_aws import amplify
import cloudflarepages
from uptime import build_statuscake_check

# Create an AWS resource (S3 Bucket)
bucket = s3.BucketV2("my-bucket")

# Export the name of the bucket
pulumi.export("bucket_name", bucket.id)

# Amplify App - build config
with open("amplify.yml", "r") as file:
    amplify_yml = file.read()

# Amplify App
conf = pulumi.Config()
github_tok = conf.require_secret("github_token2")
amplify_app = amplify.App(
    "CrumAndPoppedHorn",
    name="rumandpopcorn",
    repository="https://github.com/brokensbone/rumandpopcorn",
    build_spec=amplify_yml,
    access_token=github_tok,
)

main = amplify.Branch(
    "main",
    app_id=amplify_app.id,
    branch_name="hugo",
    stage="PRODUCTION",
    enable_auto_build=True,
)
branch_prod = amplify.Branch(
    "production",
    app_id=amplify_app.id,
    branch_name="main",
    stage="PRODUCTION",
    enable_auto_build=True,
)

domain_association_resource = amplify.DomainAssociation(
    "alcachofa-uk",
    app_id=amplify_app.id,
    domain_name="alcachofa.uk",
    sub_domains=[
        {
            "branch_name": main.branch_name,
            "prefix": "",
        },
        {
            "branch_name": main.branch_name,
            "prefix": "www",
        },
    ],
    enable_auto_sub_domain=False,
    wait_for_verification=False,
)

domain_association_rnp = amplify.DomainAssociation(
    "rumandpopcorn",
    app_id=amplify_app.id,
    domain_name="rumandpopcorn.com",
    sub_domains=[
        {
            "branch_name": branch_prod.branch_name,
            "prefix": "",
        },
        {
            "branch_name": branch_prod.branch_name,
            "prefix": "www",
        },
        {
            "branch_name": branch_prod.branch_name,
            "prefix": "prod",
        },
    ],
    enable_auto_sub_domain=False,
    wait_for_verification=False,
)

build_statuscake_check()
cloudflarepages.build()

pulumi.export("Domain", amplify_app.default_domain)
pulumi.export("DNSRecords", domain_association_rnp.certificate_verification_dns_record)
