import openai
import requests
import os
import json

openai.api_key = "<your_api_key>"  # Or set directly as a string

def fetch_open_issues(repo_owner, repo_name, token=None):
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
            raise Exception(f"Failed to fetch issues: {response.status_code}")
        page_issues = response.json()
        if not page_issues:
            break
        open_issues += [issue for issue in page_issues if "pull_request" not in issue]
        page += 1

    return open_issues


def fetch_release_notes_content(repo_owner, repo_name, file_path, branch="main", token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref={branch}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content_json = response.json()
        import base64
        content_encoded = content_json.get("content", "")
        return base64.b64decode(content_encoded).decode("utf-8")
    else:
        raise Exception(f"Could not fetch release notes: {response.status_code}")


def detect_closed_issues_with_llm(issue_list, release_notes, repo_owner, repo_name):
    issue_summary = "\n".join([f"- #{issue['number']}: {issue['title']}" for issue in issue_list])
    system_prompt = "You are a helpful assistant that matches GitHub issues to mentions in release notes."
    user_prompt = f"""
You are given a list of open GitHub issues and the contents of a release notes file.

List of open GitHub issues:
{issue_summary}

Release notes:
\"\"\"{release_notes}\"\"\"

Your task is to return a list of issue numbers (in the format #123) that are clearly referenced in the release notes.
They may be referenced like: `#123`, `(#123)`, or full URLs like `https://github.com/{repo_owner}/{repo_name}/issues/123`.

Only return a clean list like:
#4
#3
#789

No explanations. Just the list.
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    output = response.choices[0].message.content
    return [line.strip() for line in output.splitlines() if line.strip().startswith("#")]

def send_slack_notification(slack_user: str, issue_number: int, repo_url: str, slack_token: str):
    headers = {"Authorization": f"Bearer {slack_token}"}
    message = f":white_check_mark: Hi {slack_user}, your issue #{issue_number} has been included in the release and can be closed! See: {repo_url}/issues/{issue_number}"
    
    payload = {
        "channel": slack_user,
        "text": message
    }

    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    if not response.ok or not response.json().get("ok"):
        print(f"⚠️ Failed to notify {slack_user}: {response.text}")

if __name__ == "__main__":
    # 🔧 CONFIGURATION
    repo_owner = "umarali-nagoor"
    repo_name = "Test_Repo"
    branch = "master"
    file_path = "release.md"
    github_token = None  # or os.getenv("GITHUB_TOKEN")

    print("Fetching release notes...")
    release_notes = fetch_release_notes_content(repo_owner, repo_name, file_path, branch, github_token)

    print("Fetching open issues...")
    issues = fetch_open_issues(repo_owner, repo_name, github_token)

    print("Using LLM to analyze which issues are closed...")
    closed_issues = detect_closed_issues_with_llm(issues, release_notes, repo_owner, repo_name)

    all_issues = [f"#{issue['number']}" for issue in issues]
    still_open = list(set(all_issues) - set(closed_issues))

    print("\n Issues can be closed")
    for issue in closed_issues:
        print(issue)

    print("\n Issues still open:")
    for issue in still_open:
        print(issue)

    user_map = json.load(open("user_mapping.json"))  # GitHub → Slack or email

    # for issue_str in closed_issues:
    #     issue_number = int(issue_str.lstrip("#"))
    #     issue_data = next((i for i in all_issues if i["number"] == issue_number), None)

    #     if issue_data:
    #         github_user = issue_data["user"]["login"]
    #         contact = user_map.get(github_user)
    #         if contact:
    #             send_slack_notification(contact, issue_number, repo_url, slack_token)
    #         else:
    #             print(f"⚠️ No contact info for GitHub user: {github_user}")


