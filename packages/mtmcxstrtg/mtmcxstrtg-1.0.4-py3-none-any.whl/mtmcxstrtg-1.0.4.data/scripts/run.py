import os, sys
import mtmcxstrtg.strategy as strategy
import mtmcxstrtg
from mtmtool.log import create_file_logger, logging

import argparse

parser = argparse.ArgumentParser("Run Strategy")
parser.add_argument("-c", dest="yaml", type=str, help="yaml file path", default="test.yaml")
parser.add_argument("-m", dest="strategy", type=str, help="strategy method", default="cta_deviation_signal_strategy")

args = parser.parse_args()
# main_func("/home/dbl/app/invest_ratio/188_ETHBUSD.yaml")
try:
    getattr(mtmcxstrtg, args.strategy).main_func(args.yaml)

except Exception as e:
    yaml_path = os.path.abspath(args.yaml)
    config = mtmcxstrtg.PyConfig(yaml_path)
    strategy_name = config["strategy"]["name"]
    logger = create_file_logger(strategy_name, yaml_path.replace(".yaml", ".log"), log_level=logging.DEBUG)
    logger.error(e)
    accounts = [mtmcxstrtg.Account(account) for account in config["account"]]
    file_name = os.path.basename(yaml_path)
    if "ReduceOnly Order is rejected" in str(e):
        pass
    for account in accounts:
        account.send_message(f"{file_name}(strategy_name):{e}")