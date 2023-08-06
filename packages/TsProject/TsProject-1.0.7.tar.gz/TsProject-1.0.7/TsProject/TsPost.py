# -*- coding: utf-8 -*-
# @Time : 2023/04/30 10:00
# @Author : Kqy
# @Version : 1.0.7
# @Website : https://www.tsginkgo.cn/

import os;
import json;
import requests;

global NowVersion, Use;
NowVersion = "1.0.7";

# Edit The Lambda
def TSFileUploadPost(FilePath=None, UploaderKey=None, Description=None):    # Def Post Lambda
    """
        你可以通过此函数来上传文件至云端
    """

    if (not Use):
        return {"code": -1, "error": '你需要更新到最新版本！'};
    
    if (not FilePath) or (not UploaderKey):
        return {"code": -1, "error": '文件地址与API KEY均必须填写！'};

    if (os.path.getsize(FilePath)>52428800):
        return {"code": -1, "error": f'文件{FilePath}超过最大大小限制50MB！'};

    UploadUrl = "https://www.tsginkgo.cn/file-uploader/api/upload/public/";

    try:
        data = {'UploaderKey': UploaderKey, 'Description': Description}; # Post Data
        files = {'file': open(FilePath, 'rb')};  # Post File
        res = requests.post(UploadUrl, data=data, files=files).text;    # Get Post  
        return json.loads(res);
        # return {"code": 0, "res": res};  # Return Result
    except Exception as e:
        return {"code": -1, "error": str(e)};

def VersionCheck():
    try:
        Req = requests.get("https://www.tsginkgo.cn/file-uploader/api/pypackage/NewVersion.json").text;
        Req = json.loads(Req);

        for items in Req:
            if items["Type"]=="Release":
                NewVersion = items["NewVersion"];
                DownloadCmd = items["DownloadCmd"];
                MoreUrl = items["MoreUrl"];
                Force = items["Force"];
                BeginColorRed = '\033[1;31m';
                BeginColorBlue = '\033[1;34m';
                EndColor = '\033[0m';
                if (NewVersion>NowVersion):
                    # print("Need Update");
                    print("-"*64);
                    print(f"{BeginColorRed}你的 TsProject 库需要更新！{EndColor}");
                    print(f"当前版本:{NowVersion}，最新版本:{NewVersion}");
                    if (Force):
                        print(f"{BeginColorRed}新版本为强制更新版本，你必须更新到最新版本才能继续使用{EndColor}");
                        print(f"你可以通过在终端使用'{BeginColorBlue}{DownloadCmd}{EndColor}'命令来获得更新");
                        print(f"在{MoreUrl}了解更多");
                        print("-"*64);
                        Use = False;
                        return False;
                    else:
                        print(f"{BeginColorBlue}新版本为不强制更新版本，你可以继续使用此旧版本{EndColor}");
                        print(f"你可以通过在终端使用'{BeginColorBlue}{DownloadCmd}{EndColor}'命令来获得更新");
                        print(f"在{MoreUrl}了解更多");
                        print("-"*64);
                        Use = True;
                        return True;
                else:
                    print("-"*64);
                    print(f"TsProject {BeginColorBlue}{NowVersion}{EndColor}");
                    print("-"*64);
                    Use = True;
                    return True;
    except Exception as error:
        print("-"*64);
        print(f"TsProject {BeginColorBlue}{NowVersion}   OFFLINE{EndColor}");
        print("-"*64);
        Use = True;
        return True;    

Use = VersionCheck();

if __name__ == "__main__":
    print(TSFileUploadPost());