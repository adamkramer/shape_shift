# shape_shift

Identifies and leverages a diverse combination of proxies and user-agents to see whether there are any changes based on who is visiting a particular site.

Requires: Python v3.x

Steps -
1. Obtain a list of live proxies which represent various geo-locations via proxy list API
2. Check which are working, and verify that they represent the required geo-location
3. Use the proxy to connect to the site and iterate through various user-agents reading the data returned
4. Compare for outliers and highlight to the user

Will identify whether server alters it's response depending on geo-location of source IP / User-Agent which is presented.
Useful for triage during web based malware analysis.

Usage: shape_shift.py <url>
e.g: shape_shift.py "http://adamkramer.uk/browser-test.php"
e.g. shape_shift.py "http://adamkramer.uk/browser-test-404.php"
  
  
