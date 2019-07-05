import requests
from bs4 import BeautifulSoup as soup
from requests_ntlm import HttpNtlmAuth
import datetime
from math import ceil
import time

USERNAME = "shreya663976@majesco.com"
PASSWORD = "Jul@2019"
MAJESCO_URL = "https://www.majesconet.com/Pages/default.aspx"
MAJESCO_URL_ATN = "https://ess.majesconet.com/Net04/HR/MyInfo/MyInfo_MyAttendance.aspx"

s = requests.Session()

def majesco_login():
    print('Loggin in to Majesco Domain.')
    s.auth = HttpNtlmAuth(USERNAME,PASSWORD)
    resp = s.get(MAJESCO_URL)
    if resp.status_code==200:
        print('Logged In!!\n')
    else:
        print('Error\n')

def get_page():
    resp = s.get(MAJESCO_URL_ATN)
    page_html = resp.text
    pg_sp = soup(page_html, "html.parser")
    #table = pg_sp.find('table',id="cphPage_tblAttendanceParent")
    return pg_sp

def get_data(pg_sp):
    dt = datetime.datetime.today()
    sysdt = dt.day
    sysday = dt.strftime('%A')
    sysweek = week_of_month(dt)
    parentboxid = "cphPage_trParentBox"+str(sysweek)
    dayid = "cphPage_td"+sysday+str(sysweek)
    weektotal = "cphPage_tdAttendanceWeek"+str(sysweek)
    intaggreid = "cphPage_lblCMSFValW"+str(sysweek)
    intodayid = "cphPage_lblInTime"+sysday+str(sysweek)
    intoday = pg_sp.find('span',id=intodayid).text
    intaggre = pg_sp.find('span',id=intaggreid).text
    print('DATE:',dt.strftime('%d-%m-%Y %I:%M%p'))
    print('IN_TIME:',intoday)
    return intoday,intaggre

def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()
    return int(ceil(adjusted_dom/7.0))


