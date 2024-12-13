# CS 410 Final Project - Interactive Vacation Planner

## Members

- Kelvin Chong (kvchong2)
- Stanley Su (ssu603)
- Bowen Shan (bs7)

## Presentation

## Description
Vacation planning can be a complicated and time-consuming process for travelers. This project aims to simplify this process. We built a web application to allow users to interact with a chat bot to help find attractions that a user is interested in.
A traveler can provide details, such as the number of travel days, intended destinations, and attraction interests, to receive a list of recommended attractions. These details will then be used to build a user profile and design our query.
We developed crawlers to scour and index travel websites such as TripAdvisor, Yelp and US News. Information of particular interest includes attraction types, user reviews/ratings, operating hours, costs, and addresses.

## Implementation
Our application is a trip-planning helper that recommends attractions in a specified city that a visitor may be interested in. We envisioned an application that would first converse with a user in a “ChatGPT-like” interface to discover a user’s interests and destination. The app would then perform a search to find suitable attractions based on these interests and present them to the user.

Our project consists of three components. The first component was to retrieve data for various attractions, and we needed enough data to store as a collection of queryable documents. We embarked on scraping several well-known websites such as Yelp, TripAdvisor, and US News & World. However, we encountered many issues with bot-blocking software, which hindered our ability to properly fetch the data. As such, we were not able to automate the data collection process as we envisioned but instead had to manually retrieve relevant information from the web pages. As a result, we only managed to retrieve and clean a more limited dataset than originally proposed. We used SQLite to store our data, from which text data can be filtered and fed into a retrieval system.

The second component was our document retrieval. We imagined a RAG-style approach where we would query against our document pool for relevant attractions with BM25, ranking the attractions against the user query. This prioritized attractions with descriptions/reviews that were both unique and relevant to the user’s interests. As such, we added a pre-prompting step for an LLM to examine the user’s query and extract their interests that could be searched. We filtered the results by city name and then used BM25 to do a term matching search against the user interests. The result is a re-ranked list of the top 10 results that we added to the user’s original prompt.  This was run through an LLM to generate a response.  In addition, we added a post-LLM prompt that would examine the output and return a list of mentioned attractions so that we can display images of the attractions in another widget.

The final component is the user interface. Our ambition was to eventually create a mobile on-the-go application, but we used a web application instead due to resource constraints. The user interface consists of a text field where the user can enter their questions and interact with the LLM. There is a response window that streams the response from the LLM. Finally, a list widget displays all of the mentioned attractions that the user can click on to display more details.

### Application Environment
We used Python to fetch and scrape the websites, and the results were stored in a local SQLite database. We used an LLM repository called Ollama (https://ollama.com) that provides a small free model that we can run on our computers. We used uvicorn for our HTTP and websocket server. Our user interface is a React application.

### Web Scraping
The scripts we used to scrape attractions data from TripAdvisor/Yelp/US News are located under the [src/](src/) directory. These files first fetched the webpages that we were interested in and downloaded their html content into the data/sources/ directory. We then scraped the text off the pages and stored them as CSV or JSONL files under [data/scraped/](data/scraped/). These files were then ingested into our SQLite database.

### Server
The core of our application is on the server under the [server/](server/) directory.  It has a “server.py” entry point which starts off the uvicorn WSGI server.  Files to handle the various web requests are in the [server/handler/](server/handler/) directory.

The [server/handler/http_files.py](server/handler/http_files.py) file is used to deliver the client html/javascript/css files to a web browser.
The [server/handler/ws.py](server/handler/ws.py) file is the main file used to handle the interaction between the client, receiving the user’s request and then streaming the LLM response through a websocket.  In the ```ws.py``` file, there is a function called ```augment_city_search()```.  This is a pre-prompt that uses the LLM to determine what city and interests a user has, based on the current interaction with the user.  This function then calls a search function in [server/handler/search.py](server/handler/search.py) that does the search.  The results are stuffed into the prompt that is sent to the LLM.  After the LLM is done, we call a function called ```get_mentioned_cities()``` that does post-prompting to extract the attractions mentioned in the conversation.  We prompt the LLM to return the results in JSON format so that we can use it in the user interface.

The [server/handler/search.py](server/handler/search.py) file handles retrieving a ranked list of potential attractions. We first use SQL to fetch an initial list of attractions by the city name and description. We then tokenized and normalized the description and user query to improve term matching similarity by consolidating variations of the same word. After doing so, we initialized the BM25 object with the attraction description and user interest to score all the attractions’ description based on their term frequency, unique terms, and document length in comparison to the relevant terms. After doing this, we ranked, reformatted, and returned the top 10 results so as to not overload the LLM with irrelevant information. From there, we could retrieve the original database ID to fetch the rest of the attraction information.

### Client
The [client/src/](client/src/) directory contains the source code for the web client.  It is a React application that communicates with the server.  The main channel is a websocket that sends a user’s prompt and receives the replies from the server.  We opted to use a websocket so that we can stream the text as the LLM generates the text to provide user feedback that processing is occurring.  We send the entire conversation to the server to avoid having to maintain a state on the server.  Separately, we make XHR requests to fetch information about individual attractions from the SQLite database.

## Using the Software
### Installation/Running
1. Install required Python libraries: ```pip install -r requirements.txt```
    * If an error occurs while install pysqlite3, please install libsqlite3-dev first: ```sudo apt-get install libsqlite3-dev```
2. Build the react client:
```
cd client
npm install
npm run build
cd ../
```
3. Install ollama from [https://ollama.com/](https://ollama.com/) and follow the instructions for the appropriate OS
    * In a separate CLI instance, run the following: ```ollama serve```
    * Download quantized llama3.2: ```ollama pull llama3.2```
4. Start the server: ```python server/server.py```
5. Open [http://localhost:8000/](http://localhost:8000/) in a web browser.

### Using the Application
If the application is working properly, the chatbot should greet you with the following message: “Where would you like to go?” To get started, prompt the chatbot by providing a potential destination and the interests that you have for that destination. For example:
* “I’d like to find out more about Paris”
* “I’m planning a trip to London”
* “Tell me about the museums in New York City”
* “I’m interested in the casinos in Las Vegas”
* “Plan a trip to Paris with a focus on art and food”

The response of the LLM should be visible in the main window. Feel free to continue interacting with the chatbot to further narrow your search to a few attractions, or ask it to provide you details about a certain location. For example, if you were interested in museums in NY, you could say:
* “I would like to visit a history museum”
* “Tell me more about the Metropolitan Museum of Art”

When the LLM has a better understanding of your interests, a list of attractions will appear on the left and a complete itinerary will be presented. At any time, click on one of the attractions to pull up more details about it.
