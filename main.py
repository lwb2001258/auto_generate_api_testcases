import pytest


if __name__ == '__main__':
    pytest.main(['-q', 'tests/xxx_service/xxx_service_xxx-controller.py', "--test_env=qa", "--envFlag=normal"])
