from collections import Counter
import re
import spacy
spacy_model_dir = "spacy_model"
nlp = spacy.load(spacy_model_dir)
# spacy_model_dir = "spacy_model"
# nlp.to_disk(spacy_model_dir)


def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    return text


def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return keywords


def count_matched_keywords(list1, list2):
    total_common = 0
    common = []
    for keywords1 in list1:
        for keywords2 in list2:
            common_keywords = set(keywords1) & set(keywords2)  # Intersection of keyword sets
            common.append(set(keywords1))
            total_common += len(common_keywords)

    return total_common,common


list1 = [
    "machine learning",
    "data analysis",
    "python programming",
    "natural language processing"
]

list2 = [
    "machine learning",
    "deep learning",
    "data analysis",
    "nlp techniques"
]

# Preprocess and extract keywords from the lists
preprocessed_list1 = [preprocess_text(keyword) for keyword in list1]
preprocessed_list2 = [preprocess_text(keyword) for keyword in list2]

extracted_keywords_list1 = [extract_keywords(keyword) for keyword in preprocessed_list1]
extracted_keywords_list2 = [extract_keywords(keyword) for keyword in preprocessed_list2]

print(extracted_keywords_list2)

# Count matched keywords
matched_keywords_count,common_keywords = count_matched_keywords(extracted_keywords_list1, extracted_keywords_list2)
print(common_keywords)
print(f"Number of matched keywords: {matched_keywords_count}", common_keywords)
