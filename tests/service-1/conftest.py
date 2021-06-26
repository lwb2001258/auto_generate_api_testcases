from common.data_provider import *


def step1UsingPOST_1_json_data(env):
    return get_json_data_from_es("tests/service-1/test_service_1_controller_1-controller.py::test_step1UsingPOST_1", env)


def step2UsingPOST_json_data(env):
    return get_json_data_from_es("tests/service-1/test_service-1_controller_1-asset-controller.py::test_step2UsingPOST", env)


def step3UsingPOST_json_data(env):
    return get_json_data_from_es("tests/service-1/test_service_1—controller_1-controller.py::test_step3POST", env)


def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == 'test_step1UsingPOST_1':
        test_data = step1UsingPOST_1_json_data(metafunc.config.getoption('test_env'))
        metafunc.parametrize("test_data", test_data)
    if metafunc.function.__name__ == 'test_step2UsingPOST':
        test_data = step1UsingPOST_1_json_data(metafunc.config.getoption('test_env'))
        metafunc.parametrize("test_data", test_data)
    if metafunc.function.__name__ == 'test_step3POST':
        test_data = step1UsingPOST_1_json_data(metafunc.config.getoption('test_env'))
        metafunc.parametrize("test_data", test_data)