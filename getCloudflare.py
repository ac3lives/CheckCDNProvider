import requests
from requests.exceptions import HTTPError

#Configure the cloudflare URL
cloudflare_url = "https://api.cloudflare.com/client/v4/ips"

def get_cloudflare_cdn_ranges():
	try:
	    response = requests.get(cloudflare_url)
	    response.raise_for_status()
	    jsonResponse = response.json()
	    #print(jsonResponse)
	    #print(jsonResponse['result']['ipv4_cidrs'])
	    cloudflareIPV4Array = jsonResponse['result']['ipv4_cidrs']
	    return cloudflareIPV4Array

	except HTTPError as http_err:
	    print(f'HTTP error occurred: {http_err}')
	except Exception as err:
	    print(f'Other error occurred: {err}')

if __name__ == '__main__':
	print(get_cloudflare_cdn_ranges())