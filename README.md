# AI-Driven - Auto monitoring and regulating of GitHub issues                                       

## Problem

In today’s real world scenario, let’s discuss about Alex, the Product Manager, manages strategic product requirements through the AHA tool. Nina, the Project Manager, aligns execution by mapping each AHA item to corresponding GitHub issues and epics. John, Team lead works closely with Nina to break down AHA items into actionable issues and manages them throughout the development lifecycle.
 

Nina relies on these issues to update the progress and ensure traceability across the SDLC. At the core of the workflow lies the synergy between product managers, project managers, and engineering teams.

 
Despite scheduled tri-weekly syncs between Alex and Nina, the meetings often revolve around pulling fragmented updates directly from developers’ minds, since comments in GitHub issues are either linked, incomplete or outdated. Nina’s manual coordination with the team not only slows down the process but also creates knowledge silos and dependency bottlenecks.

### Offering
 
This is where, Ideaprenur team is providing an offering to promote traceability and visibility using LLM powered on release notes, and AHA roadmaps. Our offering presents a recursive, AI-driven solution to automate, and optimize issue lifecycle management. And intelligently correlates GitHub issues with AHA roadmap and release note data to identify stale, irrelevant, or completed items. Also through Slack-based prompting, it requests clarification or auto-resolve from relevant team members.

### Benefits
 
Imagine the efficiency gains in various scenarios such as support tickets, leadership asks, customer queries, etc., if the issues were properly updated, validated, and closed in alignment with the roadmap and release progress. This is the ideal state, multiple systemic and behavioral challenges prevent its realization.

### Solution

The offering mainly identifies the stale, irrelevant, open issues, and notify the issue owner by tagging through slack channel by considering factors such as
 
- AHA roadmap
- Release note data
- Issue status
- Age of an issue’s latest comments
 
### System Architecture

![Architecture Diagram](images/H_LLM.png)


The LLM powered GitHub issue triage system architecture comprises three layers:
 
- Data sources such as GitHub Issues API, AHA roadmap and release note exports.
- LLM Processing Layer that Classifies issues as relevant or not, based on AHA roadmap, release note, issue status, and age of an issue latest comments.
- Action Engine automatically closes or flags issues, generates comments, triggers Slack alerts, and maintains an audit trail.
 
### Innovation

- Zero-touch automation enables seamless issue tracking, eliminating the need for manual intervention.
- Slack-triggered workflows streamline issue lifecycle management directly from team communication channels.
- AI-driven decision-making intelligently classifies, updates, and resolves issues based on context and relevance.

### Technologies

![Applied technologies](images/H_User_Flow.png)
 
- GPT-4, Claude, LLaMA 3 for LLM capabilities
- Slack Bolt API for team communication
- GitHub and GitLab REST APIs
- Python FastAPI, Flask modules with LangChain for orchestration.
 
This intelligent orchestration system not only reduces manual intervention but also enhances productivity by keeping all stakeholders informed and aligned, thereby turning disjointed updates into an actionable source of truth.
 

Our offering demo are just around the corner, Thank you all, and see you soon!
