import pandas as pd
import csv
import json as js

### ALIGN THE FORMART OF ALL FILES ###

### Merge set-1 question and solution

# Convert solution jsonl file into csv 
with open('set-1-solution.jsonl', 'r') as f1_solution:
    for line in f1_solution:
        js1_parsed = js.loads(line)

        # Your code to process the parsed JSON object goes here
        # For example, writing it to a CSV file as you are doing in your code

with open('set-1-solution.csv', 'wt') as file_1:  
    dict_writer = csv.DictWriter(file_1, fieldnames=["title", 
                                                    "slug", 
                                                    "difficulty", 
                                                    "id",
                                                    "content", 
                                                    "answer"])
            
    dict_writer.writeheader()
    dict_writer.writerow(js1_parsed) 
 
df1_question = pd.read_csv("set-1-question.csv") 
df1_solution = pd.read_csv("set-1-solution.csv") 

df1_solution.rename(columns={
    'id': 'Question ID',
    'slug': 'Question Slug', 
    'title': 'Question Title',
    'difficulty': 'Difficulty Level',
    'content': 'Question',
    'answer': 'Answer'
    }, inplace=True)

df1 = pd.merge(df1_question, df1_solution, how="outer", on=["Question ID", 
                                                            "Question Title",
                                                            "Question Slug",
                                                            "Difficulty Level"])

### Process set-3.json

# Convert set-3.json into csv
with open('set-3.json', 'r') as file3:
    content3 = file3.read()

js3_parsed = js.loads(content3)

with open('set-3.csv', 'wt') as f3:
    dict_writer = csv.DictWriter(f3, fieldnames=["source_file", "task_id", "prompt", "code", "test_imports", "test_list"])
    dict_writer.writeheader()
    for item in js3_parsed:
        dict_writer.writerow(item)

# Modify set-3.csv
df3 = pd.read_csv("set-3.csv") 

df3.rename(columns={
    'task_id': 'Question ID', 
    'prompt': 'Question',
    'code': 'Answer',
    'test_imports': 'Test Imports',
    'test_list': 'Assert Statement List'
    }, inplace=True)

# Delete 'Source column' (irrelevant info)
del df3['source_file']

### Process set-5.json

# Convert set-5 into csv file
with open('set-5.json', 'r') as file5:
    content5 = file5.read()

js5_parsed = js.loads(content5)

# Create a list of dictionaries containing only the values
values_list = [item for item in js5_parsed.values()]

with open('set-5.csv', 'w', newline='') as set5_csv:
    fieldnames = ["title", "difficulty", "question", "answer"]
    csv_writer = csv.DictWriter(set5_csv, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    # Write each dictionary as a separate row in the CSV file
    for row in values_list:
        csv_writer.writerow(row)

# Modify set-5.csv
df5 = pd.read_csv("set-5.csv") 

df5.rename(columns={
    'title': 'Question Title',
    'difficulty': 'Difficulty Level',
    'question': 'Question',
    'answer': 'Answer'
    }, inplace=True)

# Add 'Array' topic/tag column to set-5
column_name_tag_5 = 'Tag'
fill_value_array = 'Array'

if column_name_tag_5 not in df5:
    df5[column_name_tag_5] = fill_value_array

### Process set-6.json

# Convert set-6 into csv file
with open('set-6.json', 'r') as file6:
    content6 = file6.read()

js6_parsed = js.loads(content6)

# Create a list of dictionaries containing only the values
values_list_2 = [item for item in js6_parsed.values()]

with open("set-6.csv", 'w', newline='') as set6_csv:
    fieldnames = ["title", "difficulty", "question", "answer"]
    csv_writer = csv.DictWriter(set6_csv, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    # Write each dictionary as a separate row in the CSV file
    for row in values_list_2:
        csv_writer.writerow(row)

# Modify set-5-convert.csv
df6 = pd.read_csv("set-6.csv") 

df6.rename(columns={
    'title': 'Question Title',
    'difficulty': 'Difficulty Level',
    'question': 'Question',
    'answer': 'Answer'
    }, inplace=True)

# Add 'Array' topic/tag column to set-6/set-E
column_name_tag_6 = 'Tag'
fill_value_matrix = 'Matrix'

if column_name_tag_6 not in df6:
    df6[column_name_tag_6] = fill_value_matrix

# There are 4 df: df1, df3, df5, df6

# Concatenate the DataFrames vertically & Reset the index
combined_df = pd.concat([df1, df3, df5, df6], ignore_index=True)
del combined_df['Question ID']
combined_df = combined_df.reset_index(drop=True)

combined_df.to_csv('combined_data.csv')
