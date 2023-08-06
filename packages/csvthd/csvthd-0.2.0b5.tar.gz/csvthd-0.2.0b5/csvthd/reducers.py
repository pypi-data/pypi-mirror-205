def sum_transaction_amount(acc, cur):
    # append transaction to acc so it isn't eaten after being provided by filter
    acc[0].append(cur)
    # add transaction amount to sum
    acc[1] += cur["amount"]
    # return accumulator
    return acc
