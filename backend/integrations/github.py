from github import Github
from config_db import get_integration_config

def create_github_issue(title, body):
    """
    Create a new issue in the configured GitHub repository.
    """
    config = get_integration_config('github')
    if not config:
        raise ValueError("GitHub integration is not configured.")

    # Authenticate with GitHub
    github = Github(config['access_token'])
    repo = github.get_repo(config['repository'])

    # Create issue
    issue = repo.create_issue(title=title, body=body)
    return issue
