import json
import storage

storage.remount("/", False)

with open("/data.json", 'w') as file:
    file.write(json.dumps({"odometer": 0.0}))