import os
import openai
from datetime import datetime, timedelta
#from slack_sdk import WebClient

# -------- CONFIG ----------
openai.api_key = "<key>"  # Or set directly as a string
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")  # optional, for notifications
SLACK_CHANNEL = "#your-channel"

#openai.api_key = OPENAI_API_KEY
#slack_client = WebClient(token=SLACK_BOT_TOKEN) if SLACK_BOT_TOKEN else None

# -------- LLM RELEVANCE CHECK --------
def check_issue_relevance_with_llm(issue_title, issue_body, roadmap_text):
    prompt = f"""
You are a product manager assistant.

Product roadmap:
{roadmap_text}

GitHub Issue:
Title: {issue_title}
Body: {issue_body}

Question: Is this GitHub issue relevant to the product roadmap? Answer "Yes" or "No" only.
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        answer = response.choices[0].message.content.strip().lower()
        return answer.startswith("yes")
    except Exception as e:
        print(f"LLM call failed: {e}")
        # fallback to false to be safe
        return False

# -------- Slack Notification --------
# def send_slack_notification(user, issue_url):
#     if not slack_client:
#         print(f"Slack not configured. Would notify {user} about issue {issue_url}")
#         return
#     try:
#         slack_client.chat_postMessage(
#             channel=SLACK_CHANNEL,
#             text=f"<@{user}>, regarding issue {issue_url}: I feel this issue is unrelated to the current product roadmap. Would you like to close it?"
#         )
#         print(f"Sent Slack notification to {user} for issue {issue_url}")
#     except Exception as e:
#         print(f"Slack API error: {e}")

# -------- Main Logic --------
def filter_irrelevant_issues(issues, roadmap_text, now=None):
    """
    issues: list of dicts with keys:
        - title (str)
        - body (str or None)
        - labels (list of str)
        - last_comment_date (datetime)
        - assignee (str or None)
        - user (str)
        - html_url (str)
    roadmap_text: str
    now: datetime for current time (optional)
    """
    if not now:
        now = datetime.utcnow()

    unrelated = []

    for issue in issues:
        title = issue.get("title", "")
        body = issue.get("body") or ""
        labels = [lbl.lower() for lbl in issue.get("labels", [])]
        last_comment_date = issue.get("last_comment_date", now)
        assignee = issue.get("assignee")
        user = issue.get("user")
        url = issue.get("html_url")

        # Step 1: LLM relevance check
        relevant = check_issue_relevance_with_llm(title, body, roadmap_text)
        if relevant:
            continue

        # Step 2: fallback checks
        days_since_comment = (now - last_comment_date).days

        if "in-progress" in labels and days_since_comment <= 30:
            continue  # still relevant
        elif "backlog" in labels or days_since_comment > 30:
            # Notify user via Slack
            notify_user = assignee or user
            #send_slack_notification(notify_user, url)
            unrelated.append(issue)

    return unrelated

# -------- Example usage --------
if __name__ == "__main__":
    # Example roadmap text (could be loaded from file)
    roadmap_text = """
Q1 2025:
- AI-based content recommendations
- Onboarding workflow redesign
- Unified user profile system

Q2 2025:
- Multi-language support
- Team collaboration tools
- Scheduled reporting engine
"""

    # Example issues list (replace with real GitHub issues data)
    example_issues = [
        {
            "title": "Build ML model for content suggestion",
            "body": "This implements AI content recommendations for users.",
            "labels": ["in-progress"],
            "last_comment_date": datetime.utcnow(),
            "assignee": "john_doe",
            "user": "john_doe",
            "html_url": "https://github.com/owner/repo/issues/1"
        },
        {
            "title": "Refactor legacy payment system",
            "body": "Needs to improve payment reliability.",
            "labels": ["backlog"],
            "last_comment_date": datetime.utcnow() - timedelta(days=40),
            "assignee": None,
            "user": "jane_smith",
            "html_url": "https://github.com/owner/repo/issues/2"
        },
        {
            "title": "AI-based content recommendations",
            "body": "Needs to improve payment reliability.",
            "labels": ["in-progress"],
            "last_comment_date": datetime.utcnow(),
            "assignee": None,
            "user": "jane_smith",
            "html_url": "https://github.com/owner/repo/issues/3"
        }
    ]

    irrelevant_issues = filter_irrelevant_issues(example_issues, roadmap_text)
    print("\nIrrelevant issues found:")
    for issue in irrelevant_issues:
        print(f"- {issue['title']} ({issue['html_url']})")
