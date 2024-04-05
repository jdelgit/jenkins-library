from sys import argv
from os.path import exists

PROJECT_BUCKET = "terraform-bucket"
AWS_REGION = "eu-central-1"
DEPLOYABLE_ENVIRONMENTS = ["Dev","Test","Prod"]

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

def parse_team_name(repo_url):
    if repo_url:
        tokens = repo_url.split("/")
        # check team name


def validate_conf(environment):
    conf_file_path = f"{environment}/backend.conf"
    conf_data = parse_conf(conf_file_path)
    # Check bucket name
    if conf_data.get('bucket'):
        if conf_data["bucket"] != PROJECT_BUCKET:
            return False
    else:
        print(f"Bucket should be {PROJECT_BUCKET}")
        return False
    # Check key, must be in a team directory
    if conf_data.get('key'):
        key_data = conf_data["key"].split("/")
        if len(key_data) != 2:
            print("Invalid key. Must be a .tfstate file inside your team's folder")
            return False
        else:
            # Check repo being used, name must be same as bucket folder
            team_name = parse_team_name(repo_url)
            if team_name:
                # do check
                if key_data[0] != team_name:
                    return False
            else:
                return False
    else:
        print("key not defined")
        return False
    # check region
    if conf_data.get('region'):
        if conf_data["region"] != AWS_REGION:
            print(f"Region should be {AWS_REGION}")
            return False
    else:
        print(f"Region should be {AWS_REGION}")
        return False
    return True


if __name__ == "__main__":
    environment = argv[1]
    repo_url = argv[2]

    conf_file_path = f"{environment}/backend.conf"
    if exists(conf_file_path):
        # continue validation
        valid = validate_conf(environment, repo_url)
        if not valid:
            print("Invalid conf file")
            exit(1)
        else:
            print("Conf file valid")
            exit(0)
    else:
        print(f"File {conf_file_path} not found.\n Please verify environment and filename")
        exit(1)
