from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import json
import time

base_dir = os.getcwd() + "\\locations"

def run_driver(input_url):
    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    driver.get(input_url)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, 'html.parser')
    driver.close()

    return soup

soup = run_driver("https://travel.usnews.com/destinations/")
location_list = list(zip(
    ["https://travel.usnews.com" + link.find("a")["href"] for link in soup.find_all("li", class_ = "List__ListItem-rhf5no-1 jYdEtR")],
    [link.find("a").string for link in soup.find_all("li", class_ = "List__ListItem-rhf5no-1 jYdEtR")]
))

for ind_location in location_list:

    soup = run_driver(ind_location[0])
    location_descriptions = list(dict.fromkeys([description.replace(u'\xa0', u' ') for description in [paragraph.getText() for paragraph in soup.find_all("p")] if len(description) > 150]))


    formatted_location = re.sub('[^A-Za-z0-9]+', ' ', ind_location[1]).lower().replace(" ", "_")
    location_dir = base_dir + "\\" + formatted_location
    if not os.path.exists(location_dir):
        os.makedirs(location_dir)
    with open(location_dir +  "\\" + formatted_location + ".json", "w", encoding="utf-8") as outfile:
        json.dump({"name": ind_location[1], "description": location_descriptions}, outfile)

    soup = run_driver(ind_location[0] + "Things_To_Do/")
    attraction_links = list(dict.fromkeys(["https://travel.usnews.com" + divider.find("a")["href"] for divider in soup.find_all("div", class_ = "HeightTogglerTour__FlexColumn-sc-433q4t-6 bgXfoF")]))

    for attraction in attraction_links:
        try:
            soup = run_driver(attraction)
            attraction_name = soup.find_all("h1", class_ = "Heading-sc-1w5xk2o-0 ebVwpp")[0].getText()
            attraction_html = f"<!-- {attraction_name} -->" + str(soup.find_all("section", class_ = "travel-guide-profile-base__Section-nglwm1-6 inbIpv")[0])
        except IndexError:
            time.sleep(5)
            soup = run_driver(attraction)
            attraction_name = soup.find_all("h1", class_ = "Heading-sc-1w5xk2o-0 ebVwpp")[0].getText()
            attraction_html = f"<!-- {attraction_name} -->" + str(soup.find_all("section", class_ = "travel-guide-profile-base__Section-nglwm1-6 inbIpv")[0])

        formatted_attraction = re.sub('[^A-Za-z0-9]+', ' ', attraction_name).lower().replace(" ", "_")
        with open(location_dir +  "\\" + formatted_attraction + ".html", "w", encoding="utf-8") as outfile:
            outfile.write(attraction_html)