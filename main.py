from pyfiglet import Figlet
from termcolor import colored
import os
import Box_Login
import Box_Explorer



def Main_intro():
    os.system('cls')
    f = Figlet(font='big')
    print(colored(f.renderText('Box     breaker'), 'blue'))
    print(colored(" - Research on Data Acquisition and Analysis for Box Service", 'blue'))
    print(colored(" - Institute of Cyber Security & Privacy (ICSP)", 'blue'))
    print(colored(" - Digital Forensic Research Center", 'blue'))
    print(colored(" - Made By Jaeuk Kim (Assistant Researcher)\n", 'blue'))

if __name__ =="__main__":
    Main_intro()

    # Box ID, Box PW, z, request_token
    Essential_Information = Box_Login.Authentication()

    # 파일 리스트 수집
    # Box_Explorer.Get_File_List(Essential_Information)