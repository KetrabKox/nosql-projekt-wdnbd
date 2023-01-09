from magic_store.kv_idea.store import Store
from magic_store.constants import MESSAGES
from pathlib import Path

NAMESPACE = "KeyValueDb"

def initialDataBase(store):
    if not Path('db.json').is_file():
        store.save()

def resetDataBase():
    store = Store()
    store.save()

def createUser(store, key, user, namespace=NAMESPACE):
    result = store.get(key, namespace=namespace)

    if result["success"]:
        print("User key already exists")
        return
    else: 
        result = store.put(key, user, namespace=namespace)
        result = store.save()

def createFile(store, user, tags, file, namespace=NAMESPACE):
    result = store.get(user, namespace=namespace)

    if not result["success"]:
        print("User doesn't exist")
        return
    
    for tag in tags:
        data = store.get(user+"."+tag, namespace=namespace)
        if not data["success"]:
            result = store.put(user+"."+tag, [file], namespace=namespace)
        else:
            data["value"].append(file)
            store.put(user+"."+tag, data["value"], namespace=namespace, guard = data["guard"])
        
    result = store.save()
    
def deleteUser(store, user, namespace=NAMESPACE):
    result = store.get(user, namespace=namespace)

    if not result["success"]:
        print("User doesn't exist")
        return
    
    tags = []
    for key in store._store[namespace].keys():
        if key.split(".")[0] == user:
            tags.append(key)

    for tag in tags:
        data = store.get(tag, namespace=namespace)
        result = store.delete(tag, namespace=namespace, guard = data["guard"])
    
    result = store.save()

def searchFileFromTag(store, user, tags, namespace=NAMESPACE):
    print("files found: ")
    for tag in tags:
        data = store.get(user+"."+tag, namespace=namespace)
        if data["success"]:
            print(data)
        else:
            print("No files with tag: " + tag)

def searchFileFromAllTags(store, user, tags, namespace=NAMESPACE):
    files = {}

    for tag in tags:
        data = store.get(user+"."+tag, namespace=namespace)
        if data["success"]:
            for file in data["value"]:
                if file["name"] in files.keys():
                    files[file["name"]]["count"] += 1
                else:
                    files[file["name"]] =  {
                        "count": 1,
                        "info": file
                    }
    result = []
    for file in files.keys():
        if files[file]["count"] == len(tags):
            result.append(files[file]["info"])
    
    print("files found:",result)

def deleteTag(store, user, tag, namespace=NAMESPACE):
    result = store.get(user+"."+tag, namespace=namespace)
    if not result["success"]:
        print("Tag doesn't exist")
        return
    result = store.delete(user+"."+tag, namespace=namespace, guard = result["guard"])
    result = store.save()

if __name__ == '__main__':

    store = Store()    
    resetDataBase()
    initialDataBase(store)
    store.load()
    user1 = {
        "name": "John",
        "age": 25,
        "address": "New York",
        "phone": "1234567890",
        "email": "john25@gmail.com"
    }
    user2 = {
        "name": "Jane",
        "age": 30,
        "address": "London",
        "phone": "0987654321",
        "email": "jane30@gmail.com"
    }
    user3={
        "name":"Ola",
        "age": 22,
        "address": "Warsaw, Poland",
        "phone": "1234567890",
        "email": "ola22@gmail.com"
    }
    usermain ={
        "name":"Bartek",
        "age": 22,
        "address": "Lodz, Poland",
        "phone": "1234567890",
        "email": "bartek.firek@gmail.com"
    }
    
    createUser(store, "user1", user1)
    createUser(store, "user2", user2)
    createUser(store, "user3", user3)
    createUser(store,"usermain",usermain)

    file1 = {
        "name": "nosql1.txt"
    }

    file2 = {
        "name": "nosql2.txt"
    }

    file3 = {
        "name": "regrejsa.txt"
    }
    file_main = {
        "name": "projekt_Wdnbd.txt"
    }
    createFile(store, "usermain", ["nosql", "projekt"], file_main)
    createFile(store, "usermain", ["nosql", "prace domowe"], file1)
    createFile(store, "usermain", ["nosql", "prace domowe"], file2)
    createFile(store, "usermain", ["regresja", "prace domowe"], file3)
    createFile(store, "user1", ["nosql", "prace domowe"], file1)
    createFile(store, "user1", ["nosql", "prace domowe"], file2)
    createFile(store, "user1", ["regresja", "prace domowe"], file3)
    createFile(store, "user2", ["regresja", "prace domowe"], file3)
    createFile(store, "user3", ["nosql", "prace domowe"], file3)

    deleteUser(store, "user2")

    searchFileFromAllTags(store, "usermain", ["nosql", "prace domowe"])
    deleteTag(store, "user1", "regresja")