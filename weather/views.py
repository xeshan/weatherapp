from django.shortcuts import render
import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from collections import Counter
from django.http import HttpResponse

def index(request):
	if 'city' in request.GET:
		city = request.GET['city']
		
		geolocator = Nominatim(user_agent="weather-test")
		location = geolocator.geocode(city)
		
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
		}
		lat = location.latitude
		lon = location.longitude
		response = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}'.format(lat,lon),headers=headers)
		res = response.json()
		
		context = {
				'city_name': city,
				'time' : res["properties"]["timeseries"][0]["time"],
				'air_pressure' : res["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_pressure_at_sea_level"],
				'air_temp' :res["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"],
				'cloud_area_fraction':res["properties"]["timeseries"][0]["data"]["instant"]["details"]["cloud_area_fraction"],
				'relative_humidity': res["properties"]["timeseries"][0]["data"]["instant"]["details"]["relative_humidity"],
				'wind_from_direction' :res["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_from_direction"],
				'wind_speed' :res["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_speed"],
				}
	else:

		context = None
	
	return render(request, 'weather/index.html', context)


def word_frequencies(request):

	if 'url' in request.GET:
		url = request.GET['url']
		
		my_wordlist = []
		my_source_code = requests.get(url).text
		
		my_soup = BeautifulSoup(my_source_code, 'html.parser')
	    
		for each_text in my_soup.findAll('p'):
			content = each_text.text
	    
			words = content.lower().split()
			for each_word in words:
				my_wordlist.append(each_word)

		clean_list =[]
		for word in my_wordlist: 
			symbols = '!@#$%^&*()_+={[}]|:"<>?/., '
			for i in range (0, len(symbols)):
				word = word.replace(symbols[i], '')
			if len(word) > 0:
				clean_list.append(word)

		word_count = {}
		for word in clean_list:
			if word in word_count:
				word_count[word] += 1
			else:
				word_count[word] = 1
		

		context = {
					'url': url,
					'word_frequencies' : word_count ,
					}
	else:

		context = None

	return render(request, 'weather/fetch-data.html', context)

def integer_data(request):
	if 'goal' in request.GET:
		goal = int(request.GET['goal'])
		seq = request.GET['seq']
		seq=seq.split(',')
		for i in range(0, len(seq)):
			seq[i] = int(seq[i])
		n = len(seq)

		result = calc(seq, goal)

		context = {
			'goal' : goal,
			'seq'  : seq,
			'result': result
		}
	else:
		context = None	

	return render(request,'weather/integer-data.html', context)

def calc(seq, goal):
    d = {0: []}
    for item in seq:
        next_d ={}
        for itotal, path in d.items():
            for cand in [-item, item]:
                tnext = itotal + cand
                if abs(tnext) <= 500:
                    next_d[tnext] = path + [cand]
        d = next_d
    if goal in d:
        return d[goal]
    else:
        return 'None'