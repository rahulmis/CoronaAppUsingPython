def Scrap():
    def notifyme(title,message):
        plyer.notification.notify(
            title=title,
            message=message,
            app_icon = 'vv.ico',
            timeout=20
        )
    url = 'https://www.worldometers.info/coronavirus/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    tablebody = soup.find('tbody')
    ttt = tablebody.find_all('tr')
    notifycountry = countrydata.get()
    if(notifycountry == ''):
        notifycountry = 'india'
    countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases = [], [], [], [], [], [], []
    serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion = [], [], [], [], []
    headers = ['countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases',
               'serious', 'totalcases_permillion', 'totaldeaths_permillion', 'totaltests', 'totaltests_permillion']

    for i in ttt:
        id = i.find_all('td')
        if(id[0].text.strip().lower() == notifycountry):
            totalcases1 = int(id[1].text.strip().replace(',', ''))
            totaldeaths1 = id[3].text.strip()
            newcases1 = id[2].text.strip()
            newdeaths1 = id[4].text.strip()
            notifyme('Corona Virus Details In {}'.format(notifycountry),
                     'Total Cases : {}\nTotal Deaths : {}\nNew Cases : {}\nNew Deaths : {}'.format(totalcases1,
                                                                                                   totaldeaths1,
                                                                                                   newcases1,
                                                                                                   newdeaths1))
        countries.append(id[0].text.strip())
        total_cases.append(int(id[1].text.strip().replace(',', '')))
        new_cases.append(id[2].text.strip())
        total_deaths.append(id[3].text.strip())
        new_deaths.append(id[4].text.strip())
        total_recovered.append(id[5].text.strip())
        active_cases.append(id[6].text.strip())
        serious.append(id[7].text.strip())
        totalcases_permillion.append(id[8].text.strip())
        totaldeaths_permillion.append(id[9].text.strip())
        totaltests.append(id[10].text.strip())
        totaltests_permillion.append(id[11].text.strip())
    df = pd.DataFrame(list(zip(countries, total_cases, new_cases,total_deaths, new_deaths, total_recovered, active_cases,serious,
                               totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion)),columns=headers)
    sor = df.sort_values('total_cases',ascending=False)
    for k in formatlist:
        if(k == 'html'):
            path2 = '{}/alldata.html'.format(path)
            sor.to_html(r'{}'.format(path2))
        if(k == 'json'):
            path2 = '{}/alldata.json'.format(path)
            sor.to_json(r'{}'.format(path2))
        if(k == 'csv'):
            path2 = '{}/alldata.csv'.format(path)
            sor.to_csv(r'{}'.format(path2))
    if(len(formatlist) !=0):
        messagebox.showinfo("Notification",'Corona Record Is saved {}'.format(path2),parent=root)


def download():
    global path
    if(len(formatlist) != 0):
        path = filedialog.askdirectory()
    else:
        pass
    Scrap()
    formatlist.clear()
    InHtml.configure(state='normal')
    InJson.configure(state='normal')
    InCsv.configure(state='normal')

def inhtml():
    formatlist.append('html')
    InHtml.configure(state='disabled')
def incsv():
    formatlist.append('csv')
    InCsv.configure(state='disabled')
def injson():
    formatlist.append('json')
    InJson.configure(state='disabled')

import plyer
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import messagebox,filedialog
root = Tk()
root.title('Corona Virus Information ')
root.geometry('530x300+200+80')
root.configure(bg='plum2')
root.iconbitmap('vv.ico')
formatlist = []
path = ''
#############################################################  Labels
IntroLabel = Label(root,text='Corona Virus Info',font=('new roman',30,'italic bold'),bg='blue',width=22)
IntroLabel.place(x=0,y=0)

EntryLabel = Label(root,text='Notify Country : ',font=('arial',20,'italic bold'),bg='plum2')
EntryLabel.place(x=10,y=70)

FormatLabel = Label(root,text='Download In : ',font=('arial',20,'italic bold'),bg='plum2')
FormatLabel.place(x=10,y=150)

############################################################# Entry
countrydata = StringVar()
ent1 = Entry(root,textvariable=countrydata,font=('arial',20,'italic bold'),relief=RIDGE,bd=2,width=20)
ent1.place(x=220,y=70)
############################################################  Buttons
InHtml = Button(root,text='Html',bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground='blue',activeforeground='white',
                bd=5,width=5,command=inhtml)
InHtml.place(x=210,y=150)

InJson = Button(root,text='Json',bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground='blue',activeforeground='white',
                bd=5,width=5,command=injson)
InJson.place(x=320,y=150)

InCsv = Button(root,text='Csv',bg='green',font=('arial',15,'italic bold'),relief=RIDGE,activebackground='blue',activeforeground='white',
                bd=5,width=5,command=incsv)
InCsv.place(x=430,y=150)

Submit = Button(root,text='Submit',bg='red',font=('arial',15,'italic bold'),relief=RIDGE,activebackground='blue',activeforeground='white',
                bd=5,width=25,command=download)
Submit.place(x=110,y=250)


root.mainloop()