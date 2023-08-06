import os
from mtmtool.io import read_json, write_json
from functools import wraps, partial


def get_profit(price_current, price_last, fee, islong):
    price_current = float(price_current)
    price_last = float(price_last)
    fee = float(fee)
    if islong:
        expect_profit = (price_current / price_last) - 1 - fee
    else:
        expect_profit = 1 - (price_current / price_last) - fee
    return expect_profit


def get_earn(profit, coin, last_price):
    return float(profit) * float(coin) * float(last_price)


def read_amount(amount_path):
    if os.path.exists(amount_path):
        amount_dict = read_json(amount_path)
        return amount_dict
    else:
        return {}


def write_amount(amount_path, amount_dict):
    write_json(amount_path, amount_dict)


def split_list_execute_method(func=None, split_key=None):
    if func is None:
        return partial(split_list_execute_method, split_key=split_key)
    if split_key is None:
        raise ValueError("split_key is None")

    @wraps(func)
    def wrapper(*args, **kwargs):
        if split_key in kwargs:
            split_values = kwargs[split_key]
            del kwargs[split_key]
            if isinstance(split_values, list):
                result = []
                for item in split_values:
                    kwargs[split_key] = item
                    result.append(func(*args, **kwargs))
                return result
        else:
            return func(*args, **kwargs)

    return wrapper