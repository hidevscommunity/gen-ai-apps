import json

def calculate_end_from_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        input_data = json.load(file)

    # Iterate through the list of dictionaries and calculate "end" for each one
    for item in input_data:
        item["end"] =round(item["start"] + item["duration"],2)
        del item["duration"]  # Remove the "duration" key from each dictionary

    # Save the updated data to a new JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(input_data, output_file)

# # Replace 'input_file.json' with the actual path to your input JSON file
# input_file_path = '/home/bharathi/langchain_experiments/GenAI/transcript.json'

# # Replace 'output_file.json' with the desired path and filename for the output JSON file
# output_file_path = '/home/bharathi/langchain_experiments/GenAI/transcript_end.json'

# # Call the function to calculate the "end" values and remove "duration" and save the new JSON file
# calculate_end_from_file(input_file_path, output_file_path)

