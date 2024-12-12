from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import json
import time
import numpy as np
import pandas as pd

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

json_files = []
for dirpath, _, filenames in os.walk(base_dir):
    for filename in filenames:
        if filename.endswith(".json"):
            json_files.append(os.path.join(dirpath, filename))

city_names = []
for ind_file in json_files:
    with open(ind_file) as file:
        json_content = json.load(file)
    city_names.append(json_content["name"])
pd.DataFrame(city_names, columns = ["Name"]).to_csv('city_names.csv', index=False)

html_files = []
for dirpath, _, filenames in os.walk(base_dir):
    for filename in filenames:
        if filename.endswith(".html"):
            html_files.append(os.path.join(dirpath, filename))

attraction_information = pd.DataFrame(columns = ["Name", "Price", "Hours", "Keywords", "Estimated Time to Spend", "Score", "Description", "Image"])
image_pattern = re.compile("https:.*?(?:png|jpg|svg)")
index = 0

for ind_file in html_files:
    with open(ind_file, "r", encoding = "utf8") as file:
        html_content = file.read()
    comment = re.search('<!--(.*?)-->', html_content)
    attraction_name = comment.group(1).strip()

    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all(["p", "span", "b"])
    entire_text = [p.text for p in paragraphs]

    attraction_price = entire_text[entire_text.index("Price & Hours") + 1] if "Price & Hours" in entire_text else ""
    attraction_hours = entire_text[entire_text.index("Price & Hours") + 2] if "Price & Hours" in entire_text else ""
    attraction_keywords = entire_text[entire_text.index("Type") - 1].replace("Type", "").strip() if "Type" in entire_text else ""
    attraction_time = entire_text[entire_text.index("Time to Spend") - 1].replace("Time to Spend", "").strip() if "Time to Spend" in entire_text else ""
    attraction_score = str(np.mean(
        [
            float(entire_text[entire_text.index("Value ") + 1]) if "Value " in entire_text else 0,
            float(entire_text[entire_text.index("Facilities ") + 1]) if "Facilities " in entire_text else 0,
            float(entire_text[entire_text.index("Atmosphere ") + 1]) if "Atmosphere " in entire_text else 0
        ]
    ))
    attraction_description = " ".join(dict.fromkeys([description.replace(u'\xa0', u' ') for description in entire_text if len(description) > 150]))

    images = soup.find_all('img')
    try:
        image_url = image_pattern.findall(images[0]["srcset"])[-1]
    except:
        image_url = ""

    new_record = pd.DataFrame(
        {
            "Name": attraction_name,
            "Price": attraction_price,
            "Hours": attraction_hours,
            "Keywords": attraction_keywords,
            "Estimated Time to Spend": attraction_time,
            "Score": attraction_score,
            "Description": attraction_description,
            "Image": image_url,
            "Filepath": ind_file
        }, index = [0])
    attraction_information = pd.concat([attraction_information, new_record])

    index = index + 1

attraction_information.reset_index(drop=True, inplace=True)
attraction_information["Hours"] = attraction_information["Hours"].replace("Details", "")
attraction_information.to_csv('attraction_information.csv', index=False)