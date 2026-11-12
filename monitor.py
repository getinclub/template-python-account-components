"""Deterministic synthetic evidence, not live account data."""
import json
from components import group_accounts

def replay():
    accounts = ["A", "B", "C", "D"]
    links = [["A", "B"], ["B", "C"]]
    actual = group_accounts(accounts, links)
    expected = [["A", "B", "C"], ["D"]]
    flat = [account for group in actual for account in group]
    return {"scenario": "synthetic alias connectivity", "accounts": accounts,
            "links": links, "actual_groups": actual, "expected_groups": expected,
            "group_count": len(actual), "membership_count": len(flat),
            "unique_account_count": len(set(flat)), "correct": actual == expected}

if __name__ == "__main__":
    print(json.dumps(replay(), indent=2))
