import os
import requests
from datetime import datetime, timedelta
import Box_Search
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    # 'http': 'http://127.0.0.1:8888',
    # 'https': 'http://127.0.0.1:8888'
}


def Forensic_Menu(Box_MetaSet):
    os.system('cls')

    while(True):

        print("\n\n수집 메뉴를 선택해주세요.")
        print("0. 종료")
        print("1. 파일 메타데이터 보기 (Live)")
        print("2. 파일 메타데이터 보기 (Trash)")
        print("3. 파일 다운로드 (Live)")
        print("4. 파일 다운로드 (Trash)")
        print("5. 파일 히스토리 수집 (Live)")
        print("6. 검색")

        selectMenu = input("\n선택: ")

        if selectMenu not in ["0", "1", "2", "3", "4", "5", "6"]:
            print("\n잘못된 입력입니다. 다시 입력해주세요. (0 ~ 6)")
            continue

        if selectMenu == "0":
            exit(0)

        elif selectMenu == "1":
            Box_Show(Box_MetaSet.Global_file_list)

        elif selectMenu == "2":
            Box_RB_Show(Box_MetaSet.RB_Global_file_list)

        elif selectMenu == "3":
            Box_Export(Box_MetaSet)

        elif selectMenu == "4":
            Box_RB_Export(Box_MetaSet)

        elif selectMenu == "5":
            Box_History(Box_MetaSet)

        elif selectMenu == "6":
            Box_Search.Start(Box_MetaSet)


def Box_Show(MetaSet):
    for file in MetaSet:
        File_WriteLine(file)


def File_WriteLine(meta_json):
    print("-" * 50)
    print("★ Count : " + str(meta_json.Count))
    print("★ name : " + str(meta_json.name))
    print("★ fid : " + str(meta_json.fid))
    print("★ path : " + str(meta_json.path))
    print("★ size : " + str(meta_json.size) + " Byte")
    print("★ is_shared : " + str(meta_json.is_shared))
    print("★ is_trashed : " + str(meta_json.is_trashed))
    print("★ trashed_at : " + str(meta_json.trashed_at))

    if meta_json.durl != "":
        server_ctime = VTime_Convert(meta_json.server_ctime)
    else:
        server_ctime = Time_Convert(meta_json.server_ctime)
    print("★ server_ctime : " + server_ctime)  # utc

    print("★ content_ctime : " + Time_Convert(str(meta_json.content_ctime)))  # utc
    print("★ server_mtime : " + VTime_Convert(str(meta_json.server_mtime)))  # utc
    print("★ lastmod_user : " + str(meta_json.lastmod_user))
    print("★ version_count : " + str(meta_json.version_count))
    print("★ version_num : " + str(meta_json.version_num))
    print("★ extension : " + str(meta_json.extension))
    print("★ owner : " + str(meta_json.owner))
    print("★ sha1 : " + str(meta_json.sha1))
    print("★ collabo name:", str(meta_json.collabo_name))
    print("★ collabo email:", str(meta_json.collabo_email))
    print("★ durl : " + str(meta_json.durl))
    print("\n\n")


def Box_RB_Show(MetaSet):
    for RB_file in MetaSet:
        RB_File_WriteLine(RB_file)


def RB_File_WriteLine(meta_json):
    print("-" * 50)
    print("★ count : " + str(meta_json.count))
    print("★ is_trashed : " + str(meta_json.is_trashed))
    print("★ typedID : " + str(meta_json.typedID))
    print("★ type : " + str(meta_json.type))
    print("★ id : " + str(meta_json.id))
    print("★ description : " + str(meta_json.description))
    print("★ date : " + Time_Convert(str(meta_json.date)))  # utc
    print("★ extension : " + str(meta_json.extension))
    print("★ name : " + str(meta_json.name))
    print("★ itemSize : " + str(meta_json.itemSize))
    print("★ parentFolderID : " + str(meta_json.parentFolderID))
    print("★ created : " + Time_Convert(str(meta_json.created)))  # utc
    print("★ contentUpdated : " + Time_Convert(str(meta_json.contentUpdated)))  # utc
    print("★ deleted : " + Time_Convert(str(meta_json.deleted)))  # utc
    print("★ filesCount : " + str(meta_json.filesCount))
    print("★ isExternallyOwned : " + str(meta_json.isExternallyOwned))
    print("★ deletedBy : " + str(meta_json.deletedBy))
    print("★ deletedFromTrash : " +
          Time_Convert(str(meta_json.deletedFromTrash)))  # utc
    print("★ lastUpdatedByName : " + str(meta_json.lastUpdatedByName))
    print("★ isSelfOrAncestorCollaborated : " +
          str(meta_json.isSelfOrAncestorCollaborated))
    print("★ versionCount : " + str(meta_json.versionCount))
    print("★ ownerName : " + str(meta_json.ownerName))
    print("★ ownerEnterpriseName : " + str(meta_json.ownerEnterpriseName))
    print("★ ownerEnterpriseID : " + str(meta_json.ownerEnterpriseID))
    print("★ contentCreated : " + Time_Convert(str(meta_json.contentCreated)))  # utc
    print("★ isBox3DPackageSupported : " +
          str(meta_json.isBox3DPackageSupported))
    print("★ durl : " + str(meta_json.durl))
    print("★ iconType : " + str(meta_json.iconType))
    print("★ isRetained : " + str(meta_json.isRetained))
    print("★ isRetainedUntil : " + str(meta_json.isRetainedUntil))
    print("★ isRetainedByPolicyType : " +
          str(meta_json.isRetainedByPolicyType))
    print("★ canDelete : " + str(meta_json.canDelete))
    print("★ canRestore : " + str(meta_json.canRestore))
    print("\n\n")


def Box_History(MetaSet):
    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    i = 0

    while True:
        if i == len(MetaSet.Global_file_list):
            break

        file = MetaSet.Global_file_list[i]

        if file.version_count == 1:
            i += 1
            continue

        version_count = str(file.version_count)
        version_file_name = ""

        for index in range(1, file.version_count):
            Download_target = MetaSet.Global_file_list[i + index]

            version_file_name = str(file.name).split(
                '.')[0] + "(ver" + str(int(version_count) - index) + ")"
            version_file_name += "." + file.extension

            requestURL = str(Download_target.durl)
            responseData = requests.get(
                url=requestURL, cookies=Box_Cookies, proxies=proxies, verify=False)
            filePATH = os.path.join(".\\Box", ".history", version_file_name)

            f = open(filePATH, 'wb')
            f.write(responseData.content)

            print("[Success]", filePATH)

        i += int(version_count)


def Box_Export(MetaSet):

    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    Box_Request_Token = str(MetaSet.request_token)

    for file in MetaSet.Global_file_list:

        if int(file.version_count) != 1:
            continue

        fid = "f_" + str(file.fid)

        requestURL = "https://app.box.com/index.php?" + \
            "rm=box_v2_download_file&" + "file_id=" + str(fid)

        data = {
            "request_token": Box_Request_Token
        }

        responseData = requests.post(
            url=requestURL, data=data, cookies=Box_Cookies, proxies=proxies, verify=False)

        filePATH = os.path.join(".\\Box", ".downloads",
                                str(file.name))

        f = open(filePATH, 'wb')
        f.write(responseData.content)

        print("[Success]", filePATH)


def Box_RB_Export(MetaSet):

    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    Box_Request_Token = str(MetaSet.request_token)

    for RB_file in MetaSet.RB_Global_file_list:
        fid = "f_" + str(RB_file.id)

        requestURL = "https://app.box.com/app-api/enduserapp/trash/restore"

        header = {
            "X-Request-Token": Box_Request_Token
        }

        data = "{\"itemTypedIDs\":[\"" + \
            str(fid) + "\"],\"parentFolderID\":\"\"}"

        responseData = requests.post(
            url=requestURL, headers=header, data=data, cookies=Box_Cookies, proxies=proxies, verify=False)

        requestURL2 = "https://app.box.com/index.php?" + \
            "rm=box_v2_download_file&" + "file_id=" + str(fid)

        data = {
            "request_token": Box_Request_Token
        }

        responseData = requests.post(
            url=requestURL2, data=data, cookies=Box_Cookies, proxies=proxies, verify=False)

        filePATH = os.path.join(".\\Box", ".downloads",
                                str(RB_file.name))

        f = open(filePATH, 'wb')
        f.write(responseData.content)

        print("[RB_Success]", filePATH)


# 버전 시간 변환 2022-12-19T00:27:02-08:00 -> 2022-12-19T17:27:02+09:00
def VTime_Convert(timeStamp):
    if timeStamp == "" or timeStamp is None:
        return ""

    dateStamp, delta = timeStamp[:-6], 9 - int(timeStamp[-6:-3])
    convertTime = datetime.strptime(dateStamp, '%Y-%m-%dT%H:%M:%S')
    convertTime += timedelta(hours=delta)
    return str(convertTime.strftime('%Y-%m-%dT%H:%M:%S+09:00'))

# UTC -> UTC+9 1671437126 -> 2022-12-19T17:05:26Z+09:00


def Time_Convert(UTC):
    if UTC == "" or UTC is None:
        return ""

    dateStamp = datetime.fromtimestamp(int(UTC))
    return str(dateStamp.strftime('%Y-%m-%dT%H:%M:%SZ+09:00'))
