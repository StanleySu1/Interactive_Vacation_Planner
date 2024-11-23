import requests
from bs4 import BeautifulSoup
import os

# Get the current script directory
script_dir = os.path.dirname(__file__)
# Construct the full path to the file
amsterdam_path = os.path.join(script_dir, "../data/sources/yelp/amsterdam.txt")
amsterdam_path = os.path.abspath(amsterdam_path)

with open(amsterdam_path, 'r') as file:
    for line in file:
        r = requests.get(line.strip())
        soup = BeautifulSoup(r.text, 'html.parser')

        #Extract title 
        div_tag = soup.find('div', class_='y-css-74ugvt')
        while div_tag is None:
            r = requests.get(line.strip())
            soup = BeautifulSoup(r.text, 'html.parser')
            div_tag = soup.find('div', class_='y-css-74ugvt')
        title_tag = div_tag.find('h1', class_='y-css-olzveb')
        title = title_tag.text
        print(title)

        #Extract review score
        span_tag = soup.find('span', class_="y-css-1jz061g")
        review_score = span_tag.text.strip()
        print(review_score)

        #Extract number of reviews 
        a_tag = soup.find('a', class_="y-css-1ijjqcc")
        reviews_text = a_tag.text.strip()  # "(1.2k reviews)"
        reviews_count = reviews_text.split()[0][1:]
        if reviews_count.endswith('k'):
            reviews_count = float(reviews_count[:-1]) * 1000
        else:
            float(reviews_count)
        print(reviews_count)

        #Extract operating hours
        outer_span = soup.find('span', class_='y-css-qavbuq')
        inner_span = outer_span.find('span', class_='y-css-1jz061g')
        operating_hours = inner_span.text
        print(operating_hours)

        #Extract type of attraction
        outer_span = soup.find('span', class_='y-css-1cafv3i')
        inner_span = outer_span.find('span', class_='y-css-1jz061g')
        a_tag = inner_span.find('a', class_='y-css-1ijjqcc')
        attraction_type = a_tag.text
        print(attraction_type)

        #Extract address
        p_tag = soup.find('p', class_='y-css-jbomhy')
        #Some attractions don't have addresses on yelp 
        if p_tag is not None:
            address = p_tag.text
        print(address)

        # Extract reviews in front page
        # Find all <p> elements with the specific class for reviews
        divs = soup.findAll('p', class_="comment__09f24__D0cxf y-css-1wfz87z")
        reviews = []
        for div in divs:
            span = div.find('span', class_="raw__09f24__T4Ezm")  # Look for the <span> element inside <p>
            if span:  # Ensure the <span> element exists
                reviews.append(span.text)  # Append the review text
                print(span.text)  # Print the review text