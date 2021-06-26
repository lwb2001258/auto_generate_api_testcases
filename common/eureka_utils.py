from common.http_utils import *
import xml.etree.ElementTree as ET
from common.config_utils import Config_Util
from common import log_config


def get_service_url(service, env_flag="normal", env="qa"):
    cf = Config_Util(env)
    eureka_url = cf.get_property("eureka", "eureka_url").rstrip("/")
    res = execute_http(url="{}/eureka/apps/{}".format(eureka_url, service))
    root = ET.fromstring(res[0])
    url_dict = {}
    try:
        for elem in root.iter():
            if elem.tag == "instance":
                if elem.find("status").text == "UP":
                    if elem.find("metadata").find("envflag") is None:
                        url_dict["normal"] = "http://" + elem.find(
                            "hostName").text + ":" + elem.find("port").text + "/"
                    else:
                        url_dict[elem.find("metadata").find("envflag").text] = "http://" + elem.find("hostName").text + ":" + elem.find("port").text + "/"
    except Exception as e:
        logging.error("get eureka_url error, service is {}, env is {},errMsg is {}".format(service, env, e))
    service_url = url_dict.get(env_flag)
    if not service_url:
        if len(url_dict.values()) > 0:
            service_url = list(url_dict.values())[0]
        else:
            service_url = ""
    return service_url


def get_all_service(env="qa"):
    cf = Config_Util(env)
    eureka_url = cf.get_property("others", "eureka_url").rstrip("/")
    res = execute_http(url="{}/eureka/apps/".format(eureka_url))
    root = ET.fromstring(res[0])
    service_list = []
    try:
        for elem in root.iter():
            if elem.tag == "application":
                service_list.append(elem.find("name").text)
    except Exception as e:
        logging.error("get all eureka services error, env is {},errMsg is {}".format(env, e))
    return service_list
