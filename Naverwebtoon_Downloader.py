import os
import requests
import zipfile
import shutil
from bs4 import BeautifulSoup


# 679544
# &no=
# http://comic.naver.com/webtoon/detail.nhn?titleId=679544&no=50
# http://comic.naver.com/webtoon/list.nhn?titleId=679544

def download(fire):
    global number
    global wname
    global endFire

    dBaseUrl = "http://comic.naver.com/webtoon/detail.nhn?titleId="
    URL = dBaseUrl + number + "&no=" + str(fire)#각 화의 URL조합
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")#파싱
    jpgs = soup.select("div.wt_viewer img")#선택자

    j = 1
    for i in jpgs:
        filename = wname[0] + "-" + str(fire) + "-" + str(j) + ".jpg"
        print("filename : {4}%({2}/{3}){0}\noriginal url : {1}".format(filename, i.get('src'),fire,endFire,int(fire/endFire*100)))
        req = requests.get(i.get('src'), headers={'Referer': URL}).content #headers = {'Referer': URL}이용하여 요청(403 방지) #각 사진들 다운
        with open("./" + wname[0] + "/" + filename, 'wb') as d:#저장
            d.write(req)
        j += 1


def files2zip():
    global wname

    print("files to zip start!\n")

    h_zip = zipfile.ZipFile('./' + wname[0] + '.zip', 'w')#zip
    for folder, subfolders, files in os.walk('./' + wname[0] + "/"):
        for file in files:
            if (file.endswith('.jpg') or file.endswith('.png')):
                h_zip.write(os.path.join(folder, file),
                            os.path.relpath(os.path.join(folder, file), './' + wname[0] + "/"),
                            compress_type=zipfile.ZIP_DEFLATED)
    h_zip.close()

    print("finish zipping!\n")
    print("deleting files...\n")
    shutil.rmtree("./" + wname[0])#폴더 지움
    print("finish deleting files!!\n\n")

baseUrl = "http://comic.naver.com/webtoon/list.nhn?titleId="
try:
    print("웹툰의 리스트가 있는 페이지의 URL을 입력 해 주세요.\n예시) http://comic.naver.com/webtoon/list.nhn?titleId=679544\n입력 : ",end="")
    number = input().replace("http://comic.naver.com/webtoon/list.nhn?titleId=", "")
    URL = baseUrl + number
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    curUrl = soup.select_one("td.title a")
    title = soup.select_one("#content > div.comicinfo > div.detail > h2")  # 파싱

    curFire = curUrl.get('onclick') # 마지막 업데이트 화 저장
    curFire = curFire.replace("clickcr(","")
    curFire = curFire.replace(")","")
    curFire = curFire.replace("'","")
    curFire = curFire.split(",")

    wname = title.get_text().strip().replace("\t", "").split()  # 제목과 작가이름 받아온 후 분리
except:
    print("아무래도 URL에 문제가 있는 것 같습니다.\n확인 해 주세요.\n")
    exit(1)

print("웹툰 : {1}\n작가 : {2}\n[1 ~ {0}]\n\n1화부터 {0}화까지 검색되었습니다.\n".format(curFire[3], wname[0], wname[1]))
print("다운로드를 시작할 화를 입력 해 주세요 : ", end="")
try:
    startFire = int(input())
except:
    print("잘못 입력하신듯 ㅇㅇ")
    exit(1)


if (startFire > int(curFire[3])):
    print("제 크롤러는 타임머신이 아닙니다.\n미래의 화를 요구하지 말아주세요.")
    exit(1)

print("다운로드를 끝낼 화를 입력 해 주세요 : ", end="")
try:
    endFire = int(input())
except:
    print("잘못 입력하신듯 ㅇㅇ")
    exit(1)
if(endFire < startFire):
    print("시작화가 끝낼 화보다 더 나중입니다.\n")
    exit(1)

if (endFire > int(curFire[3])):
    print("제 크롤러는 타임머신이 아닙니다.\n미래의 화를 요구하지 말아주세요.")
    exit(1)

if not os.path.exists(wname[0]):  # 다운로드 할 폴더생성
    os.makedirs(wname[0])

print("download start!\n")
for i in range(startFire, endFire + 1):#각 화를 위한 다운
    download(i)
print("download complete!\n\n")

print("파일들을 압축 후 원 파일들을 삭제하시겠습니까? (Y/N)")
answer = input()
while(1):
    if (answer == "Y" or answer == "y"):
        files2zip()#zip으로 바꿔주는 함수
        break
    if(answer=="n"or answer=="N"):
        break

print("All works are done")
