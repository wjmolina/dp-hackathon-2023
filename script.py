import glob
import os
import shutil

os.makedirs("package/simple", exist_ok=True)
packages = set()

for raw_file_name in glob.glob(os.path.join("dist", "*.tar.gz")):
    file_name = os.path.basename(raw_file_name)
    split_file_name = file_name.split("-")[0]
    packaged_file_name = os.path.join("package/simple", split_file_name)

    os.makedirs(packaged_file_name, exist_ok=True)
    shutil.copy(raw_file_name, os.path.join(packaged_file_name, file_name))

    with open(os.path.join(packaged_file_name, "index.html"), "a") as stream:
        stream.write(f'<a href="{file_name}"></a>\n')

    packages.add(split_file_name)

with open("package/simple/index.html", "w") as stream:
    for package in packages:
        stream.write(f'<a href="{package}"></a>\n')
