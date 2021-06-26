import random
import re


def get_random_str(length=6):
    random_str = ""
    base_str = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789"
    n = len(base_str) - 1
    for i in range(length):
        index = random.randint(0, n)
        random_str += base_str[index]
    return random_str


def regex_random_length(reg_str):
    pattern = "get_random_str\((.*)\)"
    res = re.search(pattern, reg_str)
    if res:
        if res.group(1).isdigit():
            return int(res.group(1))
        else:
            return 6