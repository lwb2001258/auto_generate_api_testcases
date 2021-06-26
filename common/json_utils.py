import json
from common.regex_utils import *
from common.config_utils import *
from common.random_utils import *
from common.time_utils import *


def response_check(return_json, response_dict):
    try:
        return_dict = json.loads(return_json)
    except Exception as e:
        print(e)
        # raise TypeError("return_json should be a str")
        return
    for key in response_dict:
        if type(response_dict.get(key)) == list:
            if type(return_dict.get(key)) == list:
                for item in response_dict.get(key):
                    if type(item) != dict:
                        assert item in return_dict.get(key)
                    else:
                        if item in return_dict.get(key):
                            continue
                        check_dict_keys = item.keys()
                        check_num = 0
                        for item2 in return_dict.get(key):
                            if type(item2) == dict:
                                item2_keys = item2.keys()
                                if set(check_dict_keys).issubset(item2_keys):
                                    check_num += 1
                                    response_check(json.dumps(item2), item)
                        assert check_num > 0, "there are not dict can check with it"
            else:
                raise AssertionError("return {} is {}, not a list, can not compare to a list".format(key.strip(">="), return_dict.get(key.strip(">="))))
        elif type(response_dict.get(key)) != dict:
            if key.endswith(">="):
                assert return_dict.get(key.strip(">=")) >= response_dict.get(key), "return {} is {}, not >= {}".format(key.strip(">="), return_dict.get(key.strip(">=")), response_dict.get(key))
            elif key.endswith("<="):
                assert return_dict.get(key.strip("<=")) <= response_dict.get(key), "return {} is {}, not <= {}".format(key.strip("<="), return_dict.get(key.strip("<=")), response_dict.get(key))
            elif key.endswith("!="):
                assert response_dict.get(key) != return_dict.get(key.strip("!=")), "return {} is {}, not != {}".format(key.strip("!="), return_dict.get(key.strip("!=")), response_dict.get(key))
            elif key.endswith("<"):
                assert return_dict.get(key.strip("<")) < response_dict.get(key), "return {} is {}, not < {}".format(key.strip("<"), return_dict.get(key.strip("<")), response_dict.get(key))
            elif key.endswith(">"):
                assert return_dict.get(key.strip(">")) > response_dict.get(key), "return {} is {}, not > {}".format(key.strip(">"), return_dict.get(key.strip(">")), response_dict.get(key))
            else:
                assert response_dict.get(key) == return_dict.get(key), "return {} is {}, not = {}".format(key, return_dict.get(key), response_dict.get(key))
        else:
            response_check(json.dumps(return_dict.get(key)), response_dict.get(key))


def checkReturnCode(returnKey, expectValue, returnValue):
    if returnKey.endswith(">="):
        assert returnValue >= expectValue, "return status code is {}, not >= {}".format(returnValue, expectValue)
    elif returnKey.endswith("<="):
        assert returnValue <= expectValue, "return status code is {}, not <= {}".format(returnValue, expectValue)
    elif returnKey.endswith("!="):
        assert returnValue != expectValue, "return status code is {}, not != {}".format(returnValue, expectValue)
    elif returnKey.endswith(">"):
        assert returnValue > expectValue, "return status code is {}, not > {}".format(returnValue, expectValue)
    elif returnKey.endswith("<"):
        assert returnValue < expectValue, "return status code is {}, not < {}".format(returnValue, expectValue)
    else:
        assert returnValue == expectValue, "return status code is {}, not = {}".format(returnValue, expectValue)


def json_replace_mode(data_dict, path, env):
    for key in data_dict.keys():
        value = data_dict.get(key)
        if type(value) == str:
            param_key = regex_match_param_key(value)
            if param_key:
                service = get_service_from_path(path)
                cf = Config_Util(env)
                param_value = cf.get_property(service, param_key)
                data_dict[key] = param_value
            elif value.strip() == "get_localtime_str()":
                data_dict[key] = get_localtime_str()
            elif value.strip() == "get_local_timestamp()":
                data_dict[key] = get_local_timestamp()
            elif regex_random_length(value.strip()):
                data_dict[key] = get_random_str(regex_random_length(value.strip()))
        elif type(value) == list:
            for index, item in enumerate(value):
                if type(item) == str:
                    param_key = regex_match_param_key(item)
                    if param_key:
                        service = get_service_from_path(path)
                        cf = Config_Util(env)
                        param_value = cf.get_property(service, param_key)
                        value[index] = param_value
                    elif value.strip() == "get_localtime_str()":
                        data_dict[key] = get_localtime_str()
                    elif value.strip() == "get_local_timestamp()":
                        data_dict[key] = get_local_timestamp()
                    elif regex_random_length(value.strip()):
                        data_dict[key] = get_random_str(regex_random_length(value.strip()))
                elif type(item) == dict:
                    json_replace_mode(item, path, env)
        elif type(value) == dict:
            json_replace_mode(value, path, env)
