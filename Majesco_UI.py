from tkinter import *
import Majesco_Fetch as maj
import datetime
from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read('config.ini')

LOGINHOURS = '08:45' #CONFIG.get('INFO', 'CHECKIN_HRS')
LOGINHOURS6HRS = '06:00'
FONT = 'Lucida Sans Unicode'#CONFIG.get('INFO', 'FONT')
FONTSIZE = 10 #CONFIG.get('INFO', 'FONTSIZE')
FONTWEIGHT = ''
BACKGROUNDCOLOR = CONFIG.get('INFO', 'BACKGROUNDCOLOR')
FOREGROUNDCOLOR = CONFIG.get('INFO', 'FOREGROUNDCOLOR')
XAXIS = 165

### TK Init options
win=Tk()
win.title('Majesco Clock')
win.resizable(0,0)
win.geometry("310x220")
win.configure(background=BACKGROUNDCOLOR)
#win.wm_attributes("-topmost", 1)
#win.overrideredirect(1)
#win.attributes("-toolwindow",1)

### Get Intime Data from Majesco
login = maj.majesco_login()
if login == 1:
    pg_sp = maj.get_page()
    in_today,in_agg = maj.get_data(pg_sp)
else:
    in_today,in_agg='0','0'
"""
in_today,in_agg = '09:00','21:00'
"""

### Time Update Funtions
def update_clock():
    #now = datetime.datetime.today().strftime('%d-%m-%Y %I:%M:%S %p')
    now = datetime.datetime.today().strftime('%I:%M:%S %p')
    lbl1ans.configure(text=now)
    win.after(1000,update_clock)

def update_time_passed():
    timepassed = (datetime.datetime.now().replace(second = 0,microsecond=0))-intimesys
    lbl4ans.configure(text=str(timepassed)[:-3]+' Hrs')
    win.after(1000,update_time_passed)

def update_time_to_pass():
    timetopass = timeout - (datetime.datetime.now().replace(second = 0,microsecond=0))
    if datetime.timedelta(seconds=0)>=timetopass:
        timetopass = (datetime.datetime.now().replace(second = 0,microsecond=0)) - timeout
        lbl5.configure(text='Extra Time',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
        lbl6.configure(text='6/8.45 Hrs',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
        lbl6ans.configure(text='DONE!',font=(FONT, FONTSIZE, FONTWEIGHT),fg='green')
    lbl5ans.configure(text=str(timetopass)[:-3]+' Hrs')
    win.after(1000,update_time_to_pass)

def update_time_to_pass_6hrs():
    timetopass = timeout_6hrs - (datetime.datetime.now().replace(second = 0,microsecond=0))
    if datetime.timedelta(seconds=0)>=timetopass:
        timetopass = (datetime.datetime.now().replace(second = 0,microsecond=0)) - timeout_6hrs
        lbl6ans.configure(text='DONE!',font=(FONT, FONTSIZE, FONTWEIGHT),fg='green')
    else:
        lbl6ans.configure(text=str(timetopass)[:-3]+' Hrs')
        win.after(1000,update_time_to_pass_6hrs)


dt = datetime.datetime.today()

### Current Time
lbl1 = Label(win, text='Current Time',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR).place(x=50, y=25)
lbl1ans = Label(text="",font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
lbl1ans.place(x=XAXIS, y=25)
update_clock()

if in_today=='00:00':
    loglabl = Label(win, text='Intime not Logged for today!',font=(FONT, 12, FONTWEIGHT),fg='red',bg=BACKGROUNDCOLOR).place(x=30, y=60)
elif in_today=='0':
    loglabl = Label(win, text='Unable to Login!',font=(FONT, 12, FONTWEIGHT),fg='red',bg=BACKGROUNDCOLOR).place(x=75, y=60)
else:
    ### In Time
    intimesys = dt.replace(hour=int(in_today[:2]), minute=int(in_today[3:]),second = 0,microsecond=0)
    lbl2 = Label(win, text='In Time',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR).place(x=50, y=50)
    lbl2ans = Label(win, text=intimesys.strftime("%I:%M %p"),font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR).place(x=XAXIS, y=50)
    
    ### Out Time
    timeout = intimesys+datetime.timedelta(hours=int(LOGINHOURS[:2]), minutes=int(LOGINHOURS[3:]))
    timeout_6hrs = intimesys+datetime.timedelta(hours=int(LOGINHOURS6HRS[:2]), minutes=int(LOGINHOURS6HRS[3:]))
    lbl3 = Label(win, text='Out Time',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR).place(x=50, y=75)
    lbl3ans = Label(win, text=timeout.strftime("%I:%M %p"),font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR).place(x=XAXIS, y=75)
    
    ### Time Passed
    lbl4 = Label(win, text='Time Passed',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR).place(x=50, y=100)
    lbl4ans = Label(text="",font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
    lbl4ans.place(x=XAXIS, y=100)
    update_time_passed()

    ### Time To Pass - Full Day
    lbl6 = Label(win, text='6.00 Hrs',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
    lbl6.place(x=50, y=125)
    lbl6ans = Label(text="",font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
    lbl6ans.place(x=XAXIS, y=125)
    update_time_to_pass_6hrs()
    
    ### Time To Pass/Extra Time
    lbl5 = Label(win, text='8.45 Hrs',font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
    lbl5.place(x=50, y=150)
    lbl5ans = Label(text="",font=(FONT, FONTSIZE, FONTWEIGHT),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR)
    lbl5ans.place(x=XAXIS, y=150)
    update_time_to_pass()
    
    ### Footer
    lbl2 = Label(win, text='Created by Shreyan Jadhav',font=(FONT, 7),bg=BACKGROUNDCOLOR, fg=FOREGROUNDCOLOR).place(x=150, y=190)

win.mainloop()
