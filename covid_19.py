import tkinter as tk
import requests
from bs4 import BeautifulSoup as bs
from plyer import notification
import urllib
from tkinter import *


HEIGHT = 600
WIDTH = 600

url = "https://www.worldometers.info/coronavirus/country/"


class covid:
    def __init__(self, cname):
        self.country = cname
        self.url = url+self.country

    def run(self):

        response = requests.get(self.url)
        data = self.scrapeData(response)
        return data

    def scrapeData(self, response):
        soup = bs(response.content, "html.parser")
        container = soup.find('div', class_="col-md-8")
        # print(container)
        containers = container.find_all(id="maincounter- wrap")
        print(containers)
        listt = [self.country.upper()]
        for _ in containers:
            var = _.find('h1').get_text()
            span = _.find('div', class_="maincounter-number")
            rate = span.get_text().strip("\n")
            final = f"{var}{rate}"
            listt.append(final)

        return listt


if __name__ == "__main__":
    icon = 'covid.ICO'

    def start(varf):
        start = covid(varf)
        data = start.run()
        stri = " \n"
        notification.notify(
            title=f"Covid 19 report for: {data[0]}",
            message=stri.join(data[1:]),
            timeout=20,
            app_icon=icon)


def format_response(coviddata):
    try:
        country = coviddata['country']
        cases = coviddata['cases']
        todayCases = coviddata['todayCases']
        deaths = coviddata['deaths']
        todayDeaths = coviddata['todayDeaths']
        recovered = coviddata['recovered']
        active = coviddata['active']
        critical = coviddata['critical']
        casesPerOneMillion = coviddata['casesPerOneMillion']
        deathsPerOneMillion = coviddata['deathsPerOneMillion']
        totalTests = coviddata['totalTests']
        testsPerOneMillion = coviddata['testsPerOneMillion']

        final_str = " Here's the data you requested : \n country: {} \n cases: {} \n todayCases: {} \n  deaths :{} \n todayDeaths:{}\n recovered :{} \n active:{} \n critical : {} \n casesPerOneMillion : {} \n deathsPerOneMillion: {} \n totalTests :{} \n testsPerOneMillion:{} ".format(
            country, cases, todayCases, deaths, todayDeaths, recovered, active, critical, casesPerOneMillion, deathsPerOneMillion, totalTests, testsPerOneMillion)
    except:
        final_str = 'There was a problem retrieving that information'

    return final_str


def get_coviddata(country):
    url = "https://coronavirus-19-api.herokuapp.com/countries/"+country
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    coviddata = response.json()
    label['text'] = format_response(coviddata)


root = tk.Tk()


canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='2.png')
background_label = tk.Label(root, image=background_image, bd=0)
background_label.place(relwidth=1, relheight=1)


frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Get Data", font=40,
                   command=lambda: get_coviddata(entry.get()))


lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75,
                  relheight=0.6, anchor='n')

label = tk.Label(root, text="Enter a Country name/Get world data",
                 font=('Times', 13, 'bold'), bg="white", bd=2).place(x=80, y=32)


cname = tk.Entry(root, font=40)
cname.pack()
cname.place(relwidth=0.3, relheight=0.044, x=400, y=550)


button = tk.Button(frame, text="Get Data", font=40,
                   command=lambda: get_coviddata(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

btn = tk.Button(root, text="Show Report", command=lambda: start(cname.get()))
btn.place(x=505, y=550)

btn = tk.Label(lower_frame)
btn.place(relwidth=1, relheight=1)

label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

root.mainloop()
