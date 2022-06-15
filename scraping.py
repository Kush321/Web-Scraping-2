from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome(
    executable_path=r"/Users/kush/Desktop/Web Scraping/chromedriver")
browser.get(start_url)
time.sleep(10)
header = ["Name", "Light-Years From Earth", "Planet Mass", "Stellar Magnitude", "Discovery Date", "Planet Type",
    "Discovery Date", "Mass", "Planet Radius", "Orbital Radius", "Orbital Period", "Eccentricity", "Direction Method"]
planet_data = []
new_planet_data = []


def scrape():
    for i in range(0, 201):
            soup = BeautifulSoup(browser.page_source, "html.parser")
            for j in soup.find_all("ul", attrs={"class", "exoplanet"}):
                li = j.find_all("li")
                el = []
                for f, r in enumerate(li):
                    if f == 0:
                        el.append(r.find_all("a")[0].contents[0])
                    else:
                        try:
                            el.append(r.contents[0])
                        except:
                            el.append("")
                l = li[0]
                el.append("https://exoplanets.nasa.gov" +
                          l.find_all("a", href=True)[0]["href"])
                planet_data.append(el)
            browser.find_element_by_xpath(
                '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            with open("data.csv", "w") as f:
                x = csv.writer(f)
                x.writerow(header)
                x.writerows(planet_data)
            
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp = []
        for i in soup.find_all("tr",attrs={"class","fact_row"}):
            v = i.find_all("td")
            for s in v:
                try:
                    temp.append(s.find_all("div",attrs={"class","value"})[0].contents[0])
                except:
                    temp.append("")
        new_planet_data.append(temp)
    except:
        time.sleep(3)
        scrape_more_data(hyperlink)
    with open("data.csv","w") as f:
        x = csv.writer(f)
        x.writerow(header)
        x.writerows(planet_data)
scrape()
