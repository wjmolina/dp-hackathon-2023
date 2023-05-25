from collections import defaultdict

import boto3

bucket_name = "dp-hackathon-2023"

s3 = boto3.client("s3")
paginator = s3.get_paginator("list_objects_v2")
packages = defaultdict(set)

for page in paginator.paginate(Bucket=bucket_name):
    for obj in page.get("Contents", []):
        if obj["Key"].endswith(".tar.gz"):
            packages[obj["Key"].split("/")[1]].add(obj["Key"].split("/")[-1])

s3.put_object(
    Bucket=bucket_name,
    Key="simple/index.html",
    Body="\n".join(f'<a href="{package}"></a>' for package in packages),
    ContentType="text/html",
    ACL="public-read",
)

for package, versions in packages.items():
    s3.put_object(
        Bucket=bucket_name,
        Key=f"simple/{package}/index.html",
        Body="\n".join(f'<a href="{version}"></a>' for version in versions),
        ContentType="text/html",
        ACL="public-read",
    )
