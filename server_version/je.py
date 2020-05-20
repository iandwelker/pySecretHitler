import json
import os
import time
import random

def lock():
    try: 
        open('.ed.lock', 'x')
        return True
    except:
        t=0
        while os.path.exists('.ed.lock'):
            time.sleep(0.1)
            t+=1
            if t == 20:
                return False
        else:
            open('.ed.lock', 'x')
            return True

def unlock():
    os.remove('.ed.lock')

def insert(key, val):
    lock()
    with open('stats.json', 'r+') as f:
        json_data = json.load(f)
        json_data[key] = val
        f.seek(0)
        f.write(json.dumps(json_data, indent=4, sort_keys=True))
        f.truncate()
    time.sleep(1)
    unlock()

# def getDeck():
#     with open('stats.json', 'r') as f:
#         json_data = json.load(f)
#         return json_data['deck']

# def getDiscard():
#     with open('stats.json', 'r') as f:
#         json_data = json.load(f)
#         return json_data['discard']

def threePolicies():
    lock()
    with open('stats.json', 'r+') as f:
        json_data = json.load(f)
        nums = []
        for i in range(3):
            numtoadd = random.randint(0, len(json_data['deck']) - 1)
            while numtoadd in nums:
                numtoadd = random.randint(0, len(json_data['deck']) - 1)
            else:
                # print(numtoadd)
                nums.append(numtoadd)

        nums.sort(reverse=True)
        # print(nums)
        to_return = []
        for i in nums:
            to_return+=json_data['deck'].pop(i)

        f.seek(0)
        f.write(json.dumps(json_data, indent=4, sort_keys=True))
        f.truncate()
    return to_return
    unlock()

def getValue(key):
    with open('stats.json', 'r') as f:
        json_data = json.load(f)
        return json_data[key]


# insert("last_action", "")
# print(threePolicies())
