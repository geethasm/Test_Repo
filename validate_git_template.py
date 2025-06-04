import requests
import re
import argparse

def parse_issue_body(body_text):
    sections = {
        "problem_description": r"##\s*Problem description\s*(.*?)(?=##|$)",
        "steps_to_reproduce": r"##\s*Steps to reproduce\s*(.*?)(?=##|$)",
        "observed_expected": r"##\s*What is being observed & what is expected\s*(.*?)(?=##|$)",
        "failure_request_id": r"##\s*Failure Request Id or Job/Activity Id\s*(.*?)(?=##|$)",
        "supporting_logs": r"##\s*Supporting logs or screenshots\s*(.*?)(?=##|$)",
    }

    extracted = {}
    for key, pattern in sections.items():
        match = re.search(pattern, body_text, re.DOTALL | re.IGNORECASE)
        extracted[key] = match.group(1).strip() if match else '[Not provided]'
    return extracted

def get_github_issue(owner, repo, issue_number, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get issue #{issue_number}: {response.status_code} - {response.text}")

    return response.json()['body'] or ''

def main():
    parser = argparse.ArgumentParser(description="Fetch and parse GitHub issue data")
    parser.add_argument('owner', help='GitHub repo owner/user')
    parser.add_argument('repo', help='GitHub repo name')
    parser.add_argument('issues', nargs='+', help='Issue numbers or ranges (e.g. 1 3 5-7)')
    parser.add_argument('--token', help='GitHub Personal Access Token (optional)', default=None)

    args = parser.parse_args()

    # Expand ranges in issue list, e.g. "5-7" -> 5,6,7
    issue_numbers = []
    for item in args.issues:
        if '-' in item:
            start, end = item.split('-')
            issue_numbers.extend(range(int(start), int(end) + 1))
        else:
            issue_numbers.append(int(item))

    for num in issue_numbers:
        print(f"\n=== Issue #{num} ===")
        try:
            body = get_github_issue(args.owner, args.repo, num, args.token)
            data = parse_issue_body(body)
            for key, val in data.items():
                print(f"\n{key.replace('_', ' ').title()}:\n{val}")
            print("\n-----------------------------")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

