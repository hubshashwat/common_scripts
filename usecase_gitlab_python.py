"""
Create a branch, push the code to that branch and create a merge request.
"""
import gitlab

GLOBAL_BRANCH = "main"
AUTHOR_EMAIL = "forwardtoshashwat@gmail.com"
AUTHOR_NAME = "Shashwat Kumar"


class PythonGitlab:
    """
    Gilab Python Class to perform basic functionality
    """

    def __init__(self, url, authkey, project):
        self.url = url
        self.authkey = authkey
        self.project_name = project

        # Creation of python-gitlab server
        server = gitlab.Gitlab(self.url, authkey, api_version=4, ssl_verify=False)

        # Get the exact project name instance
        self.project = None
        self.project = server.projects.get(self.project_name)

    def upload_a_file(self, place, branch_name, file_name):
        """
        Upload a file by creating a branch
        first and then sending a merge request
        :param place:
        :param branch_name:
        :param file_name:
        :return:
        """
        branch = self.create_branch(branch_name=branch_name)

        with open(place, "r") as file:
            data = file.read()

        file_upload = self.project.files.create(
            {
                "file_path": file_name,
                "branch": branch.name,
                "content": data,
                "author_email": AUTHOR_EMAIL,
                "author_name": AUTHOR_NAME,
                "commit_message": "Create yaml file",
            }
        )

        print(file_upload)

        self.create_merge_request(src_branch=branch.name, target_branch=GLOBAL_BRANCH)

    def create_merge_request(self, src_branch, target_branch):
        """
        Create a merge request from src branch to target branch
        :param src_branch: str
        :param target_branch: str
        :return:
        """
        merge_request = self.project.mergerequests.create(
            {
                "source_branch": src_branch,
                "target_branch": target_branch,
                "title": "merge cool feature using automation ;)",
            }
        )
        print(merge_request)

    def create_branch(self, branch_name):
        """
        Create a branch in your project. This is an unprotected normal branch
        :param branch_name:
        :return:
        """
        branch = self.project.branches.create(
            {"branch": branch_name, "ref": GLOBAL_BRANCH}
        )
        return branch


if __name__ == "__main__":
    PythonGitlab(
        url="https://gitlab.com/",
        authkey=YOUR PERSONAL ACCESS TOKEN,
        project=USERNAME/PROJECT_NAME,
    ).upload_a_file(
        place=r"raw/config.yaml",
        branch_name="test",
        file_name="config.yaml",
    )
