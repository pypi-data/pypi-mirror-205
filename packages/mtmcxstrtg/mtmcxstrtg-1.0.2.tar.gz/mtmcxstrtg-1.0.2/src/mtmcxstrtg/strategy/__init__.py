from cctt.binance import UMFutureHttpClient
from cctt.binance import SpotHttpClient
from mtmtool.log import create_file_logger, create_stream_logger
from mtmtool.webhook import telegram
from mtmtool.io import read_yaml, read_json, write_json
import requests
import pandas as pd
import numpy as np
import logging
import os


def json2dataframe(data):
    columns = [
        "open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "count",
        "taker_buy_volume", "taker_buy_quote_volume", "ignore"
    ]
    df = pd.DataFrame(data, columns=columns, index=None)
    for key in df.columns:
        df[key] = df.loc[:, key].astype(np.float64)
    return df


def order_send(client, order_param, logger):
    try:
        res = client.create_order(**order_param)
        logger.debug(res)
    except Exception as e:
        logger.error(order_param)
        raise e
    return res


def transfer_from_savings(client_spot, currency, amount):
    response = client_spot.savings_flexible_products(status="SUBSCRIBABLE")
    for i in response:
        if i["asset"] == currency:
            productId = i["productId"]
            break
    client_spot.savings_flexible_redeem(productId=productId, amount=float(amount), type="FAST")
    client_spot.user_universal_transfer("MAIN_UMFUTURE", currency, amount=str(amount))


def read_amount(amount_path):
    if os.path.exists(amount_path):
        amount_dict = read_json(amount_path)
        return amount_dict
    else:
        return {}


def write_amount(amount_path, amount_dict):
    write_json(amount_path, amount_dict)


def dict2text(text_dict):
    text_dict = {key: value for key, value in text_dict.items() if value is not None}
    text_list = []
    for key, value in text_dict.items():
        text_list.append(f"{key}: {value}")
    return "\n".join(text_list)


def main_func(yaml_path):
    yaml_path = os.path.abspath(yaml_path)
    config_dict = read_yaml(yaml_path)
    logger = create_file_logger("diffusd", yaml_path.replace(".yaml", ".log"), log_level=logging.DEBUG)

    # 读取amount dict, 记录了上次交易的信息
    amount_path = yaml_path.replace(".yaml", ".amount")
    amount_dict = read_amount(amount_path)
    last_num = amount_dict.get("num", None)
    last_price = amount_dict.get("price", None)
    last_amount = amount_dict.get("amount", None)

    # 读取配置文件
    name = config_dict["user"]["name"]
    api_key = config_dict["user"]["api_key"]
    secret_key = config_dict["user"]["secret_key"]
    token = config_dict["message"]["token"]
    chat_id = config_dict["message"]["chat"]
    symbol = config_dict["strategy"]["obj_coin"]["symbol"]
    currency = config_dict["strategy"]["obj_coin"]["amount"]["currency"]
    leverage = config_dict["strategy"]["obj_coin"]["amount"]["leverage"]
    once_usd = config_dict["strategy"]["obj_coin"]["amount"]["once_usd"]
    qty_min_step = 10**config_dict["strategy"]["obj_coin"]["precision"]["quantity"]
    pri_min_step = 10**config_dict["strategy"]["obj_coin"]["precision"]["price"]
    interval = config_dict["strategy"]["obj_coin"]["interval"]
    strategy_name = config_dict["strategy"]["name"]
    static_usd_symbol = config_dict["strategy"]["static_usd"]["symbol"]
    static_usd_interval = config_dict["strategy"]["static_usd"]["interval"]
    static_usd_price_open = config_dict["strategy"]["static_usd"]["price"]["open"]
    static_usd_price_close = config_dict["strategy"]["static_usd"]["price"]["close"]

    # 准备工作
    client = UMFutureHttpClient(api_key, secret_key)
    client_spot = SpotHttpClient(api_key, secret_key)
    data = client_spot.klines(static_usd_symbol, static_usd_interval, limit=200)
    df = json2dataframe(data)
    data2 = client.klines(symbol, interval, limit=200)
    df2 = json2dataframe(data2)
    price = df2.iloc[-1, 4]
    once_usd_actual = once_usd if last_amount is None else last_amount
    quantity = int(once_usd_actual * leverage / price * qty_min_step - 1) / qty_min_step
    order_param = {
        "symbol": symbol,
        "side": "BUY",
        "type": "MARKET",
        "quantity": quantity,
    }
    text_dict = {
        "account": name,
        "strategy": strategy_name,
        "monitor": static_usd_symbol,
        "execute": symbol,
    }

    if df.iloc[-2, 2] >= static_usd_price_close and not (last_num == 0 or last_num is None):
        # 平仓
        order_param["quantity"] = last_num
        order_param["reduceOnly"] = True
        order_param["side"] = "SELL"
        order_send(client, order_param, logger)
        # 发送消息
        expect_profit = (price / last_price - 0.002) - 1
        expect_earn_usd = expect_profit * last_num * last_price

        text_dict["side"] = "↓short↓"
        text_dict["coin"] = last_num
        text_dict["price"] = price
        text_dict["profit"] = str(round(expect_profit * 100, 2)) + "%"
        text_dict["earn(usd)"] = str(round(expect_earn_usd, 2))
        text = dict2text(text_dict)
        logger.info(text)
        telegram(text, token, chat_id)
        now_num = 0
        next_amount = round(expect_earn_usd + once_usd_actual, 2)
    elif df.iloc[-2, 3] <= static_usd_price_open and (last_num == 0 or last_num is None):
        # 平仓
        order_param["quantity"] = quantity
        order_send(client, order_param, logger)
        # 发送消息
        now_num = quantity
        text_dict["side"] = "↑long↑"
        text_dict["coin"] = now_num
        text_dict["price"] = price
        text = dict2text(text_dict)
        logger.info(text)
        telegram(text, token, chat_id)
        next_amount = once_usd_actual
    write_amount(amount_path, {"num": now_num, "price": price, "amount": next_amount})