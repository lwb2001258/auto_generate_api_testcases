import sys

sys.path.append("./")
sys.path.append("../")
import json
import os
from common.eureka_utils import *
import click


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def get_json_data_from_url(url):
    res = execute_http(url=url)
    return res[0]


def generate_test_files_and_json_files(json_data, service, author, env="qa", serviceUrl=""):
    json_dict = json.loads(json_data)
    paths = json_dict.get("paths")
    definitions = json_dict.get("definitions")
    tags = json_dict.get("tags")
    basePath = json_dict.get("basePath")
    if paths is None or definitions is None or tags is None:
        raise ValueError("the json file is not correct.")
    conftest_string = "def pytest_generate_tests(metafunc):\n"
    if not os.path.exists("../test_data/{}".format(service)):
        try:
            os.mkdir("../test_data/{}".format(service))
        except Exception as e:
            logging.error("make dir {} error, error msg is {}".format("../test_data/{}".format(service), e))
            return
    if not os.path.exists("../tests/{}".format(service)):
        try:
            os.mkdir("../tests/{}".format(service))
        except Exception as e:
            logging.error("make dir {} error, error msg is {}".format("../tests/{}".format(service), e))
            return
    with open("../tests/{}/__init__.py".format(service), "w") as f:
        f.close()
    with open("../tests/{}/conftest.py".format(service), "w") as confFile:
        confFile.write("from common.data_provider import *\n")
        confFile.write("\n")
        confFile.write("\n")
    for item in tags:
        tests_path = "../tests/{}/test_{}.py".format(service, service + "_" + item.get("name"))
        conf_path = "../tests/{}/conftest.py".format(service)
        with open(tests_path, 'w') as testFile:
            testFile.write("from common.eureka_utils import *\n")
            testFile.write("from common.data_provider import *\n")
            testFile.write("\n")
            testFile.write("\n")
            try:
                os.mkdir("../test_data/{}/{}".format(service, service + "_" + item.get("name")))
            except Exception as e:
                logging.info("make dir {} error, errMsg is {}".format(
                    "../test_data/{}/{}".format(service, service + "_" + item.get("name")), e))
    for key in paths.keys():
        for method_key in paths.get(key).keys():
            step = paths.get(key).get(method_key).get('operationId')
            if check_contain_chinese(step):
                continue
            try:
                path = key
                tag = paths.get(key).get(method_key).get("tags")[0]
                step = paths.get(key).get(method_key).get('operationId')
                try:
                    with open(conf_path, "a+") as confFile:
                        confFile.write("def {}_json_data(env):\n".format(step.replace(" ", "")))
                        if env == "us_qa":
                            confFile.write(
                                "    return get_json_data_from_es(\"tests/us/{}/test_{}.py::test_{}\", env)\n".format(
                                    service, service + "_" + tag, step.replace(" ", "")))
                        else:
                            confFile.write(
                                "    return get_json_data_from_es(\"tests/{}/test_{}.py::test_{}\", env)\n".format(
                                    service, service + "_" + tag, step.replace(" ", "")))
                        confFile.write("\n")
                        confFile.write("\n")
                except Exception as e:
                    pass
                conftest_string += "    if metafunc.function.__name__ == 'test_{}':\n".format(step.replace(" ", ""))
                conftest_string += "        test_data = {}_json_data(metafunc.config.getoption('test_env'))\n".format(
                    step.replace(" ", ""))
                conftest_string += "        metafunc.parametrize(\"test_data\", test_data)\n"
                method = method_key
                if env == "us_qa":
                    tests_path = "../tests/us/{}/test_{}.py".format(service, service + "_" + tag)
                else:
                    tests_path = "../tests/{}/test_{}.py".format(service, service + "_" + tag)

                with open(tests_path, 'a+') as testFile:
                    testFile.write("def test_{}(environment, envFlag, test_data):\n".format(step.replace(" ", "")))
                    testFile.write("    \"\"\"\n")
                    testFile.write("    author = \"{}\",\n".format(author))
                    testFile.write("    version = \"0.1.1\",\n")
                    testFile.write("    description = \"{}\",\n".format(paths.get(key).get(method_key).get("summary")))
                    testFile.write("    service = \"{}\",\n".format(service.lower()))
                    testFile.write("    enabled = True,\n")
                    testFile.write("    level = \"api\",\n")
                    testFile.write("    api = \"{}\",\n".format(path))
                    testFile.write("    method = \"{}\"\n".format(method.upper()))
                    testFile.write("    \"\"\"\n")
                    testFile.write(
                        "    request_data, response_data, envFlag_json = test_data[0], test_data[1], test_data[2]\n")
                    testFile.write("    if envFlag_json:\n")
                    testFile.write("        envFlag = envFlag_json\n")
                    testFile.write("    xGrayEnv = request_data.get(\"x-gray-env\")\n")
                    testFile.write("    xTraceID = request_data.get(\"x-trace-id\")\n")
                    testFile.write("    xUserId = request_data.get(\"x-user-id\")\n")
                    testFile.write(
                        "    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}\n")
                    testFile.write("    if xGrayEnv:\n")
                    testFile.write("        del request_data[\"x-gray-env\"]\n")
                    testFile.write("        headers[\"x-gray-env\"] = xGrayEnv\n")
                    testFile.write("    if xTraceID:\n")
                    testFile.write("        del request_data[\"x-trace-id\"]\n")
                    testFile.write("        headers[\"x-trace-id\"] = xTraceID\n")
                    testFile.write("    if xUserId:\n")
                    testFile.write("        del request_data[\"x-user-id\"]\n")
                    testFile.write("        headers[\"x-user-id\"] = xUserId\n")
                    if not serviceUrl:
                        testFile.write(
                            "    service_url = get_service_url(service=\"{}\", env_flag=envFlag, env=environment)\n".format(
                                service))
                    else:
                        testFile.write(
                            "    service_url = {}\n".format(serviceUrl))
                    if basePath != "/":
                        testFile.write("    url = service_url.rstrip(\"/\")+\"{}\"\n".format((basePath + path)))
                    else:
                        testFile.write("    url = service_url.rstrip(\"/\")+\"{}\"\n".format(path))
                    testFile.write(
                        "    res = execute_http(url=url, method=\"{}\", data=json.dumps(request_data), headers=headers)\n".format(
                            method.upper()))
                    testFile.write("    returnKey = None\n")
                    testFile.write("    for key in response_data.keys():\n")
                    testFile.write("        if \"returnStatus\" in key:\n")
                    testFile.write("            returnKey = key\n")
                    testFile.write("    if returnKey:\n")
                    testFile.write("        expectValue = response_data.get(returnKey)\n")
                    testFile.write("        checkReturnCode(returnKey, expectValue, res[1])\n")
                    testFile.write("        del response_data[returnKey]\n")
                    testFile.write("    execString = None\n")
                    testFile.write("    if response_data.get(\"execString\"):\n")
                    testFile.write("        execString = response_data.get(\"execString\")\n")
                    testFile.write("        del response_data[\"execString\"]\n")
                    testFile.write("    response_check(res[0], response_data)\n")
                    testFile.write("    if execString:\n")
                    testFile.write("        exec(execString)\n")
                    testFile.write("\n\n")
                    if env == "us_qa":
                        json_path = "../test_data/us/{}/{}/{}Step.json".format(service, service + "_" + tag,
                                                                               step.replace(" ", ""))
                    else:
                        json_path = "../test_data/{}/{}/{}Step.json".format(service, service + "_" + tag,
                                                                            step.replace(" ", ""))
                    with open(json_path, 'w') as f:
                        f.write("{\n")
                        f.write("  \"qa\":\n")
                        f.write("    [\n")
                        f.write("      {\n")
                        f.write("        \"request\":{\n")
                        try:
                            for item_index, item in enumerate(paths.get(key).get(method_key).get('parameters')):
                                if item.get("in") == "body":
                                    request_body = item.get("schema").get("$ref").replace("#/definitions/", "")
                                    body_property = definitions.get(request_body).get('properties').get("body")
                                    if body_property:
                                        if body_property.get("type") is None:
                                            f.write("            \"body\": {\n")
                                            body_class = body_property.get("$ref").replace("#/definitions/", "")
                                            class_dict = definitions.get(body_class)
                                            if class_dict.get('properties') is not None:
                                                for index, property_key in enumerate(
                                                        class_dict.get('properties').keys()):
                                                    if index != (len(class_dict.get('properties').keys()) - 1):
                                                        if class_dict.get('properties').get(property_key).get(
                                                                "type") == "string":
                                                            f.write("                \"{}\":\"string\",\n".format(
                                                                property_key))
                                                        elif class_dict.get('properties').get(property_key).get(
                                                                "type") in ["number", "integer", "long"]:
                                                            f.write("                \"{}\":0,\n".format(property_key))
                                                        elif class_dict.get('properties').get(property_key).get(
                                                                "type") == "boolean":
                                                            f.write(
                                                                "                \"{}\":false,\n".format(property_key))
                                                        elif class_dict.get('properties').get(property_key).get(
                                                                "type") == "array":
                                                            f.write("                \"{}\":[],\n".format(property_key))
                                                    else:
                                                        if item_index != len(
                                                                paths.get(key).get(method_key).get('parameters')) - 1:
                                                            if class_dict.get('properties').get(property_key).get(
                                                                    "type") == "string":
                                                                f.write("                \"{}\":\"string\"\n".format(
                                                                    property_key))
                                                                f.write("              },\n")
                                                            elif class_dict.get('properties').get(property_key).get(
                                                                    "type") in ["number", "integer", "long"]:
                                                                f.write(
                                                                    "                \"{}\":0\n".format(property_key))
                                                                f.write("              },\n")
                                                            elif class_dict.get('properties').get(property_key).get(
                                                                    "type") == "boolean":
                                                                f.write("                \"{}\":false\n".format(
                                                                    property_key))
                                                                f.write("              },\n")
                                                            elif class_dict.get('properties').get(property_key).get(
                                                                    "type") == "array":
                                                                f.write(
                                                                    "                \"{}\":[]\n".format(property_key))
                                                                f.write("              },\n")
                                                        else:
                                                            if class_dict.get('properties').get(property_key).get(
                                                                    "type") == "string":
                                                                f.write("                \"{}\":\"string\"\n".format(
                                                                    property_key))
                                                                f.write("              }\n")
                                                            elif class_dict.get('properties').get(property_key).get(
                                                                    "type") in [
                                                                "number", "integer", "long"]:
                                                                f.write(
                                                                    "                \"{}\":0\n".format(property_key))
                                                                f.write("              }\n")
                                                            elif class_dict.get('properties').get(property_key).get(
                                                                    "type") == "boolean":
                                                                f.write("                \"{}\":false\n".format(
                                                                    property_key))
                                                                f.write("              }\n")
                                                            elif class_dict.get('properties').get(property_key).get(
                                                                    "type") == "array":
                                                                f.write(
                                                                    "                \"{}\":[]\n".format(property_key))
                                                                f.write("              }\n")
                                            else:
                                                f.write("            },\n")
                                        elif body_property.get("type") == "string":
                                            if item_index != len(paths.get(key).get(method_key).get('parameters')) - 1:
                                                f.write("            \"body\": \"string\",\n")

                                        elif body_property.get("type") == "array":
                                            if item_index != len(paths.get(key).get(method_key).get('parameters')) - 1:
                                                f.write("            \"body\": [],\n")

                                        elif body_property.get("type") == "integer":
                                            if item_index != len(paths.get(key).get(method_key).get('parameters')) - 1:
                                                f.write("            \"body\": 0,\n")

                                        elif body_property.get("type") == "object":
                                            if item_index != len(paths.get(key).get(method_key).get('parameters')) - 1:
                                                f.write("            \"body\": {},\n")

                                elif item.get("in") == "query":
                                    f.write("              \"{}\":\"string\",\n".format(item.get("name")))

                                elif item.get("in") == 'header':
                                    if item_index != len(paths.get(key).get(method_key).get('parameters')) - 1:
                                        f.write("              \"{}\":\"string\",\n".format(item.get("name")))
                                    else:
                                        f.write("              \"{}\":\"string\"\n".format(item.get("name")))
                        except Exception as e1:
                            logging.error("generate request data error, errMsg is {}".format(e1))
                        f.write("        },\n")
                        f.write("        \"response\":{\n")
                        try:
                            for item_index, item in enumerate(paths.get(key).get(method_key).get('responses')):
                                if item == "200":
                                    dict200 = paths.get(key).get(method_key).get('responses').get("200")
                                    if "schema" in dict200.keys():
                                        dict_schema = dict200.get('schema')
                                        if '$ref' in dict_schema.keys():
                                            data_class = dict_schema.get("$ref").replace("#/definitions/", "")
                                            data_dict = definitions.get(data_class)
                                            property_dict = data_dict.get('properties')
                                            for property in property_dict.keys():
                                                if property_dict.get(property).get("type") == "integer":
                                                    f.write("          \"{}\": 0,\n".format(property))
                                                elif property_dict.get(property).get("type") == "string":
                                                    f.write("          \"{}\": \"string\",\n".format(property))
                                                elif property_dict.get(property).get("type") == 'boolean':
                                                    f.write(
                                                        "          \"{}\": true,\n".format(property))
                                                elif property_dict.get(property).get("type") == 'object':
                                                    f.write(
                                                        "          \"{}\": ".format(property) + "{},\n")
                                                elif property_dict.get(property).get("type") == 'array':
                                                    f.write(
                                                        "          \"{}\": [],\n".format(property))
                        except Exception as e:
                            logging.error("generate response data error, errMsg is {}".format(str(e)))
                        f.write("          \"returnStatus\": 200\n")
                        f.write("        }\n")
                        f.write("      }\n")
                        f.write("    ]\n")
                        f.write("}")
            except Exception:
                logging.error("generate test files error")
    try:
        with open(conf_path, "a+") as confFile:
            confFile.write(conftest_string)
    except:
        pass


def generate_test_files_and_json_files_by_service(service, author="lion@qq.com", env_flag="normal", env="qa"):
    service_url = get_service_url(service, env_flag, env).rstrip("/")
    url = "{}/v2/api-docs?group=all".format(service_url)
    json_data = get_json_data_from_url(url)
    generate_test_files_and_json_files(json_data=json_data, service=service, author=author, env=env)


def generate_test_files_and_json_files_from_json_file(file_path, service, author="lion@qq.com", env="qa",
                                                      serviceUrl=""):
    with open(file_path, "r", encoding="utf-8") as f:
        json_data = f.read()
    generate_test_files_and_json_files(json_data=json_data, service=service, author=author, env=env,
                                       serviceUrl=serviceUrl)


def generate_all_test_cases_and_json_files(author="lion@qq.com", env="qa"):
    service_list = get_all_service(env)
    for service in service_list:
        try:
            generate_test_files_and_json_files_by_service(service=service, author=author, env=env)
        except Exception as e:
            logging.error("generate test files error, service is {}, errMsg is {}".format(service, e))


@click.command()
@click.option('--service', help='service name')
@click.option('--env', default="qa", help="the environment of service")
@click.option('--envflag', default="normal", help='the gray flag of service')
@click.option('--author', default="lion@qq.com", help='the author create the test cases')
def generateTestCaseFromCmd(service, author, envflag, env):
    generate_test_files_and_json_files_by_service(service=service, author=author, env_flag=envflag, env=env)


@click.command()
@click.option('--filepath', help='service name')
@click.option('--service', default="service-1", help='service name')
@click.option('--author', default="lion@qq.com", help='the author create the test cases')
@click.option('--serviceUrl', default="", help='the service ip address')
def generateTestCaseFromJsonFile(filepath, service, author="lion.lin@qq.com", env="qa", serviceUrl=""):
    generate_test_files_and_json_files_from_json_file(filepath, service, author, env, serviceUrl)


if __name__ == "__main__":
    generateTestCaseFromCmd()
