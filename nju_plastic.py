# 软院塑料云自动创建虚拟机脚本

import json
import string

import requests
import random

payload = json.loads(
    '{"availability_zone":"nova","admin_pass":"QWEqwe123","config_drive":false,"user_data":"","disk_config":"AUTO","instance_count":1,"name":"instance-111","profile":{},"security_groups":["f86678b5-f409-417a-84e0-96d93d40422e"],"unit":"H","new_ports":[],"source_id":"","flavor_id":"216","nics":[{"net-id":"f9645808-8e70-4811-b4f8-324bdf6eaf2f","subnet-id":"0e78e4bf-bf47-42be-9011-857e4f15ceeb"}],"key_name":null,"scheduler_hints":{},"new_volumes":[],"block_device_mapping_v2":[{"uuid":"e63d9aa4-3078-46c4-a124-be16c24c5daf","boot_index":0,"source_type":"image","volume_type":"hdd","volume_size":30,"destination_type":"volume","delete_on_termination":false}],"meta":{},"ecs_tags":[]}'
)

headers = {
    "Cookie": "xxx",
    "X-Csrftoken": "xxx",
    "X-Requested-With": "xxx",
}

machine_ids = []

for i in range(44, 44 + 8 + 1):
    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    payload["name"] = "devops-student-app-" + str(i)
    payload["admin_pass"] = password

    r = requests.post(
        "https://172.19.241.235/ecs/api/nova/servers/",
        json=payload,
        headers=headers,
        verify=False,
    ).json()[0]

    print(r)
    print(r["id"])
    machine_ids.append((r["id"], password))

machines = []

for i in machine_ids:
    while True:
        r = requests.get(
            "https://172.19.241.235/ecs/api/nova/servers/" + i[0] + "/",
            headers=headers,
            verify=False,
        ).json()
        print(r)
        if r["addresses"]:
            pri_ip = r["addresses"]["NUSI_Network"][0]["addr"]
            break

    machines.append(f"ssh root@{pri_ip} / Password: {i[1]}")

for i in machines:
    print(i)
