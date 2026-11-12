from copy import deepcopy
import random
import pytest
from components import group_accounts

@pytest.mark.parametrize("accounts,links,expected", [
    ([], [], []),
    (["A"], [], [["A"]]),
    (["C","A","B"], [], [["A"],["B"],["C"]]),
    (["A","B","C","D"], [("A","B"),("B","C")], [["A","B","C"],["D"]]),
    (["A","B","C"], [("A","B"),("B","C"),("C","A")], [["A","B","C"]]),
    (["A","B"], [("A","B"),("B","A"),("A","B")], [["A","B"]]),
    (["A","B"], [("A","A")], [["A"],["B"]]),
    (["A","B"], [("A","A"),("A","B")], [["A","B"]]),
    (["A","B","C","D"], [("A","B"),("C","D")], [["A","B"],["C","D"]]),
    (["A","B","C","D"], [("A","B"),("C","D"),("B","C")], [["A","B","C","D"]]),
    (["10","2","a","A"], [("a","2"),("10","A")], [["10","A"],["2","a"]]),
    (["é","e","E"], [("é","e")], [["E"],["e","é"]]),
])
def test_examples(accounts, links, expected):
    assert group_accounts(accounts, links) == expected

@pytest.mark.parametrize("accounts,links", [
    (None, []), (("A",), []), (["A"], None), (["A"], ()),
    (["A","A"], []), ([""], []), ([1], []), ([True], []),
    ([[]], []), (["A"], ["AA"]), (["A"], [("A",)]),
    (["A"], [("A","A","A")]), (["A"], [("A","B")]),
    (["A"], [("A",[]) ]), (["A"], [("A",False)]),
    (["A","B"], [("A","B"),("B","unknown")]),
])
def test_invalid_input(accounts, links):
    with pytest.raises(ValueError):
        group_accounts(accounts, links)

def test_inputs_and_output_do_not_alias():
    accounts=["C","B","A"]; links=[["A","B"],["B","C"]]
    before=deepcopy((accounts,links))
    result=group_accounts(accounts,links)
    assert (accounts,links)==before
    result[0].append("other")
    assert (accounts,links)==before

def test_permutations_and_partition():
    rng=random.Random(1106)
    accounts=list("ABCDEFG"); links=[["A","B"],["B","C"],["D","E"],["F","F"]]
    expected=[["A","B","C"],["D","E"],["F"],["G"]]
    for _ in range(40):
        rng.shuffle(accounts); rng.shuffle(links)
        flipped=[edge[::-1] if rng.randrange(2) else edge[:] for edge in links]
        result=group_accounts(accounts,flipped)
        assert result==expected
        assert sorted(x for g in result for x in g)==sorted(accounts)

def test_long_chain_without_recursion():
    accounts=[f"acct-{i:05}" for i in range(6000)]
    links=list(zip(accounts, accounts[1:]))
    assert group_accounts(accounts,links)==[accounts]

def test_multiple_calls_are_independent():
    assert group_accounts(["A","B"],[("A","B")])==[["A","B"]]
    assert group_accounts(["A","B"],[])==[["A"],["B"]]
