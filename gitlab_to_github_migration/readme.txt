Step1:

0) Clone this repo. cd to common_scripts/gitlab_to_github_migration.

1) Create all repos (empty) and (private) from gitlab to github.

To do so:
* Generate personal access tokens for gitlab (https://gitlab.com/-/profile/personal_access_tokens) and github (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) and add them to the script transfer.py [this creates your direct projects, projects in groups and subgroups

Post this step, all repos should be created. This script will generate a text file with all the http url links of the gitlab account you have to migrate.

2) Run scripts.py and wait.
