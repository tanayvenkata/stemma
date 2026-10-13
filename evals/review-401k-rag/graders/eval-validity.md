---
type: llm
weight: 1
---

PASS if the answer explains that the evaluation cannot support decisions, citing at least one concrete reason from the code: only 8 cases, the generator model also judges itself, routing correctness is never checked, or a golden case's answer is hard-coded into the prompts. FAIL if the eval is accepted at face value or criticized only generically.
