from common.eureka_utils import *
from common.data_provider import *


def test_bizAssetTagsUsingPOST(environment, envFlag, test_data):
    """
    author = "lion@qq.com",
    version = "0.1.1",
    description = "bizAssetTags",
    service = "service-1",
    enabled = True,
    level = "api",
    api = "1111",
    method = "POST"
    """
    request_data, response_data, envFlag_json = test_data[0], test_data[1], test_data[2]
    if envFlag_json:
        envFlag = envFlag_json
    xGrayEnv = request_data.get("x-gray-env")
    xTraceID = request_data.get("x-trace-id")
    xUserId = request_data.get("x-user-id")
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    if xGrayEnv:
        del request_data["x-gray-env"]
        headers["x-gray-env"] = xGrayEnv
    if xTraceID:
        del request_data["x-trace-id"]
        headers["x-trace-id"] = xTraceID
    if xUserId:
        del request_data["x-user-id"]
        headers["x-user-id"] = xUserId
    service_url = get_service_url(service="service-1", env_flag=envFlag, env=environment)
    url = service_url.rstrip("/")+"/22222"
    res = execute_http(url=url, method="POST", data=json.dumps(request_data), headers=headers)
    returnKey = None
    for key in response_data.keys():
        if "returnStatus" in key:
            returnKey = key
    if returnKey:
        expectValue = response_data.get(returnKey)
        checkReturnCode(returnKey, expectValue, res[1])
        del response_data[returnKey]
    execString = None
    if response_data.get("execString"):
        execString = response_data.get("execString")
        del response_data["execString"]
    response_check(res[0], response_data)
    if execString:
        exec(execString)


def test_getAssetByCodeUsingPOST(environment, envFlag, test_data):
    """
    author = "lion@qq.com",
    version = "0.1.1",
    description = "step1",
    service = "service-1",
    enabled = True,
    level = "api",
    api = "22222",
    method = "POST"
    """
    request_data, response_data, envFlag_json = test_data[0], test_data[1], test_data[2]
    if envFlag_json:
        envFlag = envFlag_json
    xGrayEnv = request_data.get("x-gray-env")
    xTraceID = request_data.get("x-trace-id")
    xUserId = request_data.get("x-user-id")
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    if xGrayEnv:
        del request_data["x-gray-env"]
        headers["x-gray-env"] = xGrayEnv
    if xTraceID:
        del request_data["x-trace-id"]
        headers["x-trace-id"] = xTraceID
    if xUserId:
        del request_data["x-user-id"]
        headers["x-user-id"] = xUserId
    service_url = get_service_url(service="service-1", env_flag=envFlag, env=environment)
    url = service_url.rstrip("/")+"/111111"
    res = execute_http(url=url, method="POST", data=json.dumps(request_data), headers=headers)
    returnKey = None
    for key in response_data.keys():
        if "returnStatus" in key:
            returnKey = key
    if returnKey:
        expectValue = response_data.get(returnKey)
        checkReturnCode(returnKey, expectValue, res[1])
        del response_data[returnKey]
    execString = None
    if response_data.get("execString"):
        execString = response_data.get("execString")
        del response_data["execString"]
    response_check(res[0], response_data)
    if execString:
        exec(execString)


def test_getAssetListUsingPOST(environment, envFlag, test_data):
    """
    author = "lion@qq.com",
    version = "0.1.1",
    description = "getAssetList",
    service = "service-1",
    enabled = True,
    level = "api",
    api = "33333",
    method = "POST"
    """
    request_data, response_data, envFlag_json = test_data[0], test_data[1], test_data[2]
    if envFlag_json:
        envFlag = envFlag_json
    xGrayEnv = request_data.get("x-gray-env")
    xTraceID = request_data.get("x-trace-id")
    xUserId = request_data.get("x-user-id")
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
    if xGrayEnv:
        del request_data["x-gray-env"]
        headers["x-gray-env"] = xGrayEnv
    if xTraceID:
        del request_data["x-trace-id"]
        headers["x-trace-id"] = xTraceID
    if xUserId:
        del request_data["x-user-id"]
        headers["x-user-id"] = xUserId
    service_url = get_service_url(service="service-1", env_flag=envFlag, env=environment)
    url = service_url.rstrip("/")+"/333333"
    res = execute_http(url=url, method="POST", data=json.dumps(request_data), headers=headers)
    returnKey = None
    for key in response_data.keys():
        if "returnStatus" in key:
            returnKey = key
    if returnKey:
        expectValue = response_data.get(returnKey)
        checkReturnCode(returnKey, expectValue, res[1])
        del response_data[returnKey]
    execString = None
    if response_data.get("execString"):
        execString = response_data.get("execString")
        del response_data["execString"]
    response_check(res[0], response_data)
    if execString:
        exec(execString)





