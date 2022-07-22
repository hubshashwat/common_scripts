GITHUB_USERNAME = 'USERNAME'

import os

with open("migration.txt","r") as file:
    set_of_paths = file.read()

set_of_paths = eval(set_of_paths)

for paths in set_of_paths:
    try:
        print("Starting to push -------------->",paths," from gitlab to local")
        os.system(f'git clone --bare https://gitlab.com/{paths}.git')
        cd = f'{paths.split("/")[-1]}.git'
        os.chdir(cd)
        print("Starting to push -------------->", paths, " from local to github")
        os.system(f'git push --mirror https://github.com/{GITHUB_USERNAME}/{paths.split("/")[-1]}.git')
        os.chdir('..')
    except Exception as exc:
        print(exc)
