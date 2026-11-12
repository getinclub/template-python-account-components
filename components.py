"""Pure connected-component exercise. Never merges or writes real accounts."""

def group_accounts(accounts, links):
    """Return canonical disjoint groups under undirected transitive links.

    Repair this function only. Keep the supplied input validation contract.
    """
    _validate(accounts, links)
    # BUG: a direct link is mistaken for a complete component.
    groups = {tuple(sorted(set(edge))) for edge in links}
    linked = {account for edge in links for account in edge}
    groups.update((account,) for account in accounts if account not in linked)
    return [list(group) for group in sorted(groups)]


def _validate(accounts, links):
    if not isinstance(accounts, list) or not isinstance(links, list):
        raise ValueError("accounts and links must be lists")
    if any(not isinstance(x, str) or not x for x in accounts):
        raise ValueError("account IDs must be nonempty strings")
    if len(set(accounts)) != len(accounts):
        raise ValueError("duplicate account ID")
    known = set(accounts)
    for edge in links:
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError("each link must contain two account IDs")
        if any(not isinstance(x, str) or x not in known for x in edge):
            raise ValueError("link refers to an unknown account")
