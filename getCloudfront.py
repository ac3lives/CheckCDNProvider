import requests
from requests.exceptions import HTTPError

#Configure the cloudfront URL
cloudfront_url = "https://d7uri8nf7uskq.cloudfront.net/tools/list-cloudfront-ips"

def get_cloudfront_cdn_ranges():
	try:
	    response = requests.get(cloudfront_url)
	    response.raise_for_status()
	    jsonResponse = response.json()
	    #print(jsonResponse)
	    #print(jsonResponse['result']['ipv4_cidrs'])
	    cloudfrontIPV4Array = jsonResponse['CLOUDFRONT_GLOBAL_IP_LIST'] + jsonResponse['CLOUDFRONT_REGIONAL_EDGE_IP_LIST']
	    return cloudfrontIPV4Array

	except HTTPError as http_err:
	    print(f'HTTP error occurred: {http_err}')
	except Exception as err:
	    print(f'Other error occurred: {err}')

if __name__ == '__main__':
	print(get_cloudfront_cdn_ranges())