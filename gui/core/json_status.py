import json
import os


class Status(object):
    # APP PATH
    # ///////////////////////////////////////////////////////////////
    json_file = "resources\status.json"
    app_path = os.path.abspath(os.getcwd())
    status_path = os.path.normpath(os.path.join(app_path, json_file))
    if not os.path.isfile(status_path):
        print(f"WARNING: \"status.json\" not found! check in the folder {status_path}")

    def __init__(self):
        super(Status, self).__init__()

        self.items = {}

        self.deserialize()

    def serialize(self):
        # WRITE JSON FILE
        with open(self.status_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    def deserialize(self):
        # READ JSON FILE
        with open(self.status_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings