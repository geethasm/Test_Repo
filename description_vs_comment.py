import requests

def get_issue_description_and_comments(owner, repo, issue_number, token=None):
    base_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    # Get the issue itself
    issue_resp = requests.get(base_url, headers=headers)
    if issue_resp.status_code != 200:
        return f"Failed to get issue: {issue_resp.status_code} - {issue_resp.text}"

    issue_data = issue_resp.json()
    description = issue_data.get('body', '')

    # Get the comments
    comments_url = issue_data.get('comments_url')
    comments_resp = requests.get(comments_url, headers=headers)
    if comments_resp.status_code != 200:
        return f"Failed to get comments: {comments_resp.status_code} - {comments_resp.text}"

    comments_data = comments_resp.json()
    comments = [comment['body'] for comment in comments_data]

    return description, comments


# Example usage:
owner = "umarali-nagoor"
repo = "Test_Repo"
issue_number = 1  # Replace with the actual issue number
token = None  # Optional: your GitHub personal access token

description, comments = get_issue_description_and_comments(owner, repo, issue_number, token)

print("=== Issue Description ===")
print(description)
print("\n=== Comments ===")
for i, comment in enumerate(comments, 1):
    print(f"Comment {i}:\n{comment}\n")

