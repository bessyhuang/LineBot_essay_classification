# 語料下載：博碩士論文知識加值系統 this_one

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as b4

from pymongo import MongoClient

def del_space_in_text(summary):
    for i in summary:
        if i in " :":
            summary = summary.strip()
            summary = summary.replace(':', '')
    return summary

def write_corpus_to_database(basic_dict):
    client = MongoClient('localhost', 27017)
    db = client['paper2020']
    collection = db['fju_paper']
    p_id = db.fju_paper.insert_one(basic_dict)
    print(p_id, basic_dict['論文名稱'])


browser = webdriver.Chrome()
browser.get('https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge')
browser.find_element_by_name('Image10').click()

keyword = '輔仁大學' #input('請輸入校院名稱：') or 
browser.find_element_by_id('ysearchinput0').send_keys(keyword)
s1 = Select(browser.find_element_by_name('qf0'))
s1.select_by_value("asc") #s1.select_by_visible_text("校院名稱")
browser.find_element_by_id("gs32search").click()

num_of_paper = browser.find_element_by_xpath('/html/body/form/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/span[2]').text
print(num_of_paper, type(num_of_paper))
browser.find_element_by_css_selector('.etd_d').click()


count = 379
basic_dict_one = {}
for paper_id in range(379, 430 + 1): #num_of_paper (1) 17 252 326 353 356 366 379 int(num_of_paper)
    print(paper_id)
    html = browser.page_source
    soup = b4(html, 'html.parser')
    table1 = soup.select('#format0_disparea > tbody')

    for i in range(len(table1)):
        basic_dict_one["id"] = count
        ### 論文基本資料
        if i == 0:
            for j in table1[0]:
                th = j.find('th')
                th = del_space_in_text(th.get_text())
                td = j.find('td')
                td = del_space_in_text(td.get_text())
                basic_dict_one[th] = td

        ### 摘要 外文摘要 目次 參考文獻 電子全文 紙本論文 QR Code
        else:
            title = browser.find_element_by_css_selector('#gs32_levelrecord > ul > li:nth-child({}) > a > em'.format(i + 1))
            title.click()
            content = table1[i].find('div')
            try:
                content = del_space_in_text(content.get_text())
                basic_dict_one[title.text] = content
            except:
                basic_dict_one[title.text] = content
                
    count += 1
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="bodyid"]/form[1]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/input[2]').clear()
    browser.find_element_by_xpath('//*[@id="bodyid"]/form[1]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/input[2]').send_keys(count)
    browser.find_element_by_xpath('//*[@id="bodyid"]/form[1]/div/table/tbody/tr[1]/td[2]/table/tbody/tr[4]/td/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/input[1]').click()
    write_corpus_to_database(basic_dict_one)
    basic_dict_one.clear()

# print(basic_dict[7].keys())
