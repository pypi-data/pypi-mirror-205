from mtmtool.log import create_file_logger, create_stream_logger, logging
from mtmtool.io import read_yaml, read_json, write_json
import os
from mtmcxstrtg.flow import action
from mtmcxstrtg.util import get_earn, get_profit, read_amount, write_amount
from mtmcxstrtg.config import PyConfig
from mtmcxstrtg.account import Account


def order_send(client, order_param, logger):
    try:
        res = client.create_order(**order_param)
        logger.debug(res)
    except Exception as e:
        logger.error(order_param)
        raise e
    return res


def main_func(yaml_path):
    # 读取yaml文件
    yaml_path = os.path.abspath(yaml_path)
    config_dict = read_yaml(yaml_path)
    accounts_info = config_dict["account"]
    strategy_info = config_dict["strategy"]

    # 创建日志
    logger = create_file_logger("logger", yaml_path.replace(".yaml", ".log"), log_level=logging.DEBUG)

    # 读取amount dict, 记录了上次交易的信息
    amount_path = yaml_path.replace(".yaml", ".amount")
    amount_dict = read_amount(amount_path)
    last_num = amount_dict.get("quantity", None)
    last_price = amount_dict.get("price", None)
    last_amount = amount_dict.get("asset", None)

    # 准备工作, 读取yaml中的初始设置，来创建本地参数副本
    envs = strategy_info["init_settings"].copy()
    envs["base_coins"] = strategy_info["init_settings"]["base_coins"] if last_amount is None else last_amount
    envs["quote_coins"] = 0 if last_num is None else last_num

    # 准备工作, 从yaml中的流配置中创建需要的部分参数
    clients = {account_info["userId"]: Account(account_info) for account_info in accounts_info}
    envs["ccxt"] = clients
    for flow_item in config_dict["strategy"]["flow"]:
        envs[flow_item["var"]] = action(action_info=flow_item["action"], envs=envs)

    # 以下是策略逻辑
    for trigger_item in strategy_info["trigger"]:
        if envs[trigger_item["condition"]]:
            # 交易
            action(action_info=trigger_item["action"], envs=envs)

            # 记录本次交易信息
            messages = strategy_info["sendtemplate"].copy()
            messages["side"] = "↑buy↑" if trigger_item["action"]["params"]["side"].lower() == "buy" else "↓sell↓"
            messages["coin"] = envs["amount"]
            messages["price"] = envs["price_current"]
            next_amount = envs["base_coins"]
            next_quantity = float(envs["amount"])
            if trigger_item["status"] == "close" and last_price:
                expect_profit = get_profit(envs["price_current"], last_price, 0.001, trigger_item["side"] == "long")
                expect_earn_usd = get_earn(expect_profit, float(envs["amount"]), last_price)
                messages["profit"] = float(expect_profit)
                messages["earnValue"] = float(expect_earn_usd)
                next_amount = envs["base_coins"] + expect_earn_usd
                next_quantity = 0

            # 发送消息
            message = PyConfig.dict2formattext(messages)
            logger.info(message)
            _userIds = trigger_item["action"]["userId"]
            userIds = _userIds if isinstance(_userIds, list) else [_userIds]
            for userId in userIds:
                clients[userId].send_message(message)

    # 保存amount dict, 记录了本次交易的信息
    write_amount(amount_path, {"quantity": next_quantity, "price": envs["price_current"], "asset": next_amount})


if __name__ == '__main__':
    main_func("cta_.yaml")