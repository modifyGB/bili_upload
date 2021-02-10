from upload import upload
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1],'r+',encoding='utf-8') as file:
            ul = upload(json.loads(file.read()))
            ul.upload()
    else:
        print('你没有传配置文件')