# Tester file for git

from fuzzywuzzy import fuzz
import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]

search = raw_input("What is your search term?")

ratio = {}
for file in files:
    rating = fuzz.token_set_ratio(file, search)
    ratio[file] = rating

new = sorted(ratio, key=ratio.get)

print(new)

#print(files)
