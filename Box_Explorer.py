import json
import requests
import re
import os
import time
import shutil
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    # 'http': 'http://127.0.0.1:8888',
    # 'https': 'http://127.0.0.1:8888'
}

# 진입점


def Get_File_List(Essential_Information: dict):

    # 자료를 담는 클래스 선언 및 z값 세팅
    Box_Explorer_Class = All_File_List(Essential_Information)

    # 라이브 메타데이터 가져오기
    Box_Explorer_Class.get_file_list()

    # 휴지통 메타데이터 가져오기
    Box_Explorer_Class.RB_get_file_list()

    return Box_Explorer_Class


class Jsondata:
    def __init__(self):
        self.itemcount = 0
        self.lencount = 0
        self.jsondata = {}


class RB_Jsondata:

    def __init__(self):
        self.pageCount = 0
        self.pageNumber = 0
        self.jsondata = {}


class Meta_data:
    def __init__(self):
        self.Count = 0
        self.name = ""
        self.fid = ""
        self.path = ""
        self.size = 0
        self.is_shared = "No"
        self.is_trashed = "No"
        self.trashed_at = ""
        self.server_ctime = ""
        self.content_ctime = ""
        self.server_mtime = ""
        self.lastmod_user = ""
        self.version_count = 0
        self.version_num = 0
        self.extension = ""
        self.owner = ""
        self.sha1 = ""
        self.sharedlink = ""
        self.collabo_name = []
        self.collabo_email = []
        self.durl = ""
        self.contentUpdated = ""
        self.comment_count = 0
        self.thumbnail = ""
        self.note_flag = 0


class RB_Meta_data:
    def __init__(self):
        self.count = 0
        self.is_trashed = "Yes"
        self.typedID = ""
        self.type = ""
        self.id = ""
        self.description = ""
        self.date = ""
        self.extension = ""
        self.name = ""
        self.itemSize = ""
        self.parentFolderID = ""
        self.created = ""
        self.contentUpdated = ""
        self.deleted = ""
        self.filesCount = ""
        self.isExternallyOwned = ""
        self.deletedBy = ""
        self.deletedFromTrash = ""
        self.lastUpdatedByName = ""
        self.isSelfOrAncestorCollaborated = ""
        self.versionCount = ""
        self.ownerName = ""
        self.ownerEnterpriseName = ""
        self.ownerEnterpriseID = ""
        self.contentCreated = ""
        self.isBox3DPackageSupported = ""
        self.durl = ""

        self.iconType = ""
        self.isRetained = ""
        self.isRetainedUntil = ""
        self.isRetainedByPolicyType = ""
        self.canDelete = ""
        self.canRestore = ""


class All_File_List:
    def __init__(self, Essential_Information):

        # 쿠키 값 세팅
        self.z = {'z': Essential_Information['z']}
        self.uid = {'uid': Essential_Information['uid']}

        # 파일 리스트 정보를 담을 리스트 선언
        self.Global_file_index = 0
        self.RB_Global_file_index = 0
        self.Global_file_list = []
        self.RB_Global_file_list = []

        # 폴더 생성
        self.initDirPath = ".\Box"
        if not os.path.exists(self.initDirPath):
            os.makedirs(self.initDirPath)

        for category in [".downloads", ".thumbnail", ".history"]:
            subPATH = os.path.join(self.initDirPath, category)
            if not os.path.exists(subPATH):
                os.makedirs(subPATH)
            else:
                shutil.rmtree(subPATH)
                os.makedirs(subPATH)

    def get_file_list(self):
        requestURL = "https://app.box.com/folder/0"

        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)

        # 버전 구하는 용도로 받아둠
        self.request_token = re.search(
            ',\"requestToken\":\"(.+?)\",\"billing\":{', responseData.text).group(1)

        Box_Poststream_Data = responseData.text.split(
            "Box.postStreamData = ")[1]
        Box_Poststream_Data = Box_Poststream_Data.split(";")[0]

        path = "All Files"
        root = "/app-api/enduserapp/folder/0"
        file_list = self.parsing_file_list(root, Box_Poststream_Data)
        folder_list = Jsondata()

        while file_list.itemcount > file_list.lencount:
            url = "https://app.box.com/app-api/enduserapp/folder/0?itemOffset=" + \
                str(file_list.lencount - 1)
            file_list.jsondata = self.next_page(url, root, file_list)
            file_list.lencount = len(
                file_list.jsondata["/app-api/enduserapp/folder/0"]["items"])

        print("★ Root 총 파일, 폴더 수: " + str(file_list.lencount) + "\n")

        for element in file_list.jsondata[root]["items"]:
            if element["type"] == "folder":
                self.check_type(element, path)
            else:
                self.get_metadata(element, path)

    def parsing_file_list(self, root, Box_Poststream_Data):
        element_list = Jsondata()
        element_list.jsondata = json.loads(Box_Poststream_Data)
        element_list.itemcount = element_list.jsondata[root]["folderItemCount"]
        element_list.lencount = len(element_list.jsondata[root]["items"])

        return element_list

    def next_page(self, url, root, element_list):
        requestURL = url

        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)

        new_jsondata = json.loads(responseData.content)
        len_jsondata = len(new_jsondata["items"])

        jsondata_root_items = element_list.jsondata[root]["items"]

        for i in range(len_jsondata):
            jsondata_root_items.append(new_jsondata["items"][i])

        element_list.jsondata[root]["items"] = jsondata_root_items

        return element_list.jsondata

    def check_type(self, i, path):  # i : 각 파일
        folder_list = Jsondata()

        if i["type"] == "folder":
            url = "https://app.box.com/folder/" + str(i["id"])
            root = "/app-api/enduserapp/folder/" + str(i["id"])
            folder_list = self.folder_file_list(url, root)

            while folder_list.itemcount > folder_list.lencount:
                url2 = "https://app.box.com/app-api/enduserapp/folder/" + \
                    str(i["id"]) + "?itemOffset=" + str(folder_list.lencount)
                folder_list.jsondata = self.next_page(url2, root, folder_list)
                folder_list.lencount = len(folder_list.jsondata[root]["items"])

            # 서브 폴더 경로는 배열의 합으로 구해진다.
            subpath = ""
            for node in folder_list.jsondata[root]["folder"]["path"]:
                subpath = os.path.join(subpath, node["name"])
            print(subpath)

            for element in folder_list.jsondata[root]["items"]:
                self.check_type(element, subpath)

        else:
            self.get_metadata(i, path)

        return folder_list

    # sidebar, meta, collabo, get_thumbnail
    def get_metadata(self, i, _path):
        meta_json = self.sidebar(i["id"])
        meta_json.path = _path
        meta_json.lastmod_user = i["lastUpdatedByName"]
        meta_json.version_num = meta_json.version_count
        meta_json = self.meta(meta_json.fid, meta_json)

        if meta_json.sharedlink != "":
            meta_json.is_shared = "YES"
            meta_json = self.collabo(meta_json.fid, meta_json)
        else:
            meta_json.collabo_name.append("")
            meta_json.collabo_email.append("")

        self.get_thumbnail(meta_json.fid, meta_json.name,
                           meta_json.thumbnail)

        self.Global_file_index += 1
        meta_json.Count += self.Global_file_index

        if meta_json.extension == "boxnote":
            meta_json.note_flag = 1

        print("★ Count :", self.Global_file_index,
              f"(현재 ver {meta_json.version_count} )")
        self.Global_file_list.append(meta_json)

        # 버전 탐색
        if meta_json.version_count != 1 and meta_json.note_flag == 0:
            self.get_version(i, meta_json.path, meta_json.version_count)

        # self.File_WriteLine(meta_json)

    def get_version(self, i, path, version_count):

        requestURL = "https://app.box.com/app-api/enduserapp/elements/tokens"

        header = {
            "X-Request-Token": self.request_token
        }

        data = "{\"fileIDs\":[" + str(i["id"]) + "]}"

        temp = ""
        downloadtoken = ""

        responseData = requests.post(
            url=requestURL, headers=header, data=data, cookies=self.z, proxies=proxies, verify=False)

        tokenJson = json.loads(responseData.content)

        historyRoot = str(i["id"])
        historyToken = "Bearer " + tokenJson[historyRoot]["read"]
        stream = "/versions?offset=0&limit=1000&fields=authenticated_download_url,created_at,extension,is_download_available,modified_at,modified_by,name,permissions,restored_at,restored_by,retention,size,trashed_at,trashed_by,uploader_display_name,version_number"
        requestURL2 = "https://api.box.com/2.0/files/" + historyRoot + stream

        header2 = {
            "Authorization": historyToken
        }

        responseData2 = requests.get(
            url=requestURL2, headers=header2, cookies=self.z, proxies=proxies, verify=False)
        vinfojson = json.loads(responseData2.content)

        if vinfojson.get("code") == "forbidden":
            print("해당 계정의 권한으로 파일(현재 ver" + str(version_count) +
                  ")의 하위 버전을 탐색할 수 없습니다. status : 403\n")
            return

        fix_count = self.Global_file_index

        for vcount in range(len(vinfojson["entries"])):
            vmeta_json = Meta_data()

            vmeta_json.Count += self.Global_file_index
            vmeta_json.name = vinfojson["entries"][vcount]["name"]
            vmeta_json.fid = vinfojson["entries"][vcount]["id"]
            vmeta_json.path = path
            vmeta_json.size = vinfojson["entries"][vcount]["size"]
            vmeta_json.trashed_at = vinfojson["entries"][vcount]["trashed_at"]
            # utc
            vmeta_json.server_ctime = vinfojson["entries"][vcount]["created_at"]
            # utc
            vmeta_json.server_mtime = vinfojson["entries"][vcount]["modified_at"]
            vmeta_json.lastmod_user = vinfojson["entries"][vcount]["modified_by"]["login"]
            vmeta_json.version_count = version_count
            vmeta_json.version_num = vinfojson["entries"][vcount]["version_number"]
            vmeta_json.extension = vinfojson["entries"][vcount]["extension"]
            vmeta_json.owner = vinfojson["entries"][vcount]["uploader_display_name"]

            temp = tokenJson[historyRoot]["read"]
            downloadtoken = "1%21" + temp[2:len(temp)]
            vmeta_json.durl = "https://public.boxcloud.com/api/2.0/files/" + \
                str(i["id"]) + "/content?access_token=" + \
                downloadtoken + "&version=" + str(vmeta_json.fid)

            if vinfojson["entries"][vcount]["trashed_at"] != "":
                vmeta_json.is_trashed = "YES"

            print("★ Count : " + str(self.Global_file_index) + " (Count " +
                  str(fix_count) + "의 하위 ver" + str(vmeta_json.version_num) + ")")

            self.Global_file_list.append(vmeta_json)

            # self.File_WriteLine(vmeta_json)

    def folder_file_list(self, url, root):
        element_list = Jsondata()
        requestURL = url
        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)

        self.request_token = re.search(
            ',\"requestToken\":\"(.+?)\",\"billing\":{', responseData.text).group(1)

        Box_Poststream_Data = responseData.text.split(
            "Box.postStreamData = ")[1]

        Box_Poststream_Data = Box_Poststream_Data.split(";")[0]

        element_list = self.parsing_file_list(root, Box_Poststream_Data)

        return element_list

    def sidebar(self, fid):
        meta = Meta_data()
        requestURL = "https://app.box.com/app-api/enduserapp/file/" + \
            str(fid) + "/sidebar"
        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)
        sidejson = json.loads(responseData.content)

        for i in range(len(sidejson["items"])):
            meta.name = sidejson["items"][i]["name"]
            meta.fid = fid
            meta.size = sidejson["items"][i]["itemSize"]
            meta.server_ctime = sidejson["items"][i]["created"]
            meta.content_ctime = sidejson["items"][i]["contentCreated"]
            meta.contentUpdated = sidejson["items"][i]["contentUpdated"]
            meta.version_count = sidejson["items"][i]["versionCount"] + 1
            meta.owner = sidejson["items"][i]["ownerName"]
            meta.extension = sidejson["items"][i]["extension"]
            meta.comment_count = sidejson["items"][i]["commentsCount"]

            if sidejson["items"][i]["thumbnailURLs"] == "None":
                meta.thumbnail = ""
            else:
                meta.thumbnail = sidejson["items"][i]["thumbnailURLs"]["large"]

        return meta

    def get_thumbnail(self, fid, fname, thumbnail):

        if thumbnail is not None:
            thumbnailURL = "https://app.box.com" + \
                thumbnail.split("thumb_320.jpg")[0] + "thumb_1024.jpg"

            responseData = requests.get(
                url=thumbnailURL, cookies=self.z, proxies=proxies, verify=False)
            filePATH = os.path.join(
                self.initDirPath, ".thumbnail", str(fid) + ".jpg")

            f = open(filePATH, 'wb')
            f.write(responseData.content)

    def meta(self, fid, meta_json):
        requestURL = "https://app.box.com/index.php?fileIDs[]=" + \
            str(fid) + "&rm=preview_get_files_metadata"

        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)
        metajson = json.loads(responseData.content)
        meta_json.sharedlink = metajson["filesMetadata"][0]["shared_link"]
        meta_json.sha1 = metajson["filesMetadata"][0]["sha1"]

        return meta_json

    def collabo(self, fid, meta_json):
        requestURL = "https://app.box.com/file/" + str(fid) + "/collaborators"

        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)

        Box_Poststream_Data = responseData.text.split(
            "Box.postStreamData = ")[1]
        Box_Poststream_Data = Box_Poststream_Data.split(";")[0]

        collaboJson = json.loads(Box_Poststream_Data)
        root = "/app-api/enduserapp/item/f_" + str(fid) + "/collaborators"

        for users in range(len(collaboJson[root]["collaborators"])):
            meta_json.collabo_name.append(
                collaboJson[root]["collaborators"][users]["name"])
            meta_json.collabo_email.append(
                collaboJson[root]["collaborators"][users]["email"])

        return meta_json

    # 휴지통 영역

    def RB_get_file_list(self):
        requestURL = "https://app.box.com/trash"
        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)

        Box_prefetched_Data = responseData.text.split(
            "Box.prefetchedData = ")[1]
        Box_prefetched_Data = Box_prefetched_Data.split(';')[0]

        RB_root = "/app-api/enduserapp/trash"
        RB_file_list = self.RB_parsing_file_list(RB_root, Box_prefetched_Data)
        RB_file_list.pageNumber += 1

        while RB_file_list.pageNumber <= RB_file_list.pageCount:
            url = "https://app.box.com/app-api/enduserapp/trash?page=" + \
                str(RB_file_list.pageNumber)
            RB_file_list.jsondata = self.RB_next_page(
                url, RB_root, RB_file_list)
            RB_file_list.pageNumber += 1

        for element in RB_file_list.jsondata[RB_root]["items"]:
            self.RB_get_metadata(element)

    def RB_parsing_file_list(self, root, Box_prefetched_Data):
        element_list = RB_Jsondata()
        element_list.jsondata = json.loads(Box_prefetched_Data)
        element_list.pageNumber = element_list.jsondata[root]["pageNumber"]
        element_list.pageCount = element_list.jsondata[root]["pageCount"]
        return element_list

    def RB_next_page(self, url, root, element_list):
        requestURL = url
        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)

        new_jsondata = json.loads(responseData.content)
        len_jsondata = len(new_jsondata["items"])
        jsondata_root_items = element_list.jsondata[root]["items"]

        for i in range(len_jsondata):
            jsondata_root_items.append(new_jsondata["items"][i])

        element_list.jsondata[root]["items"] = jsondata_root_items
        return element_list.jsondata

    def RB_get_metadata(self, i):  # i는 휴지통 각 파일
        meta_json = self.RB_sidebar(i["id"], i)
        meta_json.iconType = i["iconType"]
        meta_json.isRetained = i["isRetained"]
        meta_json.isRetainedUntil = i["isRetainedUntil"]
        meta_json.isRetainedByPolicyType = i["isRetainedByPolicyType"]
        meta_json.canDelete = i["canDelete"]
        meta_json.canRestore = i["canRestore"]
        meta_json.durl = "https://app.box.com/index.php?" + \
            "rm=box_v2_download_file&" + "file_id=" + str(i["id"])
        self.RB_Global_file_list.append(meta_json)

        print("★ 휴지통 Count :", self.RB_Global_file_index)
        self.RB_Global_file_index += 1

    def RB_sidebar(self, fid, item):
        meta = RB_Meta_data()
        meta.count = self.RB_Global_file_index
        temp = ""

        if str(item["type"]) == "folder":
            temp = "https://app.box.com/app-api/enduserapp/folder/"
        else:
            temp = "https://app.box.com/app-api/enduserapp/file/"

        requestURL = temp + str(fid) + "/sidebar?format=trash"
        responseData = requests.get(
            url=requestURL, cookies=self.z, proxies=proxies, verify=False)
        sidejson = json.loads(responseData.content)

        for i in range(len(sidejson["items"])):
            meta.typedID = sidejson["items"][i]["typedID"]
            meta.type = sidejson["items"][i]["type"]
            meta.id = sidejson["items"][i]["id"]
            meta.description = sidejson["items"][i]["description"]
            meta.date = sidejson["items"][i]["date"]
            meta.extension = sidejson["items"][i]["extension"]
            meta.name = sidejson["items"][i]["name"]
            meta.itemSize = sidejson["items"][i]["itemSize"]
            meta.parentFolderID = sidejson["items"][i]["parentFolderID"]
            meta.created = sidejson["items"][i]["created"]
            meta.contentUpdated = sidejson["items"][i]["contentUpdated"]
            meta.deleted = sidejson["items"][i]["deleted"]
            meta.filesCount = sidejson["items"][i]["filesCount"]
            meta.isExternallyOwned = sidejson["items"][i]["isExternallyOwned"]
            meta.deletedBy = sidejson["items"][i]["deletedBy"]
            meta.deletedFromTrash = sidejson["items"][i]["deletedFromTrash"]
            meta.lastUpdatedByName = sidejson["items"][i]["lastUpdatedByName"]
            meta.isSelfOrAncestorCollaborated = sidejson["items"][i]["isSelfOrAncestorCollaborated"]
            meta.versionCount = sidejson["items"][i]["versionCount"] + 1
            meta.ownerName = sidejson["items"][i]["ownerName"]
            meta.ownerEnterpriseName = sidejson["items"][i]["ownerEnterpriseName"]
            meta.ownerEnterpriseID = sidejson["items"][i]["ownerEnterpriseID"]
            meta.contentCreated = sidejson["items"][i].get("contentCreated")
            meta.isBox3DPackageSupported = sidejson["items"][i].get(
                "isBox3DPackageSupported")

        return meta
