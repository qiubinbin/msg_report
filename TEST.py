import re

pattern_date = re.compile(r'\d+')
print(bool(re.match(pattern_date,'2019')))
