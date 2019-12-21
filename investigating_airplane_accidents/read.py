import pandas as pd
import numpy as np
import timeit
import re
import operator

aviation_data = list()
with open("AviationData.txt","r") as file:
    line = file.readline()
    while line:
        aviation_data.append(line)
        line = file.readline()

aviation_list = list()
for row in aviation_data:
    aviation_list.append(row.split("|"))

### Exponential time search algorithm
start = timeit.default_timer()
for row in aviation_list:
    for item in row:
        if "LAX94LA336" in item:
            print("LAX code found in row #{}".format(aviation_list.index(row)))
            break

print("Runtime exponential search algorithm: {:.0f} ms".format(
    1000*(timeit.default_timer() - start)
    )
) # try to write as a decorator?

### Linear time search algorithm
start = timeit.default_timer()
for row in aviation_data:
    if "LAX94LA336" in row:
        print("LAX code found in row #{}".format(aviation_data.index(row)))
        break
    
print("Runtime linear search algorithm: {:.0f} ms".format(
    1000*(timeit.default_timer() - start)
    )
) # try to write as a decorator?

### log(n) search algorithm -> think about it
# start = timeit.default_timer()
# # code here

# print("Runtime linear search algorithm: {:.0f} ms".format(
#     1000*(timeit.default_timer() - start)
#     )
# ) # try to write as a decorator?

### Storing data in a list of dictionaries
aviation_dict_list = list()
aviation_data_keys = [key.strip() for key in aviation_data[0].split("|")[:-1]] # \n generated in last list item
for row in aviation_data[1:]: # take out column names / keys
    row_dict = dict() 
    row_list = [value.strip() for value in row.split("|")[:-1]]
    for key,val in zip(aviation_data_keys,row_list):
        row_dict[key] = val
    aviation_dict_list.append(row_dict)

### Searching through a list of dictionaries
start = timeit.default_timer()
for row in aviation_dict_list:
    if "LAX94LA336" in row.values():
        print("LAX code found in row #{}".format(aviation_dict_list.index(row)))
        print(row)
        break
    
print("Runtime list of dicts search algorithm: {:.0f} ms".format(
    1000*(timeit.default_timer() - start)
    )
)

### How many accidents occured in each U.S. State?
# We will use aviation_list
aviation_clean = list()
for row in aviation_list:
    aviation_clean.append(
        [value.strip() for value in row[:-1]]
        ) # there is an extra \n value at the end of each row

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
state_accidents = dict()
location_index = aviation_clean[0].index("Location") #return index of Location column

start = timeit.default_timer()
for row in aviation_clean[:-1]: # do not include column names
    state_match = re.match(r"[A-Z]{2}",row[location_index])
    if state_match:
        state = state_match.group(0)
        if state in states:
            if state in state_accidents.keys():
                state_accidents[state] += 1
            else:
                state_accidents[state] = 1
print("Runtime search state_accidents: {:.0f} ms".format(
    1000*(timeit.default_timer() - start)
    )
)

print(state_accidents)
print("State with highest number of accidents: {}, with {} accidents".format(
    max(state_accidents.items(), key=operator.itemgetter(1))[0],
    max(state_accidents.values())
    )
)

### Counting injuries per month
# Event Date column is in format MM/DD/YYYY, we can extract first 2 characters of the string
monthly_injuries = dict()
event_date_index = aviation_clean[0].index("Event Date")
serious_inj_index = aviation_clean[0].index("Total Fatal Injuries")
fatal_inj_index = aviation_clean[0].index("Total Serious Injuries")

for row in aviation_clean[1:]: # do not include column names
    month = row[event_date_index][:2] # extract month
    serious_inj = row[serious_inj_index]
    if not serious_inj: # empty string, replace to 0
        serious_inj = 0
    else:
        serious_inj = int(serious_inj)
    fatal_inj = row[fatal_inj_index]
    if not fatal_inj: # empty string, replace to 0
        fatal_inj = 0
    else:
        fatal_inj = int(fatal_inj)
    total_inj = fatal_inj + serious_inj

    if month in monthly_injuries.keys():
        monthly_injuries[month] += total_inj
    else:
        monthly_injuries[month] = total_inj

monthly_injuries.pop("") # pop key with no numeric month
print("Number of injuries per month")
print("----------------------------")
for key in sorted(monthly_injuries):
    print("{}: {}".format(key,monthly_injuries[key]))
    
### More fun things to do:
    # Rewrite this in a Jupyter NB
    # Map out accidents using the basemap library for matplotlib
    # Count the number of accidents by air carrier
    # Count the number of accidents by airplane make and model
    # Figure out what percentage of accidents occur under adverse weather conditions
