---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
tags: [diagnose]
---

When I ask "Which fund has the lowest expense ratio?" the bot says the plan documents don't contain that information. But the fees are right there in funds.csv, and the fund SQL test works if I call it directly. What's going on?
