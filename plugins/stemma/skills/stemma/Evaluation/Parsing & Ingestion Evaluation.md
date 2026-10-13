---
tags: [evaluation]
---
# Parsing & Ingestion Evaluation

Parsing converts source artifacts into the representation every downstream component sees. Plausible output can silently omit a page, scramble reading order, shift a table value, or admit a document with the wrong access policy. Evaluate source fidelity and ingestion integrity directly; downstream answer quality alone cannot localize these failures.

## When This Enters the Build

Use this first, as soon as representative source files exist. It does not require retrieval or generation. Start with corpus-wide invariants such as page reconciliation, stable IDs, versioning, and authorization metadata, then annotate representative difficult pages and task-critical fields. Leave this stage with a versioned parsed corpus, known unsupported document classes, and an explicit escalation policy; otherwise every later metric rests on unverified input.

Return here when a source format, parser, OCR route, extraction policy, ingestion path, or access-control mapping changes—or when downstream diagnosis shows that required evidence never survived conversion.

## What Must Be Preserved

| Content class | Unit to label | Important failures |
|---|---|---|
| Running text or OCR | characters, words, paragraphs | substitutions, omissions, broken order |
| Layout | regions and reading sequence | mixed columns, orphan headings, lost footnotes |
| Tables and forms | cells, spans, headers, key-value associations | shifted values, merged cells, detached units |
| Figures and equations | object, caption, surrounding reference | missing object, wrong association, unusable transcription |
| Ingestion record | document, page, version, ACL, timestamp | missing/duplicate pages, staleness, unauthorized visibility |

Weight amounts, units, dates, negation, identifiers, eligibility language, and permissions separately from aggregate fidelity. A low average error rate does not make a corrupted dosage or contract limit acceptable.

## Build the Evaluation Set

1. Inventory document classes by format, source, layout complexity, scan quality, language, age, and risk.
2. Stratify common traffic and rare high-consequence formats. Include incidents and deliberately difficult pages.
3. Preserve rendered originals and annotate only the elements the product must recover.
4. Double-label ambiguous reading order, tables, or form associations; record adjudication and valid alternatives.
5. Add ingestion expectations: source ID, page count, version, checksum, timestamps, and authorization metadata.

Do not fully transcribe every page. Use deterministic checks over the whole corpus, precise annotations on representative pages, and task-critical field labels on high-risk documents.

## Signals and Their Meaning

| Signal | Reveals | Does not establish |
|---|---|---|
| Character/word error rate | transcription edits | layout or semantic fidelity |
| Region precision/recall or IoU | required layout objects found | correct order or content |
| Reading-order agreement | sequence preservation | accurate text within regions |
| Table structure similarity | row, column, span structure | correct cell values |
| Field accuracy/completeness | preservation of required facts | general document quality |
| Document/page reconciliation | drops and duplication | content fidelity |
| Freshness and ACL checks | operational correctness | semantic parsing quality |
| Escalation, latency, cost | routing feasibility | correctness |

Retain failure counts by document class and severity whenever one score compresses several failure types.

## Practical Experiment

1. State the routing or parser claim and predeclare critical failures.
2. Run every candidate on identical immutable sources; version parser, configuration, preprocessing, and gold artifacts.
3. Compare per-document paired outcomes and uncertainty, not only corpus averages.
4. Inspect disagreements against rendered originals, blinded to candidate identity when practical.
5. Measure gate recall: which serious failures were detected, missed, or unnecessarily escalated?
6. Run retrieval questions tied to labeled regions as impact evidence, not as a substitute for parser labels.
7. Replay malformed files, retries, duplicate deliveries, source updates, and permission changes.

## Decision and Diagnosis

Choose a parser or routing policy only if it meets predeclared must-not-fail constraints for critical fields, completeness, and authorization; improves the motivating slices by a meaningful amount; and has acceptable latency, cost, and escalation load. There is no universal error threshold because failure costs differ.

Change parsing when failures originate in conversion and recur often enough, or carry enough risk, to justify the route. If correct evidence exists in parsed output but is not retrieved, investigate chunking or retrieval. Turn every serious confirmed failure into a regression fixture.

Primary references: [DocLayNet](https://arxiv.org/abs/2206.01062) for diverse layout annotation and inter-annotator agreement, and [PubTabNet/TEDS](https://arxiv.org/abs/1911.10683) for table structure evaluation.

## Part of

← [[Component Evaluation Harness]]
