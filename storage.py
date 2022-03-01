import argparse
import os
import tempfile
import json


parser = argparse.ArgumentParser()
parser.add_argument("--key")
parser.add_argument("--val")

args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

dictA = dict()

if args.key and args.val:
    if not os.path.exists(storage_path):
        with open(storage_path, 'w') as f:
            f.write(json.dumps(dictA))

    with open(storage_path, 'r') as f:
        dictA = json.loads(f.read())

    dictA[args.key] = dictA.get(args.key, list())
    dictA[args.key].append(args.val)

    with open(storage_path, 'w') as f:
        f.write(json.dumps(dictA))

elif args.key and not args.val:
    if os.path.exists(storage_path):
        with open(storage_path, 'r') as f:
            dictA = json.loads(f.read())
        print(*dictA.get(args.key, []), sep=', ')
    else:
        print(None)

