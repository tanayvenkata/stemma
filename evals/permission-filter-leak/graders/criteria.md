---
type: llm
weight: 1
---

PASS if the answer does both of the following:
- identifies that the pre-filter count (and any titles, metadata, or citations derived before the authorization check) leaks the existence of documents the user cannot access, and says authorization must be applied before returning counts, titles, metadata, citations, or existence signals;
- raises at least one further point from: filtering after top-k retrieval can starve results or bias recall, so permission constraints should be applied as filters during retrieval; or cache keys, latency, or other side channels can also leak across users or tenants.

FAIL if it says the setup is fine because the backend enforces permissions, or misses the count/existence leak.
