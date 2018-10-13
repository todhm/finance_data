
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from datetime import timedelta, date
from datetime import datetime as dt
import requests
import time


def search_stats_code(code, keyword, find_key="STAT_NAME"):
    result = {}
    result['status'] = 'FAIL'
    result['message'] = '잘못된 형식의 데이터입니다.'
    listName = 'StatisticTableList' if find_key == 'STAT_NAME' else 'StatisticItemList'

    if not type(code) is dict:
        return result

    if not listName in code.keys():
        return result

    if not 'row' in code[listName].keys():
        return result

    nameList = map(lambda x: x[find_key] if x.get(
        find_key) else '', code[listName]['row'])
    resultData = []
    for idx, name in enumerate(nameList):
        if name.find(keyword) >= 0:
            resultData.append(code[listName]['row'][idx])

    if not resultData:
        result['message'] = '해당 통계를 찾을 수 없습니다.'
        return result
    else:
        result['status'] = "SUCCESS"
        result.pop('message')
        result['data'] = resultData
        return result


def get_all_industries_company():
    return None


def get_all_industries_sites():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.implicitly_wait(10)
    indust_lst = []
    try:
        driver.get('http://finance.daum.net/quote/upjong.daum?nil_stock=refresh')
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))
        classButtonXpath = "//*[@id='bizBody1']"
        iframeTable = driver.find_element_by_xpath(classButtonXpath)
        tr_lst = iframeTable.find_elements_by_xpath('//tr')
        for tr in tr_lst:
            try:
                html_source = tr.get_attribute('innerHTML')
                soup = BeautifulSoup(html_source)
                td = soup.find('td', {'class': 'txt'})
                a = td.find('a')
                site = a['href']
                name = td.text
                siteData = {}
                siteData['name'] = name
                siteData['site'] = site
                indust_lst.append(siteData)
            except Exception as e2:
                pass

    except Exception as e:
        print(str(e))
        pass
        return None
    driver.quit()
    return indust_lst


def getCompanyNames(html_source, companyList, industry):
    soup = BeautifulSoup(html_source)
    tableElem = soup.find('table', {'class': "gTable"})
    if tableElem:
        tdList = tableElem.findAll('td', {'class': 'txt'})
        for td in tdList:
            try:
                a = td.find('a')
                site = a['href']
                companyName = td.text
                siteData = {}
                siteData['name'] = companyName
                siteData['code'] = site
                siteData['industry'] = industry
                companyList.append(siteData)
            except Exception as e:
                print(e)
                pass
    return companyList


def getScriptList(driver):
    scriptList = []
    pageXpath = "//*[@class='pagingTable']"
    paginationTable = driver.find_element_by_xpath(pageXpath)
    if paginationTable:
        paginationElements = paginationTable.find_elements_by_xpath(
            '//tr/td/span')
        for idx, pageButton in enumerate(paginationElements):
            htmlSource = pageButton.get_attribute('innerHTML')
            if 'href' in htmlSource:
                aTag = pageButton.find_element_by_tag_name('a')
                script = aTag.get_attribute('href')
                scriptList.append(script)
    return scriptList


def getAllCompanyList(industList):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.implicitly_wait(5)
    companyList = []
    for ind in industList:
        baseUrl = 'http://finance.daum.net'
        url = baseUrl + ind['site']
        industry = ind['name']
        driver.get(url)
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe"))
        html_source = driver.page_source
        companyList = getCompanyNames(html_source, companyList, industry)
        scriptList = getScriptList(driver)
        for script in scriptList:
            driver.execute_script(script)
            html_source = driver.page_source
            companyList = getCompanyNames(html_source, companyList, industry)
    return companyList


def daterange(start_date_str, end_date_str, diffrange):
    start_date = dt.strptime(start_date_str, '%Y%m%d').date()
    end_date = dt.strptime(end_date_str, '%Y%m%d').date()
    date_diff = (end_date - start_date).days
    for n in range(0, int(date_diff), diffrange):
        start = start_date + timedelta(n)
        if n + (diffrange - 1) < date_diff:
            end = start_date + timedelta(n+(diffrange - 1))
        else:
            end = start_date + timedelta(date_diff)
        yield start.strftime('%Y%m%d'), end.strftime('%Y%m%d')


def exception_handler(request, exception):
    try:
        response = requests.get(request.url)
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        response = requests.get(request.url)

    return response
