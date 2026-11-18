---
name: ponytail
description: Use when choosing an implementation, refactor or documentation structure. Ship the smallest complete solution; avoid speculative complexity.
---

# Ponytail: simplest complete path

1. Name the actual problem and acceptance checks. Separate must-haves from hypothetical future needs.
2. Inspect existing code, scripts and docs. Reuse a proven path before adding another tool, abstraction or dependency.
3. Choose the smallest reversible change that satisfies the whole contract. Prefer one source of truth with links over copied rules.
4. Avoid generic frameworks, mass cleanup, compatibility breaks and plans larger than the work. Explain a larger design only when concrete constraints require it.
5. Test observable behavior and relevant failure paths. Simplicity never means skipping authorization, validation, migration safety or verification.
6. Review the diff for removable machinery. Report the change, real checks and remaining limits in a few lines.

For documentation, shorten prose and navigation first. Do not delete essential caveats, license notices or historical evidence to reduce line count.

Done when the result works, evidence supports the claim, and no unrelated mechanism remains.
