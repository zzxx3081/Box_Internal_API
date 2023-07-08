import os
import json
import requests
from datetime import datetime, timedelta
import Box_Collector
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    # 'http': 'http://127.0.0.1:8888',
    # 'https': 'http://127.0.0.1:8888'
}


def Start(Box_MetaSet=""):
    os.system('cls')

    while(True):

        print("\n\n검색 메뉴를 선택해주세요.")
        print("0. 종료")
        print("1. 시간 검색")
        print("2. 파일 내용 검색")
        print("3. 파일 제목 검색")
        print("4. 파일 확장자 검색")
        print("5. 파일 크기 검색")

        selectMenu = input("\n선택: ")

        if selectMenu not in ["0", "1", "2", "3", "4", "5"]:
            print("\n잘못된 입력입니다. 다시 입력해주세요. (0 ~ 5)")
            continue

        if selectMenu == "0":
            exit(0)

        elif selectMenu == "1":
            Box_Search_Time(Box_MetaSet)

        elif selectMenu == "2":
            Box_Search_Content(Box_MetaSet)

        elif selectMenu == "3":
            Box_Search_Title(Box_MetaSet)

        elif selectMenu == "4":
            Box_Search_Type(Box_MetaSet)

        elif selectMenu == "5":
            Box_Search_Size(Box_MetaSet)

# 파일 시간 검색


def Box_Search_Time(MetaSet):

    Search_root = "/app-api/enduserapp/folder/0/search"

    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    print("-"*50)
    updatedTimeFrom = UTC_to_Int(input("시작 시간을 입력하세요 (ex 2022 01 01): "))
    updatedTimeTo = UTC_to_Int(input("종료 시간을 입력하세요 (ex 2023 01 01): "))
    requestURL = f"https://app.box.com/folder/0/search?updatedTime=customrange&updatedTimeFrom={updatedTimeFrom}&updatedTimeTo={updatedTimeTo}"

    responseData = requests.get(
        url=requestURL, cookies=Box_Cookies, proxies=proxies, verify=False)

    Box_PostStreamData = responseData.text.split("Box.postStreamData = ")[1]
    Box_PostStreamData = Box_PostStreamData.split(";")[0]
    JsonPage = json.loads(Box_PostStreamData)

    for item in JsonPage[Search_root]["searchItems"]:
        if str(item["typedID"])[0] == "d":
            continue

        for f in MetaSet.Global_file_list:
            if str(f.fid) == str(item["typedID"])[2:]:
                Box_Collector.File_WriteLine(f)
                break

        for RB_f in MetaSet.RB_Global_file_list:
            if str(RB_f.id) == str(item["typedID"])[2:]:
                Box_Collector.RB_File_WriteLine(RB_f)
                break

# 2023 07 01 -> 1688137200000


def UTC_to_Int(timeStamp):
    convertTime = datetime.strptime(timeStamp, '%Y %m %d')
    Epoch = datetime.strptime("1970 01 01", '%Y %m %d')
    Span_element = int((convertTime - Epoch).total_seconds() - 32400)
    return str(Span_element * 1000)


# 파일 내용 검색
def Box_Search_Content(MetaSet):
    Search_root = "/app-api/enduserapp/folder/0/search"

    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    query = input("검색할 파일 내용 일부를 입력하세요. ")

    requestURL = f"https://app.box.com/folder/0/search?kinds=file_content&query={query}"

    responseData = requests.get(
        url=requestURL, cookies=Box_Cookies, proxies=proxies, verify=False)

    Box_PostStreamData = responseData.text.split("Box.postStreamData = ")[1]
    Box_PostStreamData = Box_PostStreamData.split(";")[0]
    JsonPage = json.loads(Box_PostStreamData)

    for item in JsonPage[Search_root]["searchItems"]:
        if str(item["typedID"])[0] == "d":
            continue

        for f in MetaSet.Global_file_list:
            if str(f.fid) == str(item["typedID"])[2:]:
                Box_Collector.File_WriteLine(f)
                break

        for RB_f in MetaSet.RB_Global_file_list:
            if str(RB_f.id) == str(item["typedID"])[2:]:
                Box_Collector.RB_File_WriteLine(RB_f)
                break

# 파일 제목 검색


def Box_Search_Title(MetaSet):
    Search_root = "/app-api/enduserapp/folder/0/search"

    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    query = input("검색할 파일 제목을 입력하세요. ")

    requestURL = f"https://app.box.com/folder/0/search?kinds=name&query={query}"

    responseData = requests.get(
        url=requestURL, cookies=Box_Cookies, proxies=proxies, verify=False)

    Box_PostStreamData = responseData.text.split("Box.postStreamData = ")[1]
    Box_PostStreamData = Box_PostStreamData.split(";")[0]
    JsonPage = json.loads(Box_PostStreamData)

    for item in JsonPage[Search_root]["searchItems"]:
        if str(item["typedID"])[0] == "d":
            continue

        for f in MetaSet.Global_file_list:
            if str(f.fid) == str(item["typedID"])[2:]:
                Box_Collector.File_WriteLine(f)
                break

        for RB_f in MetaSet.RB_Global_file_list:
            if str(RB_f.id) == str(item["typedID"])[2:]:
                Box_Collector.RB_File_WriteLine(RB_f)
                break


# 파일 확장자 검색
def Box_Search_Type(MetaSet):
    Search_root = "/app-api/enduserapp/folder/0/search"

    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    dic = {
        "0": "audio",
        "1": "document",
        "2": "image",
        "3": "pdf",
        "4": "presentation",
        "5": "spreadsheet",
        "6": "video"
    }

    while(True):

        print("\n\n파일 확장자 메뉴를 선택해주세요.")
        print("0. audio")
        print("1. document")
        print("2. image")
        print("3. pdf")
        print("4. presentation")
        print("5. spreadsheet")
        print("6. video")

        selectMenu = input("\n선택: ")

        if selectMenu not in ["0", "1", "2", "3", "4", "5", "6"]:
            print("\n잘못된 입력입니다. 다시 입력해주세요. (0 ~ 6)")
            continue

        types = dic[selectMenu]
        break

    requestURL = f"https://app.box.com/folder/0/search?types={types}"

    responseData = requests.get(
        url=requestURL, cookies=Box_Cookies, proxies=proxies, verify=False)

    Box_PostStreamData = responseData.text.split("Box.postStreamData = ")[1]
    Box_PostStreamData = Box_PostStreamData.split(";")[0]
    JsonPage = json.loads(Box_PostStreamData)

    for item in JsonPage[Search_root]["searchItems"]:
        if str(item["typedID"])[0] == "d":
            continue

        for f in MetaSet.Global_file_list:
            if str(f.fid) == str(item["typedID"])[2:]:
                Box_Collector.File_WriteLine(f)
                break

        for RB_f in MetaSet.RB_Global_file_list:
            if str(RB_f.id) == str(item["typedID"])[2:]:
                Box_Collector.RB_File_WriteLine(RB_f)
                break


# 파일 크기 검색
def Box_Search_Size(MetaSet):
    Search_root = "/app-api/enduserapp/folder/0/search"

    Box_Cookies = {
        'z': MetaSet.z['z'],
        'uid': MetaSet.uid['uid']
    }

    dic = {

        "0": "1",
        "1": "5",
        "2": "25",
        "3": "100",
        "4": "1000",
        "5": "1024"
    }

    while(True):

        print("\n\n파일 크기 메뉴를 선택해주세요.")
        print("0. 0 - 1 MB")
        print("1. 1 - 5 MB")
        print("2. 5 - 25 MB")
        print("3. 25 - 100 MB")
        print("4. 100MB - 1 GB")
        print("5. 1 GB+")

        selectMenu = input("\n선택: ")

        if selectMenu not in ["0", "1", "2", "3", "4", "5"]:
            print("\n잘못된 입력입니다. 다시 입력해주세요. (0 ~ 5)")
            continue

        itemSize = dic[selectMenu]
        break

    requestURL = f"https://app.box.com/folder/0/search?itemSize={itemSize}"

    responseData = requests.get(
        url=requestURL, cookies=Box_Cookies, proxies=proxies, verify=False)

    Box_PostStreamData = responseData.text.split("Box.postStreamData = ")[1]
    Box_PostStreamData = Box_PostStreamData.split(";")[0]
    JsonPage = json.loads(Box_PostStreamData)

    for item in JsonPage[Search_root]["searchItems"]:
        if str(item["typedID"])[0] == "d":
            continue

        for f in MetaSet.Global_file_list:
            if str(f.fid) == str(item["typedID"])[2:]:
                Box_Collector.File_WriteLine(f)
                break

        for RB_f in MetaSet.RB_Global_file_list:
            if str(RB_f.id) == str(item["typedID"])[2:]:
                Box_Collector.RB_File_WriteLine(RB_f)
                break
