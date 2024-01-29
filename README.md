# CheckCDNProvider
Take a list of domains or IP addresses, resolve their IP address, and determine if it resolves to a known Content Delivery Network space.

Currently checks against:
- Cloudflare
- Cloudfront
- Merlin

Prior to running the scan, the CheckCDNProvider reaches out to each of the CDN provider's public API to obtain a list of network ranges associated with their CDN. 

Note that this was a quick and dirty script written one night while working through massive data sets, and has a lot of room for improvement. Support for AzureEdge CDN was not provided as they put their IP address ranges behind a registration + API key requirement. Could hard-code in the IP ranges at a point-in-time, or add a "API key" config option to the tool in the future.

## Usage
```
python3 checkcdnprovider.py 
Please select from IP List (-iL) or Domain List (-dL)
  -dL  File name containing a list of domains to resolve and then check against CDN ranges
  -iL  File name containing a list of IP addresses to check against CDN ranges
  -tS  Sort the resulting table by the 'Hostname", "IP Address", or "CDN Provider" columns.
```
Example command:
```
python3 checkcdnprovider.py -dL testdomains.txt -tS "CDN Provider"
```

## Example output:
```
└─$ python3 checkcdnprovider.py -dL test_domains.txt -tS "CDN Provider"                                                                                                                         2 ⨯
Waiting for queue to complete 0 tasks
+----------------+----------------+--------------+
|    Hostname    |   IP Address   | CDN Provider |
+----------------+----------------+--------------+
| cloudfront.com | 207.171.166.22 |     None     |
|                |                |              |
| merlincdn.com  | 51.210.175.60  |     None     |
|                |                |              |
|   nginx.com    | 185.56.152.165 |     None     |
|                |                |              |
| cloudflare.com | 104.16.133.229 |  cloudflare  |
|                |                |              |
|  hubspot.com   | 104.19.155.83  |  cloudflare  |
|                |                |              |
+----------------+----------------+--------------+
Finished! Failed to resolve 0 domains.
```
Returns the number of domains which also failed to resolve to an IP address. 

## Future Updates
- Set a toggle for the max number of threads, right now it is hard-coded at 300 on line 59. I could've probably added this faster than typing it out in a to-do, but yeah.
- Kick off to another script which takes a list of known owned-IP ranges, manually sets the host header, and tries to connect with CDN-identified domains. Compare if the returned site matches the site through the CDN
- Set a toggle for debug to show all failed to resolve domains instead of just a count
- Add additional CDNs, namely AzureEdge

  

