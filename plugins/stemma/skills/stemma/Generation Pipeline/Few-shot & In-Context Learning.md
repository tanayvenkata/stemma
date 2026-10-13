---
tags: [generation]
reviewed: 2026-10-11
---
# Few-shot & In-Context Learning

Providing demonstrations inside the prompt and evaluating when they clarify the task versus anchor the model to brittle examples.

---

## The Decision: Do Exemplars Add Signal?

Few-shot performance depends on model, task, exemplar correctness, similarity, ordering, and prompt budget. Start with a zero-shot baseline, then add the smallest examples that clarify ambiguous semantics, formats, or boundary cases.

```
                            Few-Shot Prompting
                                     │
         ┌───────────────────────────┴───────────────────────────┐
         ▼                                                       ▼
[ Reasoning Demonstrations ]                            [ Task / Format Demonstrations ]
 • May anchor the model to a brittle path                • Clarify labels, boundaries, and output shape
 • Consume context and can contain hidden errors         • Can reduce task ambiguity
 • Compare concise answers vs worked solutions           • Still require model-specific evaluation
```

---

## 1. Reasoning Demonstrations: Benefits and Failure Modes

When using models with test-time reasoning:
- **Trajectory anchoring hypothesis**: A worked solution may bias the model toward its path even when another path fits the new problem better. Treat this as a failure mode to test, not a settled universal mechanism.
- **Context Pollution**: Long worked-out demonstrations consume context budget and may distract the model; compare them against concise ones rather than assuming either way.
- **Practical baseline**: Try zero-shot first, then compare concise demonstrations, worked demonstrations, and dynamically selected examples on held-out cases.

---

## 2. When Few-Shot is Still Indispensable

Few-shot is often useful in these scenarios:

| Scenario | Why Few-Shot Helps | Starting Point (confirm on held-out cases) |
|---|---|---|
| **Bespoke / Custom Formats** | Teaching a proprietary domain DSL or complex XML schema | Start with 1–2 minimal input/output format pairs (show the *shape*, not the reasoning); add more only if held-out format errors persist. |
| **Negative Exemplars (Anti-Fluff)** | Eliminating generic AI corporate filler | Start with one "Bad Output" vs "Good Output" pair; confirm on held-out cases that the filler drops and the bad example is not imitated. |
| **Ambiguous Classification Taxonomies** | Disambiguating borderline support ticket categories | Start with 2–3 examples of the boundaries your error analysis shows are confused; add more one at a time while per-class confusion keeps falling. |
| **Smaller or specialized models** | The model may need more task specification | Compare few-shot against fine-tuning, constrained outputs, and clearer instructions. |

---

## 3. Dynamic k-NN Exemplar Selection (For Large Datasets)

If using few-shot for classification or custom extraction across thousands of edge cases:
- Maintain a reviewed library of representative examples.
- Retrieve candidate exemplars by semantic and task metadata, then tune `k` on held-out data.
- Measure label leakage, near-duplicate contamination, ordering effects, latency, and performance on cases unlike the exemplar library.

---

## Part of
← [[Prompt Construction]]
