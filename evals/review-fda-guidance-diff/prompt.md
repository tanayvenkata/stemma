---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
tags: [review]
---

This tool compares two versions of an FDA guidance PDF and labels what changed. Regulatory-affairs people are going to rely on it. Please review it and tell me where it could miss real changes or report fake ones, and whether the validation backs up the README claims.
