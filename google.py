import urllib, json, requests
import pandas as pd

# Grabbing and parsing JSON data
## INPUT : latitude, longitude, radius (miles), 
## types (https://developers.google.com/places/web-service/search), key
## OUTPUT : Grabs JSON object from Google, turns it into nested array
def GooglePlace(lat,lng,radius,types,key):
    #making the url
    AUTH_KEY = key
    LOCATION = str(lat) + "," + str(lng)
    RADIUS = radius * 1609.344 # convert to meters (Google requirement)
    TYPES = types
    googUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
           '?location=%s'
           '&radius=%s'
           '&types=%s'
           '&sensor=false&key=%s') % (LOCATION, RADIUS, TYPES, AUTH_KEY)
    #grabbing JSON result
    response = requests.get(googUrl)
    jsonData = response.json()
    return jsonData


root = 'C:/Users/markl/OneDrive/Documents/GG/'
fn = 'goody_data.xlsx'
newfn = 'goody_google.xlsx'
ggplaces = pd.read_excel(root+fn)

# API key

MyKey = 'xxxx'



# Google types to use
google_types_keyword = ['liquor_store','liquor_store&keyword=Total Wine' ,'liquor_store&keyword=Spec','convenience_store','gas_station']

# Names for new columns
new_columns_keyword = ['liqstore','totalwine','specs','convenience','gas']

# Set search radius
rad = [1,3,5,10]

# Initialize search 
search = {}

# Loop through all google types
for r in range(len(rad)):
    for idx in range(len(google_types_keyword)):
        ggplaces[new_columns_keyword[idx]+str(rad[r])]=0  
        for row in ggplaces.iterrows():    # Loop through test stores
            index,data = row
            search[index] = GooglePlace(lat=data['lat'],lng=data['lng'],radius=rad[r],types=google_types_keyword[idx],key=MyKey)
            ggplaces.loc[index,[new_columns_keyword[idx]+str(rad[r])]] = len(search[index]['results'])

ggplaces.to_excel(root+newfn)