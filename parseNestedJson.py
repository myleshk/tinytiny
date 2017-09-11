import os
import json
import sys


class JsonParser:

    def __init__(self, data):
        if data and type(data) == dict:

            self.parseData(data)
        else:
            raise Exception("Invalid data")

    def parseData(self, data=None, level=0, prev_parents=[]):
        if not data:
            return False

        if type(data) == dict:
            pass
        elif type(data) == list:
            data = dict(zip(range(len(data)), data))
        else:
            return False

        for key in data:
            try:
                datum = data[key]
            except TypeError:
                print("TypeError: '{}', '{}'".format(data, key))
            parents = prev_parents + [key]
            if not (datum and self.parseData(datum, level + 1, parents)):
                print('{} = {}'.format("".join(map(lambda x: "[{}]".format("'{}'".format(x) if type(
                    x) is str else x), parents)), "'{}'".format(datum) if type(datum) is str else datum))
        return True

    def export(self):
        return self.data


def abort(err_msg):
    if err_msg:
        print(err_msg)
    exit()

if __name__ == "__main__":
    if sys.argv[1]:
        path = sys.argv[1]
    else:
        path = input('Enter path of json file:')
    path = os.path.abspath(path)
    path = path.strip()

    if not path.strip("/"):
        abort("Illegal path {}".format(path))

    # check if dir exists
    if not os.path.isfile(path):
        abort("File {} does not exist or is directory".format(path))

    # not we have a valid path
    with open(path, 'r+') as cms_f:
        data = json.load(cms_f)
        JsonParser(data)
