---
tags: [indexing]
---
# OCR

Optical character recognition converts pixels containing text into characters and, in stronger systems, layout regions and reading order. It is required when no trustworthy text layer exists; it may also repair corrupted native text.

## Detection and Routing

An empty extraction is a strong signal, but nonempty text can still be wrong. Detect per page using text density, glyph validity, rendered/text alignment, scan/image characteristics, and sampled fidelity. Mixed documents require mixed routing.

## Quality Factors

- resolution, focus, contrast, skew, rotation, and noise;
- language, script, font, handwriting, and mathematical notation;
- columns, forms, tables, captions, and reading order;
- preprocessing such as deskewing, denoising, cropping, and binarization;
- confidence calibration and whether low-confidence regions are observable.

Critical OCR errors include digit/letter substitutions, missing decimal points or signs, broken identifiers, lost negation, and correct text attached to the wrong region.

## Extraction Choices

- classical or neural OCR for text recognition;
- OCR plus layout/table models for structured pages;
- vision-language structured extraction for visually complex regions;
- vision-native retrieval when converting to text would discard material evidence.

Compare paradigms on actual source classes. Vision-language extraction may use visual context but can omit, normalize, or invent content; traditional OCR can be highly faithful on clean scans but weak on structure.

## Evaluation

Measure character/word error where transcripts exist, region and reading-order fidelity, task-critical field accuracy, tables/structure, source localization, downstream evidence recovery, latency, cost, and escalation load. Inspect severe errors separately from averages and preserve rendered originals plus extractor provenance.

## Part of

← [[Parsing]]
