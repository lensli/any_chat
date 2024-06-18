import json

any = ""
logo_name = "多模态大模型"
logo_favicon_path = "modules/customer/dlm/favicon.ico"


any_icon_512 = "modules/customer/dlm/any-icon-512.png"
mask_icon_512 = "modules/customer/dlm/mask-icon-512.png"
bot_avatar_path = "modules/customer/dlm/robot-256.png"
user_avatar_path = "modules/customer/dlm/user_256.png"

coin_name = "金币"


def update_json(path,data):

    # 定义要修改的键值对
    changes = data

    # 指定JSON文件的路径
    json_file_path = path

    # 读取JSON文件
    with open(json_file_path, 'r',encoding="utf-8") as file:
        data = json.load(file)

    # 修改JSON数据
    data.update(changes)

    # 将修改后的数据写回文件
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print("JSON file has been updated.")

import sys
from .lifen_comn import get_current_pyfileabspath,abs_path2relative_path
abs_pyfile = get_current_pyfileabspath()
manifest_json_path = abs_path2relative_path(abs_pyfile,"..\\..\\web_assets\\manifest.json")
data = {
    "name": logo_name,
    "short_name": logo_name,
    "icons": [
        {
            "src": f"/file={any_icon_512}",
            "type": "image/png",
            "sizes": "512x512",
            "purpose": "maskable"
        },
        {
            "src": f"/file={mask_icon_512}",
            "type": "image/png",
            "sizes": "512x512",
            "purpose": "any"
        }
    ]

}
update_json(manifest_json_path,data)

config_json_path = abs_path2relative_path(abs_pyfile,"..\\..\\config.json")

data = {
    "bot_avatar": bot_avatar_path, 
    "user_avatar": user_avatar_path
}
update_json(config_json_path,data)


