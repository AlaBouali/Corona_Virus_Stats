#encoding: utf-8
from tkinter import *
from tkinter import ttk,messagebox

import sys,datetime,os,time,threading

if  sys.version_info < (3,0):#if we are using python 2.X
    import urllib
else:#if we are using python 3.X
    import urllib.request as urllib

results_file1="bad_news.csv"#file where we save the results
 
results_file2="good_news.csv"#file where we save the results

url1='https://covid.ourworldindata.org/data/full_data.csv'#link from W.H.O 

def read_results(results):#this function opens the "results.csv" file and load the results then return the lines except for the first one
    f = open(results,'r')
    lines = f.readlines()[1:]
    f.close()
    return lines


url2="https://data.humdata.org/hxlproxy/data/download/time_series-ncov-Recovered.csv?dest=data_edit&filter01=explode&explode-header-att01=date&explode-value-att01=value&filter02=rename&rename-oldtag02=%23affected%2Bdate&rename-newtag02=%23date&rename-header02=Date&filter03=rename&rename-oldtag03=%23affected%2Bvalue&rename-newtag03=%23affected%2Brecovered%2Bvalue%2Bnum&rename-header03=Value&filter04=clean&clean-date-tags04=%23date&filter05=sort&sort-tags05=%23date&sort-reverse05=on&filter06=sort&sort-tags06=%23country%2Bname%2C%23adm1%2Bname&tagger-match-all=on&tagger-default-tag=%23affected%2Blabel&tagger-01-header=province%2Fstate&tagger-01-tag=%23adm1%2Bname&tagger-02-header=country%2Fregion&tagger-02-tag=%23country%2Bname&tagger-03-header=lat&tagger-03-tag=%23geo%2Blat&tagger-04-header=long&tagger-04-tag=%23geo%2Blon&header-row=1&url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_19-covid-Recovered.csv"

def download_results1():#this function downloads the daily updated results from the link above and saves it as "results.csv"
    try:
     urllib.urlretrieve(url1,results_file1)
    except:
     time.sleep(1)
     download_results1()

def download_results2():
    try:
     urllib.urlretrieve(url2,results_file2)
    except:
     time.sleep(1)
     download_results2()



def download_results():#this function downloads the daily updated results from the link above and saves it as "results.csv"
    download_results1()
    download_results2()

results1=[]

results2=[]

dates=[]

countries=[]

updating=False

class refresher(threading.Thread):#this function updates the "results.csv" file
 def run(self):
  global updating
  if updating==False:
   updating=True
   updater=messagebox.askyesno("Warning","Yes?")
   if updater==True:
    if os.path.exists(results_file1):
     os.remove(results_file1)
    if os.path.exists(results_file2):
     os.remove(results_file2)
    global dates_combobox
    global countries_combobox
    global dates
    global countries
    download_results()
    global results1
    global results2
    results1=read_results(results_file1)
    results2=read_results(results_file2)
    dates=[]
    countries=[]
    for line in results1:
        x=line.split(',')
        x[0]=datetime.datetime.strptime(x[0], '%Y-%m-%d').strftime('%d/%m/%y')#change date format from "YEAR-MONTH-DAY" to "DAY/MONTH/YEAR"
        if x[0] not in dates:
            dates.append(x[0])
        if x[1] not in countries:
            countries.append(x[1])
    dates.sort(key = lambda date: datetime.datetime.strptime(date, '%d/%m/%y'))#sort the list of dates
    countries.sort()#sort the list of countries
    dates_combobox.current(len(dates)-1)#set the default value of the "dates_combobox" to the latest available date
    countries_combobox.current(countries.index("Tunisia"))#set the default value of the countries_combobox to "Tunisia"
    updating=False
    main2 = Toplevel()
    Label(main2, text = "         ",font=( 500)).grid(row=0,column=2)
    Label(main2, text = "         ",font=( 500)).grid(row=1,column=0)
    Label(main2, text = "Your data has been updated .",font=( 500)).grid(row=1,column=1)
    Label(main2, text = "         ",font=( 500)).grid(row=1,column=2)
    Label(main2, text = "         ",font=( 500)).grid(row=2,column=2)
   else:
    updating=False
  else:
    main2 = Toplevel()
    Label(main2, text = "         ",font=( 500)).grid(row=0,column=2)
    Label(main2, text = "         ",font=( 500)).grid(row=1,column=0)
    Label(main2, text = "You can't run more than 1 update !",font=( 500)).grid(row=1,column=1)
    Label(main2, text = "         ",font=( 500)).grid(row=1,column=2)
    Label(main2, text = "         ",font=( 500)).grid(row=2,column=2)

def refresh_results():
    refresher().start()

def fetch_results():
    global dates
    global countries
    global results1
    global results2
    results1=read_results(results_file1)
    results2=read_results(results_file2)
    dates=[]
    countries=[]
    for line in results1:
        x=line.split(',')
        x[0]=datetime.datetime.strptime(x[0], '%Y-%m-%d').strftime('%d/%m/%y')
        if x[0] not in dates:
            dates.append(x[0])
        if x[1] not in countries:
            countries.append(x[1])
    dates.sort(key = lambda date: datetime.datetime.strptime(date, '%d/%m/%y'))
    countries.sort()

if not os.path.exists(results_file1):#if the  results file is not in the directory then we should download it !!
    download_results1()

if not os.path.exists(results_file2):#if the  results file is not in the directory then we should download it !!
    download_results2()

recovered=None
newcases=None
newdeaths=None
totalcases=None
totaldeaths=None
dates_combobox=None
countries_combobox=None

def search():#search in the loaded results
    global newcases
    global newdeaths
    global totalcases
    global totaldeaths
    global recovered
    a= countries_combobox.get()
    if (a.strip())=="" or (a not in countries):#if we provide empty string or a value that does not exist in the coutries' list
        a="Tunisia"
        countries_combobox.current(countries.index("Tunisia"))
    b=dates_combobox.get()
    if (b.strip()=='') or (b not in dates):#if we provide empty string or a value that does not exist in the coutries' list
        #b=dates[-1]
        b=dates_combobox.current(len(dates)-1)
    try:
        b=datetime.datetime.strptime(b, '%d/%m/%y').strftime('%Y-%m-%d')#set the date's format to the original format
    except:
        b=dates[-1]
        b=dates_combobox.current(len(dates)-1)

    d=a
    if d.strip()=="United States":
        d="US"
    recov=0
    if d=="World":
     for x in results2:
        if (b in x):
            x=x.split(',')
            for i in x:
                if i.strip()=='':
                    x[x.index(i)]='0'
            recov+=int(x[-1].strip())
    else:
     for x in results2:
        if (d in x) and (b in x):
            x=x.split(',')
            for i in x:
                if i.strip()=='':
                    x[x.index(i)]='0'
            recov+=int(x[-1].strip())
    recovered.set(str(recov))
    for x in results1:
        if (a in x) and (b in x):
            x=x.split(',')
            for i in x:
                if i.strip()=='':
                    x[x.index(i)]='0'
            newcases.set(x[2])
            newdeaths.set(x[3])
            totalcases.set(x[4])
            totaldeaths.set(x[5].strip())

fetch_results()

main = Tk()

main.configure(background='light sky blue')
Label(main, text = "",background='light sky blue').grid(row=0)
Label(main, text = "Date:",background='light sky blue',font=( 500)).grid(column=1,row=1)

dates_combobox = ttk.Combobox(main, values=dates,width = 15,font=( 500))
dates_combobox.grid(row=1, column=2)
Label(main, text = "Country:",background='light sky blue',font=( 500)).grid(column=3,row=1)
dates_combobox.current(len(dates)-1)

countries_combobox = ttk.Combobox(main, values=countries,width = 15,font=( 500))
countries_combobox.grid(row=1, column=4)
countries_combobox.current(countries.index("Tunisia"))

Button(main, text='Search', command=search,font=( 500), height = 1, width = 10).grid(row=1, column=5, sticky=W, pady=4)

Label(main, text = "",background='light sky blue',font=( 500)).grid(column=6,row=5)

Label(main, text = "",background='light sky blue').grid(row=2)
Label(main, text = "",background='light sky blue').grid(row=3)

Label(main, text = "        New Cases        ",background='light sky blue',font=( 500)).grid(column=1,row=4)
newcases = StringVar()
newcases.set('0' )
var_newcases = Label(main, textvariable = newcases,background='light sky blue',font=( 500)).grid(row=6,column=1)

Label(main, text = "        New Deaths        ",background='light sky blue',font=( 500)).grid(column=2,row=4)
newdeaths = StringVar()
newdeaths.set('0' )
var_newcases = Label(main, textvariable = newdeaths,background='light sky blue',font=( 500)).grid(row=6,column=2)

Label(main, text = "        Total Cases        ",background='light sky blue',font=( 500)).grid(column=3,row=4)
totalcases = StringVar()
totalcases.set('0' )
var_totalcases = Label(main, textvariable = totalcases,background='light sky blue',font=( 500)).grid(row=6,column=3)

Label(main, text = "        Total Deaths        ",background='light sky blue',font=( 500)).grid(column=4,row=4)
totaldeaths = StringVar()
totaldeaths.set('0' )
var_totaldeaths = Label(main, textvariable = totaldeaths,background='light sky blue',font=( 500)).grid(row=6,column=4)

Label(main, text = "        Recovered        ",background='light sky blue',font=( 500)).grid(column=5,row=4)
recovered = StringVar()
recovered.set('0' )
var_recovered = Label(main, textvariable = recovered,background='light sky blue',font=( 500)).grid(row=6,column=5)

Label(main, text = "",background='light sky blue',font=( 500)).grid(row=7)

Button(main, text='Update', command=refresh_results,font=( 500), height = 1, width = 10).grid(row=8, column=5, sticky=W, pady=4)

Label(main, text = "",background='light sky blue',font=( 500)).grid(row=9)

mainloop()
