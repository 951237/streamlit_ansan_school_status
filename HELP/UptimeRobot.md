# UptimeRobot Quick Reference

## Overview
UptimeRobot is a hosted monitoring service that pings endpoints on configurable schedules (1–5 minutes on the free plan) and alerts when downtime exceeds a threshold. It supports HTTP(S), keyword matching, TCP/UDP ports, ICMP (ping), and heartbeats, which makes it useful for keeping Streamlit Cloud apps awake or validating cron-driven data pipelines.

## Account & Pricing (2024)
- Free tier: up to 50 monitors, 5-minute interval, one status page, email alerts, and basic logs (up to 24 hours).
- Pro tier: 1-minute checks, multiple status pages, 1 year of logs, SMS/voice/Slack/Teams integrations, and maintenance windows.
- Enterprise: custom limits, SLA-backed support, multi-user controls, audit logs, and sub-accounts.

## Typical Setup Steps
1. Sign up at uptimeRobot.com (email + password or OAuth). Confirm email to unlock API access.
2. Create a monitor: choose type (HTTP(s), keyword, port, ping, or heartbeat), set friendly name, URL/IP, and check interval.
3. Add alert contacts (email, SMS, Slack webhook, Microsoft Teams, Discord, Telegram, Opsgenie, PagerDuty, webhooks). Associate contacts per monitor.
4. Optional: define maintenance windows to suppress notifications during planned downtime.
5. (Optional) Enable the “Keep-alive” behavior by creating an HTTP monitor pointing to your Streamlit Cloud URL to prevent the free dyno from idling.

## Useful Features
- **Keyword check**: ensures response contains/omits specific strings, handy for verifying CSV timestamp text in the dashboard.
- **Heartbeat monitor**: accepts periodic POSTs from scheduled jobs (e.g., GitHub Actions). Missed heartbeats trigger alerts, confirming crawlers run on time.
- **Status pages**: share real-time uptime with stakeholders; customize branding and embed iframes.
- **Incident notes**: add context during outages so collaborators know mitigation steps.
- **API v2**: RESTful interface for creating monitors, fetching logs, and integrating into IaC scripts. Free plan allows API usage with a generated key.

## Recommended Workflow for This Project
1. Create an HTTP monitor targeting the deployed Streamlit URL (e.g., `https://ansan-schools.streamlit.app/`) with a 5-minute interval.
2. Set alert contacts to your email and (optionally) Slack webhook so you know when the app sleeps or errors.
3. Configure a heartbeat monitor and hit it at the end of the GitHub Actions crawl job to ensure data refresh tasks run daily.
4. Publish a public status page named “안산 학교 현황판” so stakeholders can confirm service health before demos.
5. Review logs weekly; if downtime is frequent due to cold starts, consider moving to a free-tier container host as discussed in DOC/251109_개선사항.md.

## Limitations & Tips
- Free plan logs only 24 hours; export logs or upgrade if you need historical SLA metrics.
- Alerts fire after a second check fails (default 1 minute after the first failure), so very short outages might not be captured.
- For keyword monitors, response must be <1 MB; large Streamlit pages might need HTTP checks instead.
- Combine with GitHub Actions or cron jobs: trigger the Streamlit URL with `curl` alongside UptimeRobot monitoring to fully prevent idling.
