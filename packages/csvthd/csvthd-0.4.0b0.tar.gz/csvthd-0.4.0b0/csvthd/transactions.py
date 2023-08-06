# built in
import csv
from functools import reduce

# package
from .reducers import concat_details


def get_transactions(files):
    transactions = []
    for _file in files:
        with open(_file["filepath"], "r", newline="", encoding="utf-8") as f:
            rowreader = csv.reader(f)
            for idx, row in enumerate(rowreader):
                # skip header row if it has one
                if _file["hasHeaderRow"] is True and idx == 0:
                    continue

                # TODO: only do this when printing transactions, otherwise wasting
                # ... time concatenating transactions that are going to be filtered
                # ... out later
                # if detailsIdx is an array, perform concatenation
                _details_idx = _file["detailsIdx"]
                if type(_details_idx) is list:
                    # TODO: reflect on if this benefits enough from being a reducer
                    # ... to justify the reduction in code readability
                    _details = reduce(
                        concat_details, _details_idx, {"out": "", "row": row}
                    )["out"]
                else:
                    _details = row[_details_idx]

                transactions.append(
                    {
                        "date": row[_file["dateIdx"]],
                        "amount": float(row[_file["amountIdx"]]),
                        "details": _details,
                        "balance_at_time_of_transaction": row[
                            _file["balanceIdx"]
                        ],
                        "account_name": _file["accountName"],
                    }
                )
    return transactions
