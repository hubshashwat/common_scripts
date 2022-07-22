#To be added

GITLAB_USERNAME = 'ADD YOU USERNAME'
GITHUB_USERNAME = 'ADD YOU USERNAME'
GITLAB_TOKEN = 'TOKEN'
GITHUB_TOKEN = 'TOKEN'

#necessary imports
import gitlab
import requests
import json


# get all projects from a user
x = requests.get( \
    url='https://gitlab.com/api/v4/users/{user}/projects'.format(user=GITLAB_USERNAME), \
    headers={'PRIVATE-TOKEN': GITLAB_TOKEN})

#create a set of projects with its unique gitlab paths
set_of_projects = set()

# for each project in gitlab create a repo in github
for repo in json.loads(x.content):
    try:
        print('Name:', repo['name'])
        set_of_projects.add(repo['path_with_namespace'])
        y = requests.post( \
            url='https://api.github.com/user/repos', \
            headers={'Accept': 'application/vnd.github+json',
                     'Authorization': 'token {token}'.format(token=GITHUB_TOKEN)}, \
            json={'name': repo['name'], 'description': repo['description'], 'private': repo['visibility'] == 'private'})
        print(y)
        print(y.text)
    except Exception as exc:
        print(exc)

# To get the projects from each group and subgroup
gl = gitlab.Gitlab('https://gitlab.com', private_token=GITLAB_TOKEN)

for group in gl.groups.list():
    try:
        print("Group attribute name we are accessing is:", group.attributes['name'])
        group = gl.groups.get(group.attributes['id'], lazy=True)
        projects = group.projects.list(include_subgroups=True, all=True)    #get projects from group and subgroup
        for project in projects:
            if project.path_with_namespace not in set_of_projects:
                y = requests.post( \
                    url='https://api.github.com/user/repos', \
                    headers={'Accept': 'application/vnd.github+json',
                             'Authorization': 'token {token}'.format(token=GITHUB_TOKEN)}, \
                    json={'name': project.name, 'description': project.description,
                          'private': project.visibility == 'private'})
                print(y)
                print(y.text)
                set_of_projects.add(project.path_with_namespace)
    except Exception as exc:
        print(exc)

print(set_of_projects)
print(len(set_of_projects))

with open("migration.txt","w") as file:
    file.write(str(set_of_projects))
