# shape_shift

Iterates through a list of User-Agents, making HTTP requests and comparing the results with a control value.
Will identify whether server alters it's response depending on which User-Agent is presented.
Useful for triage during web based malware analysis.

Usage: shape_shift.py <url>
e.g: shape_shift.py "http://adamkramer.uk/browser-test.php"
  
  
