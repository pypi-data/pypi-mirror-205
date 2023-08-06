import requests
import json
import pandas as pd 
import getpass


class SDTcloud():
    def __init__(self):
        self.url = "http://25.10.133.65:31779"
        self.userId = input("ID: ")
        self.userPassword = getpass.getpass("PW: ")
        self.userToken = f"Bearer {self.login(self.userId, self.userPassword)}"

    # 로그인
    def login(self, 
            id: str, 
            pw: str
        ):
        "oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        param = {
            "grantType": "password",
            "email": id,
            "password": pw
        }
        
        response = requests.request('post',f"{self.url}/oauth/token", headers=headers, params=param)
        result = json.loads(response.content)
        return result["accessToken"]

    # 스토리지 등록
    def create_storage(self, name, tag):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.userToken
        }

        bodys = json.dumps({
            "name": name,
            "tag": tag
        })

        response = requests.request('post',f"{self.url}/stackbase/v1/storages", headers=headers, data=bodys)
        result = json.loads(response.content)
        return result
    
    # 스토리지 단건 정보 조회
    def get_storage(self):
        print("single get")
    
    # 유저의 스토리지 리스트 조회
    def list_storage(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.userToken
        }

        response = requests.request('get',f"{self.url}/stackbase/v1/storages", headers=headers)
        result = json.loads(response.content)
        
        df = pd.DataFrame(result)
        return df

    # 스토리지 정보 수정
    def update_storage(self):
        print("update")
    
    # 스토리지 삭제
    def delete_storage(self):
        print("delete")

    # 폴더 등록
    def create_folder(self, storageId, parentId, dirName):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.userToken
        }

        bodys = json.dumps({
            "parentId": parentId,
            "name": dirName,
            "storageId": storageId
        })

        response = requests.request('post',f"{self.url}/stackbase/v1/folder", headers=headers, data=bodys)
        result = json.loads(response.content)
        return result
    
    # 트리 검색
    def get_tree(self, storageId, parentId):
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.userToken
        }

        param = {
            "storageId": storageId,
            "parentId": parentId
        }

        response = requests.request('get',f"{self.url}/stackbase/v1/trees", headers=headers, params=param)
        result = json.loads(response.content)
        df = pd.DataFrame(result)
        return df

    # 폴더 수정
    def update_folder(self):
        print("update")

    # 폴더 삭제
    def delete_folder(self):
        print("delete")

    # 컨텐츠 조회
    def get_content(self):
        print("get")

    # 컨텐츠 수정
    def update_content(self):
        print("test")
    
    # 컨텐츠 삭제
    def delete_content(self):
        print("test")

    # 컨텐츠 다운로드
    def fget_content(self, fileId):
        
        headers = {
            "Authorization": self.userToken
        }

        response = requests.request('get',f"{self.url}/stackbase/v1/contents/download/{fileId}", headers=headers)
        result = json.loads(response.content)
        return result
    
    # 컨텐츠 등록
    def fput_content(self):
        print("fput")
        

# print("Login")
# sdt_client = SDTcloud()

# # print("get List of storage")
# # sdt_client.get_storage()

# # print("create storage")
# # sdt_client.create_storage("storage-test", "123,2,3")

# # print("get List of storage")
# # sdt_client.get_storage()

# # print("create folder")
# # sdt_client.create_folder("5c0ab969-0397-45e8-8d97-b6fc20496a16", "", "sdtcloud-test")

# # print("get List of tree")
# # print(sdt_client.get_tree("5c0ab969-0397-45e8-8d97-b6fc20496a16", ""))

# print("get List of tree")
# sdt_client.get_tree("5c0ab969-0397-45e8-8d97-b6fc20496a16", "57d77d33-913f-4932-95a8-ea15b0de812e")