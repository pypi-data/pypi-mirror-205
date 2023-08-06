import json
import sys

def split_class_path(class_path: str) -> tuple[str, str]:

    package_name = '.'.join(class_path.split('.')[:-1])
    class_name = class_path.split('.')[-1]

    return package_name, class_name

def jsonFile2Dict(jsonFile: str) -> tuple[int, dict]:

  try:
    f = open(jsonFile)
    data = json.load(f)
  except FileNotFoundError as e:
    return -1, dict(error="JsonFile is not found : {}".format(jsonFile))
  except json.decoder.JSONDecodeError as e:
    return -2, dict(error="JSONDecodeError occured : {}".format(sys.exc_info()[1]))
  
  return 1, data

class SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance