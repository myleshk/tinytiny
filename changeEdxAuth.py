import os
import json
import sys
import configparser


class EdxAuthUpdater():

    mysql_host = None
    mysql_password = None
    mysql_user = None
    mongo_host = None
    mongo_user = None
    mongo_password = None
    mongo_ssl = None

    def __init__(self, config_path='config.ini'):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.mysql_host = config['DEFAULT']['mysql_host']
        self.mysql_password = config['DEFAULT']['mysql_password']
        self.mysql_user = config['DEFAULT']['mysql_user']
        self.mongo_host = config['DEFAULT']['mongo_host']
        self.mongo_user = config['DEFAULT']['mongo_user']
        self.mongo_password = config['DEFAULT']['mongo_password']
        self.mongo_ssl = config.getboolean('DEFAULT', 'mongo_ssl')

    def processFile(self, file_path):
        with open(file_path, 'r+') as fp:
            data = json.load(fp)
            new_data = self.update(data)

            fp.seek(0)
            json.dump(new_data, fp, indent=4)
            # print(json.dumps(new_data))
            fp.truncate()

    def update(self, data_dict):
        data_dict['DATABASES']['default']['HOST'] = self.mysql_host
        data_dict['DATABASES']['default']['PASSWORD'] = self.mysql_password
        data_dict['DATABASES']['default']['USER'] = self.mysql_user
        data_dict['DATABASES']['read_replica']['HOST'] = self.mysql_host
        data_dict['DATABASES']['read_replica']['PASSWORD'] = self.mysql_password
        data_dict['DATABASES']['read_replica']['USER'] = self.mysql_user
        data_dict['DATABASES']['student_module_history']['HOST'] = self.mysql_host
        data_dict['DATABASES']['student_module_history']['PASSWORD'] = self.mysql_password
        data_dict['DATABASES']['student_module_history']['USER'] = self.mysql_user
        data_dict['DOC_STORE_CONFIG']['host'][0] = self.mongo_host
        data_dict['DOC_STORE_CONFIG']['password'] = self.mongo_password
        data_dict['DOC_STORE_CONFIG']['ssl'] = self.mongo_ssl
        data_dict['DOC_STORE_CONFIG']['user'] = self.mongo_user
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][0]['DOC_STORE_CONFIG']['host'][0] = self.mongo_host
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][0]['DOC_STORE_CONFIG']['password'] = self.mongo_password
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][0]['DOC_STORE_CONFIG']['ssl'] = self.mongo_ssl
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][0]['DOC_STORE_CONFIG']['user'] = self.mongo_user
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][1]['DOC_STORE_CONFIG']['host'][0] = self.mongo_host
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][1]['DOC_STORE_CONFIG']['password'] = self.mongo_password
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][1]['DOC_STORE_CONFIG']['ssl'] = self.mongo_ssl
        data_dict['MODULESTORE']['default']['OPTIONS']['stores'][1]['DOC_STORE_CONFIG']['user'] = self.mongo_user
        data_dict['CONTENTSTORE']['DOC_STORE_CONFIG']['host'][0] = self.mongo_host
        data_dict['CONTENTSTORE']['DOC_STORE_CONFIG']['password'] = self.mongo_password
        data_dict['CONTENTSTORE']['DOC_STORE_CONFIG']['ssl'] = self.mongo_ssl
        data_dict['CONTENTSTORE']['DOC_STORE_CONFIG']['user'] = self.mongo_user
        data_dict['CONTENTSTORE']['OPTIONS']['host'][0] = self.mongo_host
        data_dict['CONTENTSTORE']['OPTIONS']['password'] = self.mongo_password
        data_dict['CONTENTSTORE']['OPTIONS']['ssl'] = self.mongo_ssl
        data_dict['CONTENTSTORE']['OPTIONS']['user'] = self.mongo_user

        return data_dict


def abort(err_msg):
    if err_msg:
        print(err_msg)
    exit()

if __name__ == "__main__":

    try:
        path = sys.argv[1]
    except IndexError:
        path = input(
            'Enter path of "edxapp" directory or leave empty for current directory: ')
    path = os.path.abspath(path)
    path = path.strip()

    if not path.strip("/"):
        abort("Illegal path {}".format(path))

    # check if dir exists
    if not os.path.isdir(path):
        abort("Path {} does not exist".format(path))

    # not we have a valid path
    # check if both lms.auth.json and cms.auth.json exist

    lms_auth_path = os.path.join(path, "lms.auth.json")
    cms_auth_path = os.path.join(path, "cms.auth.json")

    if os.path.isfile(lms_auth_path) and os.path.isfile(cms_auth_path):
        EAU = EdxAuthUpdater()
        EAU.processFile(lms_auth_path)
        EAU.processFile(cms_auth_path)
    else:
        abort("lms.auth.json / cms.auth.json not found at {}".format(path))
