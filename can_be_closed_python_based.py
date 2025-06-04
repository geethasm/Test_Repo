import requests
import re
import base64
from typing import List, Dict


def download_release_notes(repo_owner: str, repo_name: str, file_path: str, branch: str = "main", token: str = None) -> str:
    """
    Downloads the release notes file content using GitHub API (supports private repos).
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={branch}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content_json = response.json()
        file_content_base64 = content_json.get("content", "")
        file_content = base64.b64decode(file_content_base64.encode("utf-8")).decode("utf-8")
        return file_content
    else:
        raise Exception(f"Failed to fetch file from API: HTTP {response.status_code}")


def get_closed_issues(issue_list: List[Dict], release_notes_content: str) -> List[str]:
    """
    Compares open issue numbers against release notes content.
    """
    closed_issues = []
    content = release_notes_content.lower()

    for issue in issue_list:
        issue_number = f"#{issue['number']}"
        if re.search(re.escape(issue_number.lower()), content):
            closed_issues.append(issue_number)

    return closed_issues


def get_open_issues(repo_owner: str, repo_name: str, token: str = None) -> List[Dict]:
    """
    Fetches a list of open issues from a GitHub repository.
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    issues_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    params = {"state": "open", "per_page": 100}
    open_issues = []
    page = 1

    while True:
        params["page"] = page
        response = requests.get(issues_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issues: HTTP {response.status_code} - {response.text}")

        issues = response.json()
        if not issues:
            break

        open_issues.extend([issue for issue in issues if "pull_request" not in issue])
        page += 1

    return open_issues


if __name__ == "__main__":
    # 🔧 CONFIGURATION
    repo_owner = "umarali-nagoor"
    repo_name = "Test_Repo"
    file_path = "release.md"
    branch = "master"
    github_token = None  # Set your GitHub token if repo is private

    try:
        print("📥 Downloading release notes...")
        release_notes_content = download_release_notes(repo_owner, repo_name, file_path, branch, github_token)

        print("🐛 Fetching open issues...")
        issue_list = get_open_issues(repo_owner, repo_name, github_token)

        print(f"📋 Open issues for {repo_owner}/{repo_name}:")
        for issue in issue_list:
            print(f"- #{issue['number']}: {issue['title']} (created by {issue['user']['login']})")

        print("\n🔍 Checking which issues are mentioned in the release notes...")
        closed_issues = get_closed_issues(issue_list, release_notes_content)

        print("\n✅ Issues found in release notes and can be closed:")
        for issue in closed_issues:
            print(issue)

        print("\n❌ Issues not found in release notes and still open:")
        for issue in issue_list:
            issue_number = f"#{issue['number']}"
            if issue_number not in closed_issues:
                print(issue_number)

    except Exception as e:
        print(f"❗ Error: {e}")
