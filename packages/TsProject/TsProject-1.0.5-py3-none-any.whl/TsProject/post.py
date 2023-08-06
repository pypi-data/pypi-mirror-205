# -*- coding: utf-8 -*-
# @Time : 2023/04/29 16:12
# @Author : Kqy
# @Version : 1.0.5
# @Website : https://www.tsginkgo.cn/


import os
import requests

# Edit The Lambda
def TSFileUploadPost(FilePath=None, UploaderKey=None, Description=None):    # Def Post Lambda
    """
        你可以通过此函数来上传文件至云端
    """
    if (os.path.getsize(FilePath)>52428800):
        return {"code": -1, "error": f'文件{FilePath}超过最大大小限制50MB！'};

    UploadUrl = "https://www.tsginkgo.cn/file-uploader/api/upload/public/";

    try:
        data = {'UploaderKey': UploaderKey, 'Description': Description}; # Post Data
        files = {'file': open(FilePath, 'rb')};  # Post File
        res = requests.post(UploadUrl, data=data, files=files).text;    # Get Post  
        return {"code": 0, "res": res};  # Return Result
    except Exception as e:
        return {"code": -1, "error": str(e)};

# if __name__ == "__main__":
    # TSFileUploadPost();