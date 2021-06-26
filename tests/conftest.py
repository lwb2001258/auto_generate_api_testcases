import pytest


def pytest_addoption(parser):
    parser.addoption("--test_env", action="store", default="qa",
                     dest='test_env', help="my option: qa or dev or prod")
    parser.addoption("--envFlag", action="store", default="normal",
                     dest='envFlag', help="envFlag of service")


@pytest.fixture(scope="session")
def environment(request):
    test_env = request.config.getoption('test_env')
    return test_env if test_env else "qa"


@pytest.fixture(scope="session")
def envFlag(request):
    envFlag_tag = request.config.getoption("envFlag")
    return envFlag_tag if envFlag_tag else "normal"




