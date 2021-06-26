import configparser
import os


class Config_Util:
    def __init__(self, env):
        self.cf = configparser.ConfigParser()
        if "generate" in os.path.basename(os.getcwd()):
            self.cf.read("./configs/env.{}.configs".format(env))
        else:
            self.cf.read("../configs/env.{}.configs".format(env))

    def get_sections(self):
        return self.cf.sections()

    def get_section_dict(self, section):
        return self.cf.items(section)

    def get_property(self, section, key):
        return self.cf.get(section, key)










