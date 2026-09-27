# Research instructions

Read the [fixed question](campaigns/ternary-symmetric-justified-envy/question.md), [prior state](campaigns/ternary-symmetric-justified-envy/state.md) and [preparation notes](campaigns/ternary-symmetric-justified-envy/work/preparation.md). The fixed [test corpus](campaigns/ternary-symmetric-justified-envy/work/cases.json) and [verifier](campaigns/ternary-symmetric-justified-envy/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/ternary-symmetric-justified-envy/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
