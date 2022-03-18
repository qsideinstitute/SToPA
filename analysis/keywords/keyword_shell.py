import operator
import shlex
import time
import pandas as pd
import json

##### Functions for Running Shell #####
def main():
    while True:
        command = input("$ ")
        if command == "exit" or command == "quit":
            break
        elif command == "help":
            print("psh-police_query: a simple shell written in Python")
            print("commands available: log, keyword")
        else:
            execute_commands(command)

def execute_commands(command):
    try:
        run_command(command)
    except Exception:
        import traceback
        # traceback.print_exc()
        print("psh-police_query: command not found or incorrect syntax: {}".format(command))

##### Commands for Shell #####
def run_command(command):
    split = shlex.split(command)
    # $ keyword
    if split[0] == "keyword":
        if len(split) == 1:
            print("usage: keyword [keyword or keyphrase]")
            return
        print("Keyword or Keyphrase: " + split[1])
        try:
            print(keyword_dict[split[1]])
        except Exception:
            print("error: keyword \"{}\" not found".format(split[1]))
    # $ log
    elif split[0] == "log":
        if len(split) == 1:
            print("usage: log [log number]")
            return
        try:
            entry_number = int(split[1])
        except ValueError:
            print("usage: log [log number]")
            return
        print("-"*10 + " Log #" + split[1] + " " + "-"*10)
        try:
            print(data.iloc[entry_number])
        except Exception:
            print("error: log {} not found".format(entry_number))
        print("-"*20)
        print("Narrative for this log:")
        print(data.iloc[entry_number][8])
    else:
        raise Exception

##### Startup #####
initial_time = time.time()
print("Loading data...")
# import all data
data = pd.read_csv("logs_and_keywords.csv",index_col=0)
# construct keyword dictionary for fast searching by keyword
keyword_dict = dict()
for index,log in data.iterrows():
    keywords = log["keywords"]
    if keywords == "-1":
        continue;
    # this code creates a dictionary from keywords --> lists of indices of logs to which that keyword is relevant
    # this code could be simplified with a wrapper function, writing the parse_keywords output to json and then loading the pd df from json, etc.
    keywords = keywords[1:-1].split(', ')
    for keyword in keywords:
        keyword = keyword[1:-1]
        if keyword in keyword_dict:
            temp = keyword_dict[keyword]
            temp.append(index)
            keyword_dict[keyword] = temp
        else:
            entry = []
            entry.append(index)
            keyword_dict[keyword] = entry

# start the shell
print("Data loaded in " + str(time.time() - initial_time) + " seconds.")
main()
