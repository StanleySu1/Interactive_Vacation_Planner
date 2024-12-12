import requests
from bs4 import BeautifulSoup
import os
import re
import json

# Get the current script directory
script_dir = os.path.dirname(__file__)
# Construct the full path to the file
amsterdam_path = os.path.join(script_dir, "../data/sources/yelp/amsterdam.txt")
amsterdam_path = os.path.abspath(amsterdam_path)

barcelona_path = os.path.join(script_dir, "../data/sources/yelp/barcelona.txt")
barcelona_path = os.path.abspath(barcelona_path)

lisbon_path = os.path.join(script_dir, "../data/sources/yelp/lisbon.txt")
lisbon_path = os.path.abspath(lisbon_path)

london_path = os.path.join(script_dir, "../data/sources/yelp/london.txt")
london_path = os.path.abspath(london_path)

nyc_path = os.path.join(script_dir, "../data/sources/yelp/nyc.txt")
nyc_path = os.path.abspath(nyc_path)

paris_path = os.path.join(script_dir, "../data/sources/yelp/paris.txt")
paris_path = os.path.abspath(paris_path)

rome_path = os.path.join(script_dir, "../data/sources/yelp/rome.txt")
rome_path = os.path.abspath(rome_path)

vegas_path = os.path.join(script_dir, "../data/sources/yelp/vegas.txt")
vegas_path = os.path.abspath(vegas_path)

output_path = os.path.join(script_dir, "../data/scraped/yelp/vegas.jsonl")  # Output JSONL file
output_path = os.path.abspath(output_path)

# Open the output file for writing
with open(output_path, 'w') as output_file:
    with open(vegas_path, 'r') as file:
        for line in file:
            r = requests.get(line.strip())
            soup = BeautifulSoup(r.text, 'html.parser')

            # Initialize attraction data dictionary
            attraction_data = {
                "name": None,
                "category": None,
                "hours": None,
                "address": None,
                "rating": 0,
                "number_of_reviews": 0,
                "reviews": [],
            }

            #Extract title 
            div_tag = soup.find('div', class_='y-css-74ugvt')
            while div_tag is None:
                r = requests.get(line.strip())
                soup = BeautifulSoup(r.text, 'html.parser')
                div_tag = soup.find('div', class_='y-css-74ugvt')
            title_tag = div_tag.find('h1', class_='y-css-olzveb')
            title = title_tag.text
            attraction_data["name"] = title if title_tag else None
            print(title)

            #Extract review score
            span_tag = soup.findAll('span', class_="y-css-1jz061g")
            # for span in span_tag:
            #     print(span.text)
            # review_score = span_tag[0].text.strip()
            try: 
                attraction_data["rating"] = float(span_tag[0].text.strip()) if 0 < len(span_tag) else 0
                #Extract type of attraction
                # outer_span = soup.find('span', class_='y-css-1cafv3i')
                # inner_span = outer_span.find('span', class_='y-css-1jz061g')
                # a_tag = inner_span.find('a', class_='y-css-1ijjqcc')
                # attraction_type = span_tag[1].text.strip()
                attraction_data["category"] = span_tag[1].text.strip() if 1 < len(span_tag) else None
                # print(attraction_type)
                #Extract operating hours
                # outer_span = soup.find('span', class_='y-css-qavbuq')
                # inner_span = outer_span.find('span', class_='y-css-1jz061g')
                # while inner_span is None:
                #     r = requests.get(line.strip())
                #     soup = BeautifulSoup(r.text, 'html.parser')
                #     outer_span = soup.find('span', class_='y-css-qavbuq')
                #     inner_span = outer_span.find('span', class_='y-css-1jz061g')
                # operating_hours = span_tag[2].text.strip()
                attraction_data["hours"] = span_tag[2].text.strip() if 2 < len(span_tag) else None
            except:
                attraction_data["category"] = span_tag[0].text.strip() if 0 < len(span_tag) else None
                attraction_data["hours"] = span_tag[1].text.strip() if 1 < len(span_tag) else None
            # print(operating_hours)


            #Extract number of reviews 
            a_tag = soup.find('a', class_="y-css-1x1e1r2")
            reviews_text = a_tag.text.strip()  # "(1.2k reviews)"
            reviews_count = reviews_text.split()[0][1:]
            try: 
                if reviews_count.endswith('k'):
                    reviews_count = float(reviews_count[:-1]) * 1000
                else:
                    float(reviews_count)
            except:
                reviews_count = 0
            # print(reviews_count)
            attraction_data["reviews_count"] = reviews_count

            #Extract address
            p_tag = soup.find('p', class_='y-css-jbomhy')
            #Some attractions don't have addresses on yelp 
            if p_tag is not None:
                address = p_tag.text
                attraction_data["address"] = address if p_tag else None
            # print(address)

            # Extract reviews in front page
            # Find all <p> elements with the specific class for reviews
            review_divs = soup.findAll('p', class_="comment__09f24__D0cxf y-css-1wfz87z")
            rating_divs = soup.findAll('div', class_='y-css-dnttlc')
            date_pattern = re.compile(r'^[A-Za-z]{3} \d{1,2}, \d{4}$')
            date_spans = soup.findAll('span', class_='y-css-1d8mpv1')

            # reviews = []
            for review_div, rating_div, date_span in zip(review_divs, rating_divs, date_spans):
                review_span = review_div.find('span', class_="raw__09f24__T4Ezm")  # Look for the <span> element inside <p>
                rating_aria_label = rating_div.get('aria-label')
                date_text = date_span.text.strip()
                if review_span and rating_aria_label and date_pattern.match(date_text):  # Ensure the <span> element exists
                    attraction_data['reviews'].append({
                        "review": review_span.text,
                        "rating": rating_aria_label.split()[0],
                        "visited": date_text
                    }) 
                    # reviews.append(span.text)  # Append the review text
                    # print(span.text)  # Print the review text

            # rating_divs = soup.findAll('div', class_='y-css-dnttlc')
            # for div in rating_divs:
            #     aria_label = div.get('aria-label')
            #     if aria_label:
            #         print(aria_label.split()[0])

            # date_pattern = re.compile(r'^[A-Za-z]{3} \d{1,2}, \d{4}$')
            # date_spans = soup.findAll('span', class_='y-css-1d8mpv1')
            # for span in date_spans:
            #     text = span.text.strip()
            #     if date_pattern.match(text):
            #         print(text)
            output_file.write(json.dumps(attraction_data) + "\n")