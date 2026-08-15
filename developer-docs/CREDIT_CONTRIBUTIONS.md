# CRediT author contributions

Use the repository's **CRediT author contributions** issue form to agree on and record the
contribution statement for a manuscript.

1. Open a new issue and select **CRediT author contributions**.
2. Enter the manuscript title or identifier and the complete author roster in publication order.
   Use one author per line.
3. For each of the 14 CRediT roles, enter one author per line. Enter `N/A` when a role does not
   apply. Names must exactly match the ordered roster.
4. After every author has reviewed the assignments, select the approval checkbox and submit the
   issue.

To generate the contribution statement, edit the submitted issue, copy its raw Markdown body to a
file such as `credit-issue.md`, and run:

```bash
python3 scripts/generate_credit_statement.py credit-issue.md
```

The utility prints an author-ordered statement with each author's roles in official CRediT order:

```text
Ada Lovelace: Conceptualization, Methodology; Grace Hopper: Software, Supervision
```

It also accepts the issue body on standard input:

```bash
gh issue view ISSUE_NUMBER --json body --jq .body | \
  python3 scripts/generate_credit_statement.py -
```

If an assigned name does not exactly match the roster, or the approval checkbox is not selected,
the utility exits with an error instead of generating a statement.
