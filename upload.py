import glob
import os
import re
import shutil

import boto3

bucket = "dp-hackathon-2023"

os.makedirs("pkg/simple", exist_ok=True)

for raw_file_name in glob.glob(os.path.join("dist", "*.tar.gz")):
    file_name = os.path.basename(raw_file_name)
    match = re.match(r"^(.+)-\d+\.\d+\.\d+\.tar\.gz$", file_name)

    if not match:
        continue

    packaged_file_name = os.path.join("pkg/simple", match.group(1))
    os.makedirs(packaged_file_name, exist_ok=True)
    shutil.copy(raw_file_name, os.path.join(packaged_file_name, file_name))

local_directory = "pkg"
s3 = boto3.client("s3")

for root, _, files in os.walk(local_directory):
    for file_name in files:
        if file_name.endswith(".tar.gz"):
            local_file = os.path.join(root, file_name)
            key = os.path.relpath(local_file, local_directory).replace(os.path.sep, "/")
            key = key.split("/")
            key[-1] = key[-1].replace("-", "_")
            key = "/".join(key)

            with open(local_file, "rb") as body:
                s3.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=body,
                    ContentType="application/gzip",
                    ACL="public-read",
                )
