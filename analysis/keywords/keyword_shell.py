import csv
import RAKE
import operator
import shlex
import time

##### Functions for Running Shell #####
def main():
    while True:
        command = input("$ ")
        if command == "exit" or command == "quit":
            break
        elif command == "help":
            print("psh-police_query: a simple shell written in Python")
        else:
            execute_commands(command)

def execute_commands(command):
    try:
        run_command(command)
    except Exception:
        import traceback
        traceback.print_exc()
        print("psh-police_query: command not found or not incorrect syntax: {}".format(command))

##### Commands for Shell #####
def run_command(command):
    split = shlex.split(command)
    # $ keyword
    if split[0] == "keyword":
        print("Keyword or Keyphrase: " + split[1])
        print(keyword_dict[split[1]])
    # $ log
    elif split[0] == "log":
        print("Log \#" + split[1] + ":")
        print(narratives[int(split[1])])
    else:
        raise Exception

##### Startup #####    
narratives = dict()

# import 2020 logs
with open("..\\..\\data\\parsed_logs_2020.csv",mode='r',encoding="ANSI") as f:
    csv_reader = csv.reader(f)
    i = 0
    for line in csv_reader:
        narratives[i] = line[9]
        i += 1

# import 2019 logs        
offset = len(narratives)

with open("..\\..\\data\\parsed_logs_2019.csv",mode='r',encoding="ANSI") as f:
    csv_reader = csv.reader(f)
    i = 0
    for line in csv_reader:
        narratives[i + offset] = line[9]
        i += 1

keyword_dict = dict()

initial_time = time.time()
print("Loading data...")                
# extract some keywords
for i in range(len(narratives)):
    if (i == 0):
        pass
    else:
        rake_object = RAKE.Rake(".\\stop.txt")
        words = rake_object.run(narratives[i])
        for obj in words:
            word = obj[0]
            if word in keyword_dict:
                temp = keyword_dict[word]
                temp.append(i)
                keyword_dict[word] = temp
            else:
                temp = list()
                temp.append(i)
                keyword_dict[word] = temp

print("Data loaded in " + str(time.time() - initial_time) + " seconds.")

# start the shell
main()
