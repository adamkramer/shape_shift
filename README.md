# shape_shift

Identifies and leverages a diverse combination of proxies and user-agents to see whether there are any changes based on who is visiting a particular site.

Requires: Python v3.x

Steps -
1. Obtain a list of live proxies which represent various geolocations via proxy list API
2. Check which are working, and verify that they represent the required geolocation
3. Use the proxy to connect to the site and iterate through various user-agents reading the data returned
4. Compare for outliers and highlight to the user

Will identify whether server alters its response depending on geolocation of source IP / user-agent which is presented.
Useful for triage during web based malware analysis.

Usage: shape_shift.py (url) - where url is the site which is to be analysed
  
e.g: shape_shift.py "http://adamkramer.uk/browser-test.php"
  
e.g. shape_shift.py "http://adamkramer.uk/browser-test-404.php"
  
  
  Further information, and a demonstration can be found in the associated blog post:
  https://digital-forensics.sans.org/blog/2017/10/24/uncover-targeted-web-malware
  
