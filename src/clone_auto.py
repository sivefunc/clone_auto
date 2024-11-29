import subprocess

import requests

from _version import __version__
from term_args import term_args

def get_gitlab_repos(user: str, *args, **kwargs) -> list:
    """Public Gitlab Repositories from a user
    """
    api = "https://gitlab.com/api/v4/users/USER/projects"
    try:
        response = requests.get(api.replace("USER", user), *args, **kwargs)
        response.raise_for_status()
    
    except requests.exceptions.RequestException as error:
        print(error)
        return []

    user_json = response.json()

    repos = [repo['http_url_to_repo'] for repo in user_json]
    return repos

def get_codeberg_repos(user: str, *args, **kwargs) -> list:
    """Public Gitlab repositories from a user
    """
    api = "https://codeberg.org/api/v1/users/USER/repos"
    try:
        response = requests.get(api.replace("USER", user), *args, **kwargs)
        response.raise_for_status()
    
    except requests.exceptions.RequestException as error:
        print(error)
        return []

    user_json = response.json()

    repos = [repo['clone_url'] for repo in user_json]
    return repos

def clone_repo(git_url: str) -> bool:
    """git clone git_url
    """
    command = ["git", "clone", git_url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    for c in iter(lambda: process.stdout.read(1), b""):
        print(c.decode('ascii'), end="")

PLATFORMS = {
        'gitlab': get_gitlab_repos,
        'codeberg': get_codeberg_repos
        }

def main():
    terminal = term_args()
    [user] = terminal.user
    for platform in terminal.platforms:
        for repo in PLATFORMS[platform](user):
            print(repo)

if __name__ == '__main__':
    main()
