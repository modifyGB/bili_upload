from upload import upload
import sys
import json

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ul = upload(json.loads(sys.argv[1]))
        ul.upload()
    else:
        print('你没有传配置文件')