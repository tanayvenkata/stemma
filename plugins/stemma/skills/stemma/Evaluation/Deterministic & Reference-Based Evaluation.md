---
tags: [evaluation]
---
# Deterministic & Reference-Based Evaluation

## Contents

- The Core Distinction
- First-Pass Decision Path
- Deterministic Evaluator Families
- Reference-Based Evaluation
- Software-Testing Intuition
- Greenfield RAG Example
- Failure Modes and Defenses
- Implementation Record

Use deterministic evaluation when code can decide a criterion from explicit inputs, and reference-based evaluation when expected evidence, claims, outputs, or behavior bound the acceptable answer space. This is the foundation of an evaluation suite because it is reproducible, cheap to rerun, and easy to diagnose—but only inside the contract encoded by its rules and references.

## The Core Distinction

```text
source of expected behavior              scorer
──────────────────────────              ──────
schema or invariant          ────────→  executable assertion
typed expected value         ────────→  normalized comparison
evidence regions or labels   ────────→  set/rank/coverage calculation
required claims/reference    ────────→  exact, structured, or semantic comparison
task environment             ────────→  execute and inspect outcome
```

A reference is not inherently deterministic. `expected_total: 42.50 USD` supports a typed comparison; an example essay may still require semantic or human judgment. Choose the scorer according to what equivalence means for the task.

## First-Pass Decision Path

1. **State the property.** Examples: valid schema, correct identifier, required evidence retrieved, calculation within tolerance, citation resolves, tool action changes the expected state.
2. **Identify the authority.** Schema, source document, database state, executable environment, required claims, or accepted output set.
3. **Choose the narrowest valid equivalence rule.** Exact equality, normalization, numeric tolerance, set relation, region overlap, ordered ranking, state transition, or another explicit predicate.
4. **Test positive, negative, and boundary cases.** A passing happy path does not show that the assertion rejects the wrong behavior.
5. **Record diagnostics, not only pass/fail.** Preserve expected and observed values, rule/version, relevant trace, and bounded error category.
6. **Escalate only the unresolved semantic remainder.** Do not replace a valid assertion with a model judge; do not force code to decide meaning it cannot represent.

## Deterministic Evaluator Families

| Family | Examples | Main trap |
|---|---|---|
| Contract assertions | schema, type, required fields, citation/source IDs, authorization, allowed tool arguments | valid structure can contain wrong meaning |
| Normalized equality | case/whitespace normalization, canonical dates, identifiers, enum aliases | aggressive normalization can erase meaningful differences |
| Typed numeric checks | units, tolerances, intervals, financial reconciliation | arbitrary tolerance or unit conversion can certify error |
| Set and sequence checks | required/forbidden items, subset/superset, order constraints, duplicates | incomplete references can punish valid discoveries |
| Evidence and ranking calculations | region coverage, Recall@K, Precision@K, MRR, nDCG | validity depends on label completeness and gain definitions |
| Executable outcome checks | query database, run code/tests, inspect tool or simulator state | environment and oracle can be wrong or nondeterministic |

The Metrics note defines the mathematical constructs. This note defines how to turn an explicit contract into an evaluator.

## Reference-Based Evaluation

Prefer a structured expectation over one ideal answer string:

```yaml
expected_behavior: answer
required_claims:
  - warranty duration is two years
optional_claims:
  - coverage begins on purchase date
forbidden_claims:
  - accidental damage is covered
supporting_evidence:
  - manual-v3/page-14/region-7
acceptable_variants:
  - "24 months"
abstain_if:
  - purchase jurisdiction is unknown
```

Use the least interpretive matching rule that preserves validity:

```text
exact typed value
→ normalized or set comparison
→ structured claim extraction plus explicit predicates
→ semantic model or human judgment when valid expression is too open-ended
```

Do not make reference wording or length the hidden target. Several answers can be correct, and one reference rarely exhausts an open-ended answer space.

## Software-Testing Intuition

- **Example/unit test:** this known input must produce this bounded behavior.
- **Property test:** many generated inputs must obey an invariant, such as never returning another tenant's document.
- **Metamorphic test:** transform an input in a way that predicts a relation between outputs; paraphrasing a query should preserve intent, while removing decisive evidence should trigger abstention.
- **Differential test:** run two implementations on the same cases and inspect disagreements without assuming either is automatically correct.
- **Mutation test:** deliberately inject a known defect—wrong citation, missing evidence, changed number—to verify that the evaluator actually catches it.

These methods deepen deterministic evaluation without adding subjective scoring. They test the evaluator as well as the system.

## Greenfield RAG Example

Begin the thin vertical slice with checks such as:

- every indexed region maps to an authorized source version;
- required evidence regions appear within the retrieval cutoff;
- returned citations resolve to evidence actually supplied to generation;
- structured fields parse and satisfy type/range constraints;
- a known unanswerable case abstains rather than inventing a source;
- latency, token, and cost measurements are present rather than silently missing.

Add references for bounded task content. Add a semantic judge only for the remaining property—such as nuanced claim support—that explicit predicates cannot decide validly at the required scale.

## Failure Modes and Defenses

| Failure | Plain-language symptom | Defense |
|---|---|---|
| Brittle reference | valid paraphrases fail | represent claims/variants or move only that comparison to semantic evaluation |
| Incomplete ground truth | newly useful evidence counts as irrelevant | mark it unjudged and route it through the labeling lifecycle |
| Fixture coupling | system passes by reproducing test artifacts | use stable source-level expectations, protected cases, and leakage checks |
| Weak assertion | malformed or harmful behavior still passes | add negative/boundary cases and mutation-test the evaluator |
| Hidden nondeterminism | identical runs disagree despite an “exact” test | version inputs/environment and repeat only the stochastic boundary |
| Oracle error | executable reference confidently returns the wrong result | validate the oracle and reconcile against another authority where consequences justify it |

## Implementation Record

For each evaluator retain its criterion, authority/reference version, input and output schema, normalization or tolerance rule, pass/fail logic, diagnostics, known blind spots, and owner. Run fast objective checks frequently; place slower executable checks according to runtime and risk. A framework can schedule and report them, but ordinary review must still verify that the assertion represents the intended decision.

## Part of

← [[Evaluation Strategy & Experimental Design]]
