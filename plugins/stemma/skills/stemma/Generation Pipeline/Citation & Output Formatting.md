---
tags: [generation]
---
# Citation & Output Formatting

Citation formatting exposes provenance; citation evaluation determines whether the source actually supports the claim. Not every statement needs a citation, but externally verifiable material claims should follow the product's declared evidence policy.

## Citation Contract

- stable source and region identifier;
- mapping from each material claim to one or more supporting spans;
- source title/version/date and authorization-safe display fields;
- behavior for conflicting, partial, or absent evidence;
- rendering rules for the destination;
- machine-readable representation retained separately from display text.

Validate citation **entailment**, **completeness**, **placement**, **source suitability**, and **accessibility**. A syntactically valid citation can be irrelevant; a correct answer can still violate a grounding requirement.

## Output Validation

Apply layers in order:

1. parse/schema validation;
2. type, range, and cross-field business rules;
3. claim/evidence and citation checks;
4. authorization and sensitive-data checks;
5. destination-specific escaping and rendering.

Syntax repair is safe only when it cannot change meaning. Otherwise regenerate under a bounded policy, degrade to a safer form, abstain, or escalate. Preserve raw and served forms for evaluation.

## Part of

← [[Post-Generation Processing]]
