import requests

from _version import __version__

def get_gitlab_repos(user: str, *args, **kwargs) -> list:
    """Public Gitlab Repositories from a user
    """
    api = "https://gitlab.com/api/v4/users/USER/projects"
    response = requests.get(api.replace("USER", user), *args, **kwargs)
    response.raise_for_status()
    user_json = response.json()

    repos = [repo['http_url_to_repo'] for repo in user_json]
    return repos

def main():
    for repo in get_gitlab_repos('sivefunc'):
        print(repo)

if __name__ == '__main__':
    main()
