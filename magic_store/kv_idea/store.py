import json
import uuid

from ..constants import MESSAGES

class Store:

    def __init__(self):
        self._store = {"__default__": {}}
        self._currentNamespace = None


    def createNamespace(self, namespace):
        if namespace == "__default__":
            return MESSAGES.INCORRECT_NAMESPACE

        self._store[namespace] = {}
        return MESSAGES.OK


    def put(self, key, value, *, namespace = None, guard = None):
        namespace = self._checkNamespace(namespace)

        if namespace == None:
            return MESSAGES.INCORRECT_NAMESPACE

        if not self._guardKVArgs(key, value):
            return MESSAGES.INCORRECT_TYPE

        if not (namespace in self._store):
            self._store[namespace] = {}
            #self._currentNamespace = namespace

        if key in self._store[namespace]:
            v = self._store[namespace][key]

            if v["guard"] == guard:
                v["guard"] = uuid.uuid4().hex
                v["value"] = value
            else:
                return MESSAGES.INCORRECT_GUARD
        else:
            self._store[namespace][key] = {"guard": uuid.uuid4().hex, "value": value}

        return MESSAGES.OK


    def get(self, key, *, namespace = None):
        namespace = self._checkNamespace(namespace)

        if namespace == None:
            return MESSAGES.INCORRECT_NAMESPACE

        if not(isinstance(key, str) and len(key)>0):
            return MESSAGES.INCORRECT_TYPE

        if not (namespace in self._store):
            return MESSAGES.INCORRECT_NAMESPACE

        if not (key in self._store[namespace]):
            return MESSAGES.INCORRECT_KEY

        value = None
        if isinstance(self._store[namespace][key]["value"], dict) or \
           isinstance(self._store[namespace][key]["value"], list):
            value = self._store[namespace][key]["value"].copy()
        else:
            value = self._store[namespace][key]["value"]

        return MESSAGES.ok(
            value,
            self._store[namespace][key]["guard"]
        )


    def delete(self, key, *, namespace = None, guard = None):
        namespace = self._checkNamespace(namespace)

        if namespace == None:
            return MESSAGES.INCORRECT_NAMESPACE

        if not(isinstance(key, str) and len(key)>0):
            return MESSAGES.INCORRECT_TYPE

        if not (namespace in self._store):
            return MESSAGES.INCORRECT_NAMESPACE

        if key in self._store[namespace]:
            v = self._store[namespace][key]

            if v["guard"] == guard:
                del self._store[namespace][key]
                return MESSAGES.OK
            else:
                return MESSAGES.INCORRECT_GUARD
        else:
            return MESSAGES.INCORRECT_KEY


    def save(self):
        file = open("db.json","w")
        json.dump(self._store, file)
        file.close()
        return MESSAGES.OK


    def load(self):
        file = open("db.json","r")
        self._store = json.load(file)
        file.close()
        return MESSAGES.OK


    def _checkNamespace(self, namespace):

        if namespace == "__default__":
            return None
        elif namespace == None:
            if not self._currentNamespace == None:
                return self._currentNamespace
            else:
                return "__default__"

        return namespace

    def _guardKVArgs(self, key, value):
        if isinstance(key, str) and len(key)>0:
            return True
        else:
            return False