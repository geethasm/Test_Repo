import requests

def get_github_issue_description(owner, repo, issue_number, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {}

    if token:
        headers['Authorization'] = f'token {token}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issue = response.json()
        return issue.get('body', '')  # 'body' contains the description of the issue
    else:
        return f"Failed to fetch issue: {response.status_code} - {response.text}"

# Example usage:
owner = "umarali-nagoor"
repo = "Test_Repo"
issue_number = 1  # Replace with actual issue number
token = None  # Optional: your GitHub token here

description = get_github_issue_description(owner, repo, issue_number, token)
print(description)
