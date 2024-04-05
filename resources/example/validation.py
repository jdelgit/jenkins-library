from sys import argv
from os.path import exists

PROJECT_BUCKET = "terraform-bucket"
AWS_REGION = "eu-central-1"

def parse_conf(conf_path):
    with open(conf_path) as fh:
        data = fh.read()
        lines = data.splitlines()

    conf_data = {}
    for line in lines:
        line = line.replace(" ", "").replace('"', "")
        line = line.split("=")
        conf_data[line[0]] = line[1]

    return conf_data


def validate_conf(deployment_env):
    conf_file_path = f"{deployment_env}/backend.conf"
    data = parse_conf(conf_file_path)
    # Check bucket name
    if "bucket" in data:
        if data["bucket"]:
            if data["bucket"] != PROJECT_BUCKET:
                return False
        else:
            print(f"Bucket should be {PROJECT_BUCKET}")
            return False
    else:
        # Missing bucket definition
        print(f"Bucket should be {PROJECT_BUCKET}")
        return False
    # Check key, must be in a team directory
    if "key" in data:
        if data["key"]:
            key_data = data["key"].split("/")
            if len(key_data) != 2:
                print("Invalid key. Must be a .tfstate file inside your team's folder")
                return False
        else:
            print("key not defined")
            return False
    else:
        print("key not defined")
        return False
    # check region
    if "region" in data:
        if data["region"] != AWS_REGION:
            print(f"Region should be {AWS_REGION}")
            return False
    else:
        print(f"Region should be {AWS_REGION}")
        return False
    return True

if __name__ == "__main__":
    deployment_env = argv[1]
    deployment_repo = argv[2]

    print(f"{deployment_repo}")
    conf_file_path = f"{deployment_env}/backend.conf"
    if exists(conf_file_path):
        # continue validation
        valid = validate_conf(deployment_env)
        if not valid:
            print("Invalid conf file")
            exit(1)
        else:
            print("Conf file valid")
            exit(0)
    else:
        print(f"File {conf_file_path} not found.\n Please verify environment and filename")
        exit(1)
