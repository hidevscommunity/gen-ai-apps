import os
import pandas as pd
from pprint import pprint
import json
import random
from typing import List



def get_topics() -> List:
    question_dataset_path = f"{os.getcwd()}/dataset/leetcode_questions.csv"
    question_dataset_df = pd.read_csv(filepath_or_buffer=question_dataset_path,
                                      delimiter=',')
    topic_set = set()

    for idx, val in question_dataset_df.iterrows():
        topics = val['Topic Tagged text']
        if isinstance(topics, str):
            topics = topics.split(",")

            for topic in topics:
                if topic not in topic_set:
                    topic_set.add(topic)

    return list(topic_set)



def generate_sample_question(language: str,
                            difficulty: str,
                            topic: str) -> str:
    solution_dataset_path = f"{os.getcwd()}/dataset/leetcode-solutions.jsonl"
    question_dataset_path = f"{os.getcwd()}/dataset/leetcode_questions.csv"
    solution_dataset_df = pd.read_json(path_or_buf=solution_dataset_path,
                                    lines=True)
    solution_dataset_df = solution_dataset_df[solution_dataset_df['difficulty'] == difficulty]

    question_dataset_df = pd.read_csv(filepath_or_buffer=question_dataset_path,
                                      delimiter=',')

    question_json = {}
    for _, val in solution_dataset_df.iterrows():
        if language in val['answer']:
            matching_record = question_dataset_df[question_dataset_df['Question ID'] == int(val['id'])]
            if len(matching_record):
                topic_list = matching_record['Topic Tagged text'].to_string(index=False)
                topic_list = topic_list.split(",")
                if topic in topic_list:
                    question_json[val['id']] = {
                        "title": val['title'],
                        "difficulty": val['difficulty'],
                        "question": val['content'],
                        "answer": val['answer']['python'],
                    }

    output_file_name = f"{language}_{difficulty}_{topic}_dataset.json".lower()
    output_file_path = f"{os.getcwd()}/dataset/{output_file_name}"

    with open(output_file_path, "w") as dataset_file:
        json.dump(question_json, dataset_file)

    return output_file_path

def select_random_n_questions(dataset_path: str,
                              n: int = 3) -> List:
    if not os.path.exists(dataset_path):
        raise Exception('Reference dataset does not exist!')

    with open(dataset_path, "r") as dataset_file:
        sample_question = json.load(dataset_file)

    question_ids = list(sample_question.keys())
    select_idx = []

    for _ in range(n):
        while True:
            chosen_idx = random.randint(0, len(question_ids)-1)
            if chosen_idx not in select_idx:
                select_idx.append(chosen_idx)
                break

    sample_questions = []

    for idx in select_idx:
        sample_questions.append(sample_question[question_ids[idx]])

    return sample_questions



# if __name__ == "__main__":
    # generate_sample_question(language='python',
    #                         difficulty='Easy',
    #                         topic='Array')

    # sample_questions = select_random_n_questions(dataset_path=f"{os.getcwd()}/dataset/python_easy_array_dataset.json")
    # pprint(sample_questions)