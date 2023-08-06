# built in
from datetime import datetime
from functools import reduce

# site
import click

# package
from .filters import (
    details_include_filter,
    details_exclude_filter,
    amount_is_filter,
)
from .commandline import print_transaction, style_amount
from .transactions import get_transactions
from .config import load_config
from .reducers import sum_transaction_amount

# TODO: consider looking into (odx?) other formats because someone mentioned apparently there
# ... are some other commons ones that are standardized.

# TODO: add option to get calculate total sum of filtered out transactions


@click.command()
@click.option(
    "-i",
    "--include",
    multiple=True,
    help="Only show transactions that contain the given substring in their details.",
)
@click.option(
    "-E",
    "--exclude",
    multiple=True,
    help="Only show transactions that don't contain the given substring in their details.",
)
@click.option(
    "-a",
    "--amount",
    multiple=True,
    nargs=2,
    help="Only show transactions with amounts under/over/equal to value.",
)
@click.option(
    "-s",
    "--sort-by",
    type=click.Choice(["date", "amount"]),
    default="date",
    help="Sort transactions by given property.",
)
@click.option(
    "-r", "--reverse-sort", is_flag=True, help="Reverse sorting order."
)
@click.option(
    "-S",
    "--sum",
    is_flag=True,
    help="Give a sum of all transaction amounts after filtering.",
)
def cli(include, exclude, amount, sort_by, reverse_sort, sum):
    filters = []

    # create include filters
    filters.append(details_include_filter(include))

    # create exclude filters
    filters.append(details_exclude_filter(exclude))

    # create amount is filters
    [filters.append(amount_is_filter(_amt[0], _amt[1])) for _amt in amount]

    config = load_config()
    transactions = get_transactions(config["files"])

    # sort transactions
    if sort_by == "date":
        transactions.sort(
            key=lambda t: datetime.strptime(t["date"], "%d/%m/%Y").timestamp(),
            reverse=reverse_sort,
        )
    elif sort_by == "amount":
        transactions.sort(key=lambda t: t["amount"], reverse=reverse_sort)
    else:
        raise ValueError("Invalid 'sort_by' type")

    # apply all filters
    for _filter in filters:
        transactions = filter(_filter, transactions)

    # calculate sum
    sum_amount = None
    if sum:
        transactions, sum_amount = reduce(
            sum_transaction_amount, transactions, [[], 0]
        )

    print("---[ TRANSACTIONS ]---")
    for transaction in transactions:
        print_transaction(transaction)

    # if sum calculated, print it
    if sum_amount is not None:
        print("---[ REPORTS ]---")
        print(f" | SUM AMT: {style_amount(sum_amount)} |")

    if len(filters) == 0:
        print("\nHint: Use `--help` to learn how to filter transactions.")
