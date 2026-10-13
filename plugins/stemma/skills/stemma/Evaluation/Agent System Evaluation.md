---
tags: [evaluation]
---
# Agent System Evaluation

## Contents

- When This Enters the Build
- Specify the Task and Environment
- Validate the evaluation harness
- Capture a Structured Trajectory
- Define What Is Actually Scored
- Score at Three Levels
- Reliability Across Repeated Runs
- Component Protocols
- Counterfactual and Perturbation Tests
- Evaluators and Uncertainty
- Decision Output
- Sources

Agentic systems require evaluation of both terminal outcome and trajectory. A correct answer can conceal unsafe actions, wasted work, policy violations, or a strategy that succeeds by accident.

## When This Enters the Build

Add this when the system can choose actions over time: whether to retrieve, which tool or route to use, how to update memory or state, when to retry, and when to stop. A single RAG answer without autonomous decisions usually needs generation and system evaluation, not a full trajectory harness.

Begin with a sandboxed task environment, deterministic invariants, and terminal outcomes. Add step-level semantic judgments only where multiple plausible trajectories cannot be checked through state and rules. Leave with replayable tasks, structured traces, acceptable action sets or constraints, and separate outcome, safety, and resource measures.

## Specify the Task and Environment

Version the initial state, user goal, hidden facts, permissions, budgets, stopping conditions, available tools and schemas, side effects, simulated services, acceptable terminal states, unacceptable irreversible states, and sources of environment randomness. Use sandboxed or simulated tools for destructive and security-sensitive actions.

## Validate the evaluation harness

An agent evaluation measures the model, instructions, runtime, tools, and environment together. Before attributing failure to the agent:

1. run a reference solution or scripted policy that proves the task is solvable;
2. verify every grader assertion follows from the task contract rather than an unstated implementation detail;
3. confirm tool behavior, fixtures, permissions, clocks, network, and external services are stable enough for the claim;
4. measure infrastructure flakes and retry them under a declared policy, without silently retrying genuine agent failures;
5. ensure the evaluated harness matches production in every behavior that could affect the result;
6. preserve harness and environment versions with the trial.

A persistent zero pass rate can indicate a broken or underspecified task. A surprising success can indicate a grader loophole, leaked answer, or environment shortcut. Inspect both rather than treating the score as self-explanatory.

## Capture a Structured Trajectory

For each step record visible state, available actions, selected action, arguments, observation, latency, cost, policy checks, side effects, and termination reason. Preserve raw traces, but derive stable semantic events so evaluation does not depend on one provider's trace format.

## Define What Is Actually Scored

An agent can complete the task in an environment while its final chat message says only “done,” or it can claim success while the authoritative state never changed. Before choosing a metric, specify the scored artifact:

| Task | Canonical scored artifact |
|---|---|
| Information answer | extracted final answer plus cited evidence |
| API or workflow action | authoritative state diff and external receipt |
| Software change | resulting patch/workspace plus test and review evidence |
| Research task | source set, claim/evidence map, and final artifact |
| Simulation policy | terminal world state and event trajectory |

Implement and test the extractor or state adapter as part of the harness. Log the exact artifact sent to each evaluator and spot-check it. Scoring the last assistant message by habit can turn a successful tool result into a false failure—or accept an eloquent false success.

## Score at Three Levels

| Level | Core question | Example labels |
|---|---|---|
| Outcome | Did the task end acceptably? | full success, partial success, safe failure, unsafe failure |
| Trajectory | Were decisions valid and useful? | necessary action, valid alternative, redundant step, dead end, policy violation |
| Operations | Was execution reliable and proportionate? | tool/schema error, retry recovery, loop, latency, cost, irreversible action |

When several plans are valid, label an **acceptable action set** or state constraints rather than requiring an exact reference trace. Exact matching is appropriate only when the procedure itself is required.

## Reliability Across Repeated Runs

A single success can hide an unstable policy. Repeat representative tasks when model or environment variance matters and preserve each attempt rather than silently retrying to a favorable result.

- **Per-run success** asks how often an ordinary attempt succeeds.
- **`pass@k`** asks whether at least one of up to `k` attempts succeeds. It is useful when multiple independent attempts are an allowed product strategy, but it can reward expensive lottery-ticket behavior.
- **`pass^k`** asks whether all `k` repeated attempts succeed. It emphasizes consistency and falls quickly when rare failures remain.
- **Safe-failure rate** asks whether unsuccessful attempts abstain, escalate, or terminate without unacceptable effects.

Estimate these empirically on the actual repeated-run protocol. Do not infer independence when attempts share state, cached results, correlated model behavior, or environment conditions. Report attempts, total resource use, and unsafe failures alongside any best-of-`k` result.

## Component Protocols

- **Retrieve or answer:** label whether available evidence was sufficient; count unsafe answers and unnecessary retrieval separately.
- **Tool or route selection:** test whether the action was permitted, applicable, and capable of advancing state.
- **Arguments:** validate schemas deterministically, then check semantic constraints and user intent.
- **Multi-step information gathering:** measure whether each step added evidence, resolved uncertainty, or merely consumed budget.
- **Synthesis:** map material claims and decisions to observations or evidence.
- **Termination:** distinguish completion, justified abstention/escalation, premature stopping, and looping.

## Counterfactual and Perturbation Tests

Replay the task while varying one condition: tool error, latency, ambiguous observation, reordered results, missing evidence, budget, or irrelevant content. If exact replay is impossible, run matched trials and report outcome distributions rather than one trajectory.

Also test evaluation awareness and reward hacking where the harness could reveal the grader or expected path. Withhold hidden state and grader internals from the agent, use unseen neighboring tasks, and check whether apparent success satisfies the real environment contract rather than gaming a proxy. Creative valid solutions should pass; loopholes that violate the intended contract should trigger a task or grader repair.

## Evaluators and Uncertainty

Use deterministic checks for permissions, schemas, budgets, state transitions, tool results, and invariants. Use human review or calibrated judges for plan appropriateness and partially ordered outcomes. Measure judge disagreement on difficult slices and retain human review for high-impact ambiguity.

Report success with unsafe-action rate, justified-escalation rate, tool reliability, steps, tokens, wall time, and cost. Efficiency is a constrained objective: compare it only among policies satisfying safety and quality requirements.

When a semantic judge sees full trajectories, test whether irrelevant reasoning length, tool chatter, agent identity, or action order changes a criterion that should depend only on outcome. Score process only when the process is part of the construct; do not accidentally reward or punish visible collaboration.

## Decision Output

Identify the candidate policy, environment manifest, outcome and trajectory changes by slice, critical violations, uncertainty across trials, and whether to adopt, constrain, reject, or gather more evidence. Promote new failure mechanisms into regression testing.

Keep capability and regression suites separate. Capability tasks should remain discriminating and may begin with low pass rates; solved, stable behaviors can graduate into regression coverage. Monitor saturation, task validity, environment flakes, and protected-set exposure as properties of the evaluation program.

## Sources

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [OpenAI Docs: Agent evals](https://developers.openai.com/api/docs/guides/agent-evals)

## Part of

← [[Component Evaluation Harness]]
