# Triangle Partition → Ternary symmetric justified envy-free triples

Category: Complexity open

## Source

The source gives a simple graph. Its outputs are partitions of its vertices into triples each inducing a triangle, or NO-SOLUTION.

## Target

The target has symmetric pair values in {0,1,2} and asks for a partition into triples with no justified envy. An agent envies replacing another when its utility improves and both remaining members strictly prefer the incoming agent.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This isolates existence complexity in a small-valued symmetric coalition model.

## Difficulty

Every unintended triple must be excluded under the exact justified-envy condition, rather than a stronger stability notion.

## Literature context

Results for asymmetric preferences, larger utility alphabets or stronger stability notions do not classify the stated ternary symmetric justified-envy predicate.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [2024 paper](https://link.springer.com/article/10.1007/s10458-024-09657-6): McKay, Cseh and Manlove's 2024 paper, Theorems 4.3, 4.12 and 4.16, separates binary valuations, unrestricted ternary valuations and symmetric valuations in {0,...,6}. Section 5 explicitly asks for the ternary symmetric boundary. The inspected arXiv record was last revised August 2, 2024. The exact target would resolve a named fair coalition-formation boundary; importance is moderate, with no broader consequence established.
- [arXiv record](https://arxiv.org/abs/2209.07440): McKay, Cseh and Manlove's 2024 paper, Theorems 4.3, 4.12 and 4.16, separates binary valuations, unrestricted ternary valuations and symmetric valuations in {0,...,6}. Section 5 explicitly asks for the ternary symmetric boundary. The inspected arXiv record was last revised August 2, 2024. The exact target would resolve a named fair coalition-formation boundary; importance is moderate, with no broader consequence established.

Fixed from board record `website/questions/ternary-symmetric-justified-envy.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
