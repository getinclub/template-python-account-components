# The Account Links That Stopped One Hop Too Soon

A synthetic alias report treats every approved link as a finished group. A—B and B—C produce overlapping groups [A,B] and [B,C]. B is counted twice, even though A, B and C belong to one connected component. D has no links and must remain visible.

## Your task
Repair only `group_accounts(accounts, links)` in `components.py`. Preserve `_validate`. Do not change tests to turn the build green. The starter is intentionally faulty.

1. Use Python 3.12 and create a virtual environment.
2. Run `python -m pip install -r requirements.txt`.
3. Run `python monitor.py` to inspect the incident.
4. Run `python -m pytest -v`, fix the function, then rerun both commands.
5. Open a PR against `main` explaining the root cause, algorithm, complexity and regression tests.

## Contract
- `accounts` and `links` are lists. Account IDs are unique nonempty strings. IDs are case-sensitive and are not normalized.
- Each link is a two-item list or tuple of known IDs. Links are undirected and transitive. Self-links, duplicate and reversed links are valid.
- Return a list of lists: each account occurs exactly once, including isolated accounts. Every component includes all and only accounts reachable through the supplied links.
- Sort IDs inside each component using Python string ordering; sort the outer list lexicographically. Output must not depend on input order.
- Do not mutate inputs or retain state between calls. Reject any invalid input with `ValueError`; no partial result.
- Use union-find with path compression and size/rank balancing, or an equally scalable iterative graph traversal. Avoid recursion-depth failures, repeated whole-edge rescanning and quadratic pairwise reachability tables.

## Acceptance evidence
The supplied fixture should change from 3 overlapping groups and 5 memberships to 2 disjoint groups and 4 memberships: `[["A","B","C"],["D"]]`. Tests cover cycles, bridges, singletons, repeated/self links, order invariance, input ownership, invalid inputs and a 6,000-account chain.

This is a pure connectivity exercise using synthetic IDs and already-approved links. It does not validate link evidence, authorize account merges, deduplicate people, enforce access control or write customer records. A connected component is not proof that real accounts belong to the same person.
