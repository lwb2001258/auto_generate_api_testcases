from pathlib import Path, PurePath
from common.json_utils import *
from common.log_config import *


def read_json_file(path, env):
    json_data = {}
    ret_data = []
    name_start = Path(path).name.split('.')[-2]
    p = PurePath(path).parent
    files = (entry for entry in Path(p).glob(name_start + '*'))
    for file in files:
        try:
            with open(file, "r") as f:
                json_data = json.load(f)
        except Exception as e:
            logging.error("load json file {} error, error message is {}".format(path, e))

        for item in json_data.get(env):
            try:
                request_data = item.get("request")
                json_replace_mode(request_data, path, env)
                response_data = item.get("response")
                json_replace_mode(response_data, path, env)
                ret_data.append((request_data, response_data, item.get("envFlag")))
            except Exception as e:
                logging.error("parsing the json data error, error message is {}".format(e))
                ret_data.append((item.get("request"), item.get("response"), item.get("envFlag")))
    return ret_data


def get_json_data_from_es(testcase, env):
    path = testcase.replace("test_", "").replace("tests", "test_data").replace(".py", "/").replace("::", "") + "Step.json"
    return read_json_file(path, env)
