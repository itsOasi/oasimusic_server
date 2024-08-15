from math import sqrt
import random, os, json


LOGS = []
LOG_LVLS = ["SYSTEM", "LOG", "WARN", "ERROR"]
SUPPRESSED = [0]
def log(msg):
    log = f"LOG: {msg}"
    LOGS.append(log)
    print_log(log, 1)

def log_lvl(msg, lvl=0):
    log = f"{LOG_LVLS[lvl]}: {msg}"
    LOGS.append(log)
    print_log(log, lvl)

def print_log(log, lvl):
    if not lvl in SUPPRESSED:
        print(log)

def print_logs(limit = 5):
    display = LOGS[-limit:]
    string = ""
    for item in display:
        string += f"{item}\n"
    return string

def is_same_type(a, b):
    """
        checks to see if a and b are the same type
    """
    return type(a).__name__ == type(b).__name__

def read_file(path, args="r"):
    """
        gathers data from file at path
    """
    data = []
    f = open(path, args)
    data = f.read()
    f.close()
    log("file data loaded")
    return data

def write_file(path, data, args="w"):
    """
        writes data to file at path
    """
    f = open(path, args)
    f.write(data)
    f.close()
    log("data written")

def read_dir(path):
    return os.listdir(path)

def json_to_dict(path):
    return json.loads(read_file(path))

def dict_to_json(data):
    return json.dumps(data)
    
def dict_to_json_path(path, data):
    write_file(path, json.dumps(data))

def dyn_import(module_name):
    # https://www.geeksforgeeks.org/how-to-dynamically-load-modules-or-classes-in-python/
    module = __import__(module_name)
    return module

def del_file(path):
    os.remove(path)
    log(f"file deleted: {path}")
    
def generate_id(prefix):
    """
        generates an id with a given prefix
    """
    if not is_same_type(prefix, "hi"):
        prefix = "ID" # uses default prefix if invalid data is presented
    return prefix+str(random.randrange(111111, 999999))

def get_dist(pos1, pos2):
        '''
            gets distance between position 1 and position 2 using the a2 + b2 = c2
            but with a list of terms
        '''
        c2 = 0 # hypotenuse sqrd
        print(pos1, pos2)
        for axis in range(len(pos1)):
            c2 += (pos2[axis] - pos1[axis])**2 # calculates the terms
        hyp = sqrt(c2) # gets hypotenuse length
        print("distance between vectors", hyp)
        return hyp

def is_in_slots(query, obj):
    log_lvl(f"{obj.get_name()}: {obj.__slots__}", 0)
    return query in obj.__slots__
        
def call_if_in_slots(query, obj, kwargs):
    log_lvl(f"{obj.get_name()}: {obj.__slots__}", 0)
    if is_in_slots(query, obj):
        try:
            eval(f"obj.{query}({kwargs})")
        except Exception as e:
            return False

def cmd(str):
    os.system(str)