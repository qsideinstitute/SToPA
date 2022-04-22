import csv
import RAKE
import pandas as pd
import re

# import all parsed_logs
data_2019 = pd.read_csv("../../data/parsed_logs_2019.csv",index_col=0)
data_2020 = pd.read_csv("../../data/parsed_logs_2020.csv",index_col=0)
raw_data_all = pd.concat([data_2019,data_2020],ignore_index = True)
text = ""

# create object that will extract keywords
rake_object = RAKE.Rake("./stop.txt")
keywords = list()

# setup data
number_of_rows = raw_data_all.shape[0]
narratives = raw_data_all.iloc[:,8]
i = 0
for narrative in raw_data_all.iloc[:,8]:
    text = text + str(narrative) + "\n"
    i += 1

remove = []
with open("remove.txt",'r') as file:
    lines = file.readlines();

for line in lines:
    remove.append(line[:-1])

text = text.lower()
text = re.sub("[^(a-z|\s)]"," ",text)
text = re.sub("\n","~",text)
text = re.sub("\s+"," ",text)
text = re.sub("~","\n",text)
text = re.sub("nan\n","",text)
text = re.sub("\(|\)","",text)
for word in remove:
    text = re.sub(" " + word + " "," ",text)

# extract keywords
try:
    words = rake_object.run(text)
    print(words) # debug
    wordlist = list()
    for word,relevance in words:
        wordlist.append(word)
    keywords.append(wordlist)
except Exception:
    keywords.append("-1")

# keywords_column = pd.Series(keywords,name="keywords") # note that this approach depends on iterating through the dataframe in order
# data_with_keywords = pd.concat([raw_data_all,keywords_column],axis = 1)

# data_with_keywords.to_csv("logs_and_keywords.csv")
