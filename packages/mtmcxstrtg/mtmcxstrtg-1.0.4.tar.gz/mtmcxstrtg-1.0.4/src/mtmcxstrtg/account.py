from mtmtool.webhook import auto_send as __auto_send
from mtmtool.io import read_yaml, read_json, write_json
import ccxt
import os
from mtmcxstrtg.util import split_list_execute_method

JSONPATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))

@split_list_execute_method(split_key="webhook_platform")
def auto_send(message, webhook_platform):
    return __auto_send(message, **webhook_platform)

class Account:
    """
    Settings in yaml should like this:
    account:
        -   userId: &userId "xx"
            exchange: binance
            params:
            apiKey: xx
            secret: xx
            timeout: 30000
            enableRateLimit: True
            webhook:
            -   platform: telegram
                token: xx
                chat: xx

    """
    def __init__(self, info_params: dict) -> None:
        self.info_params = info_params

        self.exchange = getattr(ccxt, self.info_params["exchange"])(self.info_params["params"])
        self.markets_cache_path = os.path.join(JSONPATH, self.info_params["exchange"]) + ".json"
        self.load_markets_cache()
        # self.exchange = ccxt.binance()
        pass

    def load_markets_cache(self):
        if not os.path.exists(self.markets_cache_path):
            self.exchange.load_markets()
            write_json(self.markets_cache_path, {
                "markets": self.exchange.markets,
                "currencies": self.exchange.currencies
            })
        else:
            self.exchange.set_markets(**read_json(self.markets_cache_path))

    def _send_message(self, message, webhook_platform):
        auto_send(message, **self.info_params["webhook"])
        if "webhook" not in self.info_params:
            return
        webhook_platforms = self.info_params["webhook"]

        # send message
        if isinstance(webhook_platforms, dict):
            return auto_send(message, **self.info_params["webhook"])
        elif isinstance(webhook_platforms, list):
            return [auto_send(message, **webhook_platform) for webhook_platform in webhook_platforms]
        else:
            raise Exception("info_params webhook type error! must be dict or list!")

    def send_message(self, message):
        if "webhook" not in self.info_params:
            return
        # send message
        auto_send(message, webhook_platform=self.info_params["webhook"])