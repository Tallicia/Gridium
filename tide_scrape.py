from requests import get
from bs4 import BeautifulSoup
import json
import re

# '/locations/ac_location_name?query=__VALUE__';
site = 'https://www.tide-forecast.com'

locations = [('Half Moon Bay', 'California', 'CA')]
locations += [('Huntington Beach', '', 'CA')]
locations += [('Providence', 'Rhode Island', 'RI')]
locations += [('Wrightsville Beach', 'North Carolina', 'NC')]

url_list = []
for loc in locations:
    url = '/locations/' + loc[0].replace(' ', '-')
    if len(loc[1]) != 0:
        url += '-' + loc[1].replace(' ', '-')
    url += '/tides/latest'
    url_list.append(url)

loc_daylight_low_tides = {}
for url_loc in url_list:
    scrape = get(site + url_loc)
    if scrape.status_code != 200:
        print('Could not reach the url :', url + url_loc)
        continue
    else:
        print('Loaded url :', url + url_loc)
    soup = BeautifulSoup(scrape.text, 'html.parser')
    cdata = soup.find_all('script', string=re.compile(r'CDATA'))
    cdata_str = str(cdata)
    if len(cdata_str) <= 2:
        print('Expected Data Payload Empty :', url + url_loc)
        continue
    else:
        print('Processing payload data')
    start, end = cdata_str.find('{'), cdata_str.rfind('};')
    json_load = json.loads(cdata_str[start: end+1])
    tide_days = json_load['tideDays']
    daylight_low_tides = []
    for day in tide_days:
        sunrise = day['sunrise']
        sunset = day['sunset']
        tides = day['tides']
        for tide in tides:
            if tide['type'] == 'low':
                tide_timestamp = tide['timestamp']
                if sunrise <= tide_timestamp <= sunset:
                    daylight_low_tides += [{'date': day['date'], 'time': tide['time'], 'height': tide['height']}]
    # print(daylight_low_tides)
    loc_daylight_low_tides[url_loc] = daylight_low_tides
for entry, val in loc_daylight_low_tides.items():
    print('=-' * 40)
    print(entry)
    print('=-' * 40)
    for v in val:
        print(v)

# Load tide forcast page for each location
# # Extract low tides information that occur after sunrise and sunset ( Daytime - Nautical?, Civil? )
# Return the time and height or each daylight low tide

# Do they not have an API though? giggles
# Get each day's forecast for low tide
# filter the times just for daylight times
