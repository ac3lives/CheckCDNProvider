import requests
from requests.exceptions import HTTPError

#Configure the merlin URL
merlin_url = "https://api.merlincdn.com/ip-list"

def get_merlin_cdn_ranges():
	try:
	    response = requests.get(merlin_url)
	    response.raise_for_status()
	    jsonResponse = response.json()
	    merlinIPV4Array = []
	    for item in jsonResponse['data']:
	    	merlinIPV4Array.append(item['ipv4'] + "/32")
	
	    return merlinIPV4Array

	except HTTPError as http_err:
	    print(f'HTTP error occurred: {http_err}')
	except Exception as err:
	    print(f'Other error occurred: {err}')

if __name__ == '__main__':
	print(get_merlin_cdn_ranges())