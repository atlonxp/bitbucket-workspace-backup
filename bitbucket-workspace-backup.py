import json
import os
from json import JSONDecodeError
from pathlib import Path

user = "your-username"      # not an email
password = "your-password"
workspace = "workspace-slug-name"

crawling_command = f'curl -u {user}:{password} "https://api.bitbucket.org/2.0/repositories/{workspace}"'

base_folder = "destination-path-for-all-clone-repositories"

try:
    next = crawling_command
    while len(next) > 0 and next is not None:
        print('\n', next)
        res = json.loads(os.popen(next).read())

        values = res['values']
        for value in values:
            project = value.get('project', None)
            print(f'\t> {project["name"]} - {value["full_name"]}')

            clone_dir = base_folder + f'projects/{project["name"]}/{value["name"]}/' if project \
                else f'repositories/{value["name"]}'
            Path(clone_dir).mkdir(parents=True, exist_ok=True)

            links = value.get('links')
            git_command = f'git clone {links["clone"][0]["href"].replace(user, f"{user}:{password}")} "{clone_dir}"'
            os.popen(git_command).read()
        next = res.get('next', None)
        if next:
            next = f'curl -u {user}:{password} "{next}"'
        else:
            break
except JSONDecodeError as e:
    print(e.args)

print('done')
