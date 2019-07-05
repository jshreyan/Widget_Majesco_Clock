from tkinter import *
import Majesco_Fetch as maj
import datetime

LOGINHOURS = '08:45'
FONT = 'Lucida Sans Unicode'
FONTSIZE = 10

win=Tk()
win.title('Majesco Clock')
#win.wm_attributes("-topmost", 1)
win.resizable(0,0)
#win.overrideredirect(1)
#win.attributes("-toolwindow",1)
win.geometry("290x200")

maj.majesco_login()
pg_sp = maj.get_page()
in_today,in_agg = maj.get_data(pg_sp)
#in_today,in_agg = '09:00','17:00'
#dt = datetime.datetime.today()

intimesys = dt.replace(hour=int(in_today[:2]), minute=int(in_today[3:]),second = 0,microsecond=0)
timeout = intimesys+datetime.timedelta(hours=int(LOGINHOURS[:2]), minutes=int(LOGINHOURS[3:]))
#print('OUT_TIME:',timeout.strftime("%I:%M %p"))

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
        lbl5.configure(text='Extra Time',font=(FONT, FONTSIZE))
    lbl5ans.configure(text=str(timetopass)[:-3]+' Hrs')
    win.after(1000,update_time_to_pass)

lbl1 = Label(win, text='Current Time',font=(FONT, FONTSIZE)).place(x=50, y=25)
lbl1ans = Label(text="",font=(FONT, FONTSIZE))
lbl1ans.place(x=150, y=25)
update_clock()

lbl2 = Label(win, text='In Time',font=(FONT, FONTSIZE)).place(x=50, y=50)
lbl2ans = Label(win, text=in_today,font=(FONT, FONTSIZE)).place(x=150, y=50)

lbl3 = Label(win, text='Out Time',font=(FONT, FONTSIZE)).place(x=50, y=75)
lbl3ans = Label(win, text=timeout.strftime("%I:%M %p"),font=(FONT, FONTSIZE)).place(x=150, y=75)

lbl4 = Label(win, text='Time Passed',font=(FONT, FONTSIZE)).place(x=50, y=100)
lbl4ans = Label(text="",font=(FONT, FONTSIZE))
lbl4ans.place(x=150, y=100)
update_time_passed()

lbl5 = Label(win, text='Time To Pass',font=(FONT, 8))
lbl5.place(x=50, y=125)
lbl5ans = Label(text="",font=(FONT, FONTSIZE))
lbl5ans.place(x=150, y=125)
update_time_to_pass()

lbl2 = Label(win, text='Created by Shreyan Jadhav',font=(FONT, 7)).place(x=150, y=170)

win.mainloop()
