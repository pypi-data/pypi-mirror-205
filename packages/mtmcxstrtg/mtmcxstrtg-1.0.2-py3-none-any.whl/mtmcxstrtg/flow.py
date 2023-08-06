import ccxt
from mtmcxstrtg.util import split_list_execute_method


@split_list_execute_method(split_key="userId")
def execute_ccxt_method(exchanges: dict, userId: str, method: str, params: dict):
    return getattr(exchanges[userId].exchange, method)(**params)


def action(action_info, envs):
    if action_info["type"] == "ccxt":
        return action_ccxt(action_info, envs)
    if action_info["type"] == "eval":
        return action_eval(action_info, envs)


def action_ccxt(action_info, envs):
    _info = action_info["params"].copy()
    for key, value in _info.items():
        if isinstance(value, str) and value.startswith("eval:"):
            _info[key] = eval(value[5:], envs)
    # 执行ccxt方法
    return execute_ccxt_method(envs["ccxt"], action_info["userId"], action_info["method"], _info)


def action_eval(action_info, envs):
    return eval(action_info["command"], envs)
