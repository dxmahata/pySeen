'''
Created on Dec 10, 2014

@author: Dxmahata
'''

__author__ = "Debanjan Mahata"

import requests
import sys
import json

API_REQUEST_COUNT = 0

#Base Url for calling Seen API
BASE_URL = "http://api.seen.co/v0.1"

#Setting up the endpoints
ENDPOINTS = {}

#setting up events endpoint
ENDPOINTS["events"] = {}
#setting up endpoint for searching events from the Seen.co event database
ENDPOINTS["events"]["search"] = "/events/search"
#setting up endpoint for requesting events of type "popular"
ENDPOINTS["events"]["popular"] = "/events/popular"
#setting up endpoint for requesting events of type "recent"
ENDPOINTS["events"]["recent"] = "/events/recent"
#setting up endpoint for requesting events of type "happening"
ENDPOINTS["events"]["happening"] = "/events/happening"
#setting up endpoint for requesting events of type "mine"
ENDPOINTS["events"]["mine"] = "/events/mine"


#setting up create endpoint
ENDPOINTS["create"] = "/create"


#setting up event endpoint
ENDPOINTS["event"] = "/event"

API_KEY = ""


def setApiKey():
    """It loads the API key from api_key.txt"""
    global API_KEY
    try:
        fp = open("api_key.txt")
        API_KEY = fp.readline()
        if API_KEY == "":
            print("The api_key.txt file appears to be blank")
            print("If you do not have an API Key from Seen.co, please get it from: http://www.developer.seen.co")
            sys.exit(0)
                
        fp.close()
    except IOError:
        print('API Key not found! Please create and fill up api_key.txt file in the same directory which contains the SeenAPI module')
        print('If you do not have an API Key from Seen.co, please get it from: http://www.developer.seen.co')
        sys.exit(0)
    except Exception as e:
        print(e)
        
        
def getEvents(flavor,query="",limit=10):
    """
    flavor can be any one of the following:
    1. search
    2. popular
    3. recent
    4. happening
    5. mine
    
    1. search:
    /events/search/:keyword
    Search events by keyword(s) or hashtag (no need to add #).
    Parameter        Description
    keywords    required    Space-separated list of keywords to search for.
    limit    optional    Maximum number of results; default = 10, max = 20.
    Request example:
    http://api.seen.co/v0.1/events/search/electric%20zoo%20festival%20ezoo5?api_key=YOUR_API_KEY
    
    2. All other types: popular, recent, happening, mine (request_type)
    /events/:request_type
    Returns a list of events based on the requested type from the list below
    Type    Description
    popular    A set of popular events on Seen, based on our algorithm
    recent    Events from the last two weeks
    happening    Events ongoing at the time of the call
    upcoming    Events that have not yet started
    mine    Events created by the developer associated with the provided key

    Parameter        Description
    type    required    One type from the list above
    limit    optional    Maximum number of results; default = 10, max = 20.
    Request example:
    http://api.seen.co/v0.1/events/popular?api_key=YOUR_API_KEY
    
    """
    global API_REQUEST_COUNT
    setApiKey()
    #Make sure this request supports this flavor
    if flavor not in ENDPOINTS['events']:
        return { 'status':'ERROR', 'statusInfo':'events for the ' + flavor + ' is not available. Please enter one of these 1.search, 2.popular, 3.recent, 4.happening, 5.mine' }
    
    if flavor == "search" and query == "":
        print "Please provide a query string in the getEvents(flavor,query="",options={}) parameter"
        sys.exit(0)
        
    payload = {}
    payload["api_key"] = API_KEY
    payload["limit"] = limit
    
  
    
    getUrl = BASE_URL+ENDPOINTS["events"][flavor]+"/"+str(query)

    try:
        r = requests.get(getUrl,params=payload)
        API_REQUEST_COUNT +=1
        
        return json.loads(r.text)
        
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }

def createEvent(keywords,options={}):
    """
    POST /create/:keywords
    This endpoint lets you enter new events in our system. Once an event has been successfully created, you will need to wait a few minutes in order for our engine to crawl all tweets and images and analyze them. Please consider that it could take a few minutes (depending on the number of events currently tracked) for the data to be updated.
    Every developer can create a maximum of 5 events an hour, and every event can have a maximum duration of two days. You can create events for past time periods but the results will vary - anything past 7 days will have incomplete tweets and limited Instagram photos.
    Parameter        Description
    keywords    required    Spaces-separated list of hashtags that define the event. These will be treated as hashtags, no need to add a # prefix. Please consider that our engine will consider all tweets/instagrams containing either one of the specified keywords ("OR semantics"). We will drop any event that is tracking non-specific hashtags, like #fun, #happiness, #love or other joyful or volume-heavy tags.
    start_date    optional    Start date (UTC) of the event in the '%FT%T' format (yyyy-mm-ddThh:mm:ss)
    end_date    optional    End date (UTC) of the event in the '%FT%T' format (yyyy-mm-ddThh:mm:ss)
    tz    optional    The UTC offset (timzone) for the event location, e.g. "+2.0". Defaults to "-5.0".
    location    optional    Free-text string, the venue/location of the event take place, e.g. New York, NY.
    POST Request example:
    POST http://api.seen.co/v0.1/create/hackny?api_key=YOUR_API_KEY&start_time=2013-09-27T13:00:00&end_time=2013-09-28T15:00:00&title=Hack%20NY&location=New%20York,%20NY&tz=-5.0
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    for option in options:
        payload[option] = options[option]
    
    postUrl = BASE_URL+ENDPOINTS["create"]+"/"+str(keywords)
    
    try:
        r = requests.post(postUrl,params=payload)
        print r.url
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }

def getEventDescription(eventLocator):
    """
    /event/:locator
    Retrieve an event's descriptive data and statistics by its locator. If successful, the response will contain an Event object.
    Request example:
    http://api.seen.co/v0.1/event/hackny-hackathon-nyu-courant-institute-new-york-ny-2012-3441?api_key=YOUR_API_KEY
    """
    
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }
    
    
def getEventHighlights(eventLocator):
    """
    /event/:locator/highlights
    Retrieve an array of highlights for the event. Request example:
    http://api.seen.co/v0.1/event/hackny-hackathon-nyu-courant-institute-new-york-ny-2012-3441/highlights?api_key=YOUR_API_KEY
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/highlights"
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }
    
    
def getEventHighlightObject(eventLocator,objectId):
    """
    /event/:locator/highlight/:id
    Returns a specific highlight object by its id.
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/highlight/"+str(objectId)
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }


def getEventRecentHighlights(eventLocator):
    """
    /event/:locator/highlights/recent
    Returns the most recent highlight objects for this event.
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/highlights/recent"
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }


def getEventHistogram(eventLocator):
    """
    /event/:locator/histogram
    Returns an array of timelights, each of them contains statistics about a particular time bucket, different timelights' time ranges don't overlap. This is the typical schema for a timelight:
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/histogram"
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }
    
def searchEventByTime(eventLocator,startTime,endTime):
    """
    /event/:locator/search/:search_type
    You can use this endpoint for retrieving an event's items according to their publishing time. It returns an array of items. Not that response is capped at 1000 items.
    Search type    Description
    /time/:start/:end    Specify start and end times with the "%FT%T%z" format.(yyyy-nn-ddThh:mm:ss+hh:mm).

    Query example:
    http://api.seen.co/v0.1/event/electric-run-new-york-brooklyn-ny-2013-9865/search/time/2013-09-27T23:00:00-04:00/2013-09-28T01:00:00-04:00/?api_key=YOUR_API_KEY
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/search/time/"+str(startTime)+"/"+str(endTime)
    
    try:
        r = requests.get(getUrl,params=payload)
    
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }


def searchEventByTerm(eventLocator,terms):
    """
    /event/:locator/search/:search_type
    You can use this endpoint for retrieving an event's items according to their contained terms. It returns an array of items. Not that response is capped at 1000 items.
    Search type    Description
        /terms/:terms    :terms is a comma-separated list of terms.
    Query example:
    http://api.seen.co/v0.1/event/electric-run-new-york-brooklyn-ny-2013-9865/search/terms/brooklyn?api_key=YOUR_API_KEY
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/search/terms/"+str(terms)
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }

def getEventTopUsers(eventLocator):
    """
    /event/:locator/top_users
    Retrieves the top users for this event. Response example:
    """
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/top_users/"
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }

def getEventTopItems(eventLocator):
    """/event/:locator/top_items
    Returns an array containing this event's items. with the highest social score.
    """
    
    global API_REQUEST_COUNT
    setApiKey()
    
    payload = {}
    payload["api_key"] = API_KEY
    
    getUrl = BASE_URL+ENDPOINTS["event"]+"/"+str(eventLocator)+"/top_items/"
    
    try:
        r = requests.get(getUrl,params=payload)
        
        API_REQUEST_COUNT += 1
        return json.loads(r.text)
    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }







