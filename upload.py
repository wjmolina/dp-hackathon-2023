import glob
import os
import shutil

import boto3

bucket_name = "dp-hackathon-2023"

os.makedirs("pkg/simple", exist_ok=True)

for raw_file_name in glob.glob(os.path.join("dist", "*.tar.gz")):
    file_name = os.path.basename(raw_file_name)
    packaged_file_name = os.path.join("pkg/simple", file_name.split("-")[0])
    os.makedirs(packaged_file_name, exist_ok=True)
    shutil.copy(raw_file_name, os.path.join(packaged_file_name, file_name))

local_directory = "pkg"
s3 = boto3.client("s3")

for root, _, files in os.walk(local_directory):
    for file_name in files:
        if file_name.endswith(".tar.gz"):
            local_file = os.path.join(root, file_name)
            s3_path = os.path.relpath(local_file, local_directory).replace(os.path.sep, "/")

            with open(local_file, "rb") as file_data:
                s3.put_object(
                    Bucket=bucket_name,
                    Key=s3_path,
                    Body=file_data,
                    ContentType="application/gzip",
                    ACL="public-read",
                )
