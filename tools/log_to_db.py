import json


def write(file_name: str, data) -> bool:
    file_name = file_name.replace("http:", "").replace("https:", "").replace("/", "-")
    try:
        with open("data/" + file_name + ".json", "w") as f:
            f.write(json.dumps(data))
        return True
    except Exception as e:
        with open("errors.txt", 'a') as f:
            f.write("\n\n\n" + str(e))
        return False
