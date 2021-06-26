import re

def regex_match_param_key(regex_str):
    pattern = "\$\{(.*)\}"
    res = re.search(pattern, regex_str)
    if res:
        return res.group(1)


def get_service_from_path(path):
    pattern = ".*test_data/(.*)/(.*)/(.*)json"
    res = re.search(pattern, path)
    if res:
        return res.group(1)

