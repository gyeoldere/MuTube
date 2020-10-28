from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import time
import csv

'''
코드 실행을 위해서는 바탕화면에 chromedriver.exe가 있어야 합니다. 
chromedriver는 https://chromedriver.chromium.org/downloads에서 받으실 수 있습니다.
'''

# 전역변수 선언부
titlelist = []
artistlist = []
datelist = []
genrelist = []
houselist = []
jaksalist = []
jakgoklist = []
lyricslist = []
toplist = []
delay=3
 


browser = Chrome(r'C:\Users\gyeol\Desktop\chromedriver.exe')
browser.implicitly_wait(delay)

# 멜론 공식 사이트에서 차트 검색으로 이동
browser.get('https://www.melon.com/chart/index.htm')
browser.find_element_by_class_name("chart_finder").click()



def chart_load(decade,year,month,week):
    print(str(decade) + " " + str(year) + " " + str(month) + " " + str(week) + " ")
    browser.find_element_by_class_name("tab01").click()  # 주간차트

    browser.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/form/div[1]/div/div/div[1]/div[1]/ul/li['
        + str(decade) + ']').click()

    # 2010년대 - 2019년 : 내림차순으로 리스트 목록 상승시키면 됨
    browser.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/div/div/div[2]/div[1]/ul/li['
                                  + str(year) + ']').click()


    # 01월~12월 : 오름차순으로 리스트 목록 상승시키면 됨
    browser.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/div/div/div[3]/div[1]/ul/li['
                                  + str(month) + ']').click()

    # 주차
    browser.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/div/div/div[4]/div[1]/ul/li['
                                  + str(week) + ']').click()

    browser.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/div/div/div[5]/div[1]/ul/li[2]').click()

    '''
    다른 장르 설정을 위한 프리셋
    if year > 3:
        browser.find_element_by_xpath(
            '/html/body/div/div[3]/div/div/form/div[1]/div/div/div[5]/div[1]/ul/li[2]').click()
    else :
        browser.find_element_by_xpath('/html/body/div/div[3]/div/div/form/div[1]/div/div/div[5]/div[1]/ul/li[2]').click()
    '''

    browser.find_element_by_class_name("btn_b26").click()


def extract_feature(score):
    forpath = "/html/body/div/div[3]/div/div/div/div[1]/div[2]/form/div[1]/table/tbody/tr["
    feature_backpath = "]/td[4]/div/a"
    featurepath = forpath + str(score) + feature_backpath

    jaksa = "작사가"
    jakgok = "작곡가"

    browser.find_element_by_xpath(featurepath).click()

    browser.implicitly_wait(3)
    title = browser.find_element_by_xpath(
        "/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[1]/div[1]").text

    if title in titlelist:
        browser.back()
        browser.implicitly_wait(3)
        time.sleep(random.randrange(1,3))
        return

    artist = browser.find_element_by_xpath(
        "/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[1]/div[2]/a/span[1]").text
    date = browser.find_element_by_xpath(
        "/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[2]/dl/dd[2]").text
    date = str(date).replace(".","")
    genre = browser.find_element_by_xpath(
        "/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[2]/dl/dd[3]").text
    ban = ["힙합","랩","발라드"]
    for banlist in ban:
        if banlist in genre:
            browser.back()
            browser.implicitly_wait(3)
            time.sleep(random.randrange(1, 3))
            print("banned" + banlist)
            return

    composers = browser.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[3]/ul/li")
    for i in range (len(composers)):
        if browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[3]/ul/li[" + str(i+1) + "]/div[2]/div[2]/span").text == "작사" :
            jaksa = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[3]/ul/li[" + str(i+1) + "]/div[2]/div[a]/a").text
        if browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[3]/ul/li[" + str(i+1) + "]/div[2]/div[2]/span").text == "작곡" :
            jakgok = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[3]/ul/li[" + str(i+1) + "]/div[2]/div[a]/a").text

    lyrics = ""
    lines = browser.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div[2]/div/br")
    lyrics = browser.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div/div[2]/div[2]/div").text
    lyrics = str(lyrics).replace("\n"," ")
    browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/form/div/div/div[2]/div[1]/div[2]/a").click()
    browser.implicitly_wait(3)
    time.sleep(random.randrange(1, 3))
    li1 = browser.find_elements_by_xpath(
        "/html/body/div/div[3]/div/div/div[1]/div/div[2]/dl[1]/dt")

    cnt = 1
    for each in li1:
        if each.text == "소속사" : break;
        else : cnt += 1

    try:
        house = browser.find_element_by_xpath(
            "/html/body/div/div[3]/div/div/div[1]/div/div[2]/dl[1]/dd[" + str(cnt) +"]").text
    except:
        house = " "

    titlelist.append(title)
    artistlist.append(artist)
    datelist.append(date)
    genrelist.append(genre)
    houselist.append(house)
    jaksalist.append(jaksa)
    jakgoklist.append(jakgok)
    lyricslist.append(lyrics)
    toplist.append(score)

    print(title)

    browser.implicitly_wait(3)
    time.sleep(random.randrange(1))
    browser.back()

    browser.implicitly_wait(3)
    time.sleep(random.randrange(1))
    browser.back()

    browser.implicitly_wait(3)


decade = 2
year = 4


for i in range (2):
    if decade == 1:
        for month in range(1,8):
            for week in range(1,5):
                for score in range(10):
                    chart_load(decade, 1, month, week)
                    try:
                        extract_feature(score+1)
                    except : continue

    else :
        for j in range (4):
            for month in range(1, 13):
                for week in range(1, 5):
                    for score in range(4):
                        chart_load(decade, year, month, week)
                        extract_feature(score+1)

            year -= 1
    decade -= 1

sumlist = [titlelist,artistlist,datelist,genrelist,houselist,jaksalist,jakgoklist,lyricslist,toplist]

with open('output.tsv', 'wt') as out_file:

    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['title', 'artist', 'date', 'genre', 'agency', 'lyricist', 'composer', 'lyrics','top','gender'])
    for times in range(len(titlelist)):
        templist = []
        for i in range(len(sumlist)):
            templist.append(sumlist[i][times])
        tsv_writer.writerow(templist)

print(titlelist)
print(len(titlelist))

