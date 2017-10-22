import urllib.request
import sys
import json
import time
import difflib

# List of countries which we want appear to be coming from - 
# Add/remove per your requirements - second field is ISO_3166 country code 
# Country codes can be obtained from: https://en.wikipedia.org/wiki/ISO_3166-1#Current_codes
# If you have preferred proxy for a particular country, place it in the 3rd field in format IP:port and it will be used

proxylist_matrix = [
					["United States", "US", ""],
					["China", "CN", ""],
					["Japan", "JP", ""],
					["Germany", "DE", ""],
					["United Kingdom", "GB", ""],
					["France", "FR", ""],
					["India", "IN", ""],
					["Italy", "IT", ""],
					["Brazil", "BR", ""],
					["Canada", "CA", ""],
					["South Korea", "KR", ""],
					["Russia", "RU", ""],
					["Australia", "AU", ""],
					["Spain", "ES", ""],
					["Mexico", "MX", ""],
					["Indonesia", "ID", ""],
					["Turkey", "TR", ""],
					["Netherlands", "NL", ""],
					["Switzerland", "CH", ""],
					["Saudi Arabia", "SA", ""],
					["Argentina", "AR", ""]
					]
					
# User Agents below obtained from http://www.networkinghowtos.com/howto/common-user-agent-list/
# Add / remove per your requirements - first field is friendly name, second field is user-agent you want to send

useragent_matrix = [
					["Google Chrome", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"],
					["Mozilla Firefox","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"],
					["Microsoft Edge","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"],
					["Microsoft Internet Explorer 6 / IE 6","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)"],
					["Microsoft Internet Explorer 7 / IE 7","Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)"],
					["Microsoft Internet Explorer 8 / IE 8","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"],
					["Microsoft Internet Explorer 9 / IE 9","Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)"],
					["Microsoft Internet Explorer 10 / IE 10","Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; MDDCJS)"],
					["Microsoft Internet Explorer 11 / IE 11","Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko"],
					["Apple iPad","Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4"],
					["Apple iPhone","Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"],
					["Googlebot (Google Search Engine Bot)","Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"],
					["Bing Bot (Bing Search Engine Bot)","Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"],
					["Samsung Phone","Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36"],
					["Samsung Galaxy Note 3","Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36"],
					["Samsung Galaxy Note 4","Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36"],
					["Google Nexus","Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7"],
					["HTC","Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"],
					["Curl","curl/7.35.0"],
					["Wget","Wget/1.15 (linux-gnu)"],
					["Lynx","Lynx/2.8.8pre.4 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.12.23"]
					]

# Shameless welcome banner					
print ("########### SHAPE_SHIFTER v1.0 - Adam Kramer 2017 #############")

# STAGE 1
# 1. Find working proxies for each of the required countries
# 2. Test proxies by connecting to them and having 3rd party site geo-locate the IP to verify it matches requirements

print ("################### STAGE 1 - SETUP PHASE #####################")
	
# Iterate through each of the required countries in the proxy list matrix
for i in range(len(proxylist_matrix)):

	# If the proxy field (3rd field) is not empty - skip attempt to obtain, as user has hard coded their preferred proxy in
	if (proxylist_matrix[i][2] != ""):
		print("[INFO] Skipping - IP field in script for " + proxylist_matrix[i][0] + " is not blank")
		continue

	# Loop will 
	while True:
	
		# Clear any proxies that have been set so far
		proxy_handler = urllib.request.ProxyHandler({})
		proxy_opener = urllib.request.build_opener(proxy_handler)
		urllib.request.install_opener(proxy_opener)
		
		# Inform user which proxy server we are attempting to obtain 
		print ("[INFO] Attempting to obtain proxy server which geo-locates to " + proxylist_matrix[i][0])
		
		# Connect to website which provides proxies and obtain json response
		try:
			# There are plenty of websites which let you obtain proxies via API query
			# I have selected the website which was the top google result - replace per your preference
			resp = urllib.request.urlopen("https://gimmeproxy.com/api/getProxy?user-agent=true&anonymityLevel=1&supportsHttps=true&country=" + proxylist_matrix[i][1], timeout = 5)
		# Broad error catching - if website can't be accessed then keep trying after 5 second pause
		except:
			print ("[ERROR] Error during proxy request - pausing for 5 seconds, then attempting retry")
			time.sleep(5)
			continue
		
		# Read output which is returned from proxy list website, decode json and extract IP/port details
		resp_json_decoded = json.loads(resp.read())
		proxylist_matrix[i][2] = resp_json_decoded['ip'] + ":" + resp_json_decoded['port']
		print ("[INFO] Proxy server obtained for " + proxylist_matrix[i][0] + " - " + proxylist_matrix[i][2])
	
		# Set obtained details as proxy currently in use
		proxy_handler = urllib.request.ProxyHandler({'http': proxylist_matrix[i][2], 'https' : proxylist_matrix[i][2]})
		proxy_opener = urllib.request.build_opener(proxy_handler)
		urllib.request.install_opener(proxy_opener)
	
		# Connect to 3rd party website to verify that the proxy is working, and that the geo-location is per requirements
		try:
			resp = urllib.request.urlopen("https://ip-api.io/json/" + resp_json_decoded['ip'], timeout = 5)
		except:
			print ("[ERROR] Error caught during testing attempt - requesting new proxy")
			continue
			
		# Response should contain required country name - if not, we will continue to next loop iteration and try another proxy
		test_resp_data = resp.read()
		if (proxylist_matrix[i][0] in str(test_resp_data)):
			print ("[INFO] " + proxylist_matrix[i][0] + " proxy tested (including verifying geo-location), appears ok")
			# break means we're happy, and we're leaving the infinite loop and onto obtaining proxy for next country
			break
			
		print ("[INFO] Testing showed proxy server not responding, or geo-location incorrect - requesting a new one")

# Inform user that we have obtained working proxies for all requested countries
print ("[INFO] Obtained all requested proxies - progressing to testing phase")
print ("################### STAGE 2 - TESTING PHASE #####################")
print ("[INFO] Each response will be compared against your default IP and user-agent " + useragent_matrix[0][0])

# Obtain a control value based on default IP / first user-agent in the list
proxy_handler = urllib.request.ProxyHandler({})
proxy_opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(proxy_opener)

# Set user-agent as first item from user-agent array
custom_headers = {}
custom_headers['User-Agent'] = useragent_matrix[0][1]
req = urllib.request.Request(sys.argv[1], headers = custom_headers)
	
# Send request and receive response into the array
while True:
	try:
		resp = urllib.request.urlopen(req, timeout = 5)
		control_website_response = resp.read()
		break
	except:
		print ("[ERROR] Could not request website when connecting via default IP, retrying...")
		time.sleep(5)
	
# Iterate through each requested country
for i in range(len(proxylist_matrix)):

	# Inform user that we are connecting to current iterations proxy
	print ("[INFO] Connecting to proxy server obtained for " + proxylist_matrix[i][0] + " - " + proxylist_matrix[i][2])
	
	# Connect to proxy
	proxy_handler = urllib.request.ProxyHandler({'http': proxylist_matrix[i][2], 'https' : proxylist_matrix[i][2]})
	proxy_opener = urllib.request.build_opener(proxy_handler)
	urllib.request.install_opener(proxy_opener)
	
	# Iterate through each required user-agent
	for j in range(len(useragent_matrix)):

		print ("[INFO] Sending query with User-Agent: " + useragent_matrix[j][0])
	
		# Set user-agent as current iteration from array
		custom_headers = {}
		custom_headers['User-Agent'] = useragent_matrix[j][1]
		req = urllib.request.Request(sys.argv[1], headers = custom_headers)
	
		# Send request and receive response into the array
		try:
			resp = urllib.request.urlopen(req, timeout = 5) 
			current_website_response = resp.read()
		except:
			print ("[ERROR] Could not request when connecting via " + proxylist_matrix[i][0] + " proxy")
			continue

		# Check whether current response is different from the control value
		if current_website_response != control_website_response:
			
			# Inform user that we've found one that is different from the control value
			print ("[ALERT] DIFFERENCE detected when using geo-location " + proxylist_matrix[i][0] + " User-Agent: " + useragent_matrix[j][0])
			print ("[ALERT] Details of the differences:")
				
			# Show the user the DIFF details
			test_data_1 = control_website_response.splitlines()
			test_data_2 = current_website_response.splitlines()
			differ_instance = difflib.Differ()
			diff_data = differ_instance.compare(test_data_1, test_data_2)
			print('\n'.join(diff_data))
