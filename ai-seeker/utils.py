import json

def calculate_ends(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        input_data = json.load(file)

    # Iterate through the list of dictionaries and calculate "end" for each one
    for item in input_data:
        item["end"] =round(item["start"] + item["duration"],2)
        del item["duration"]  # Remove the "duration" key from each dictionary

    # Save the updated data to a new JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(input_data, output_file)

import json

def create_chunks(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        output_data = json.load(file)

    combined_json_list = []

    # Calculate the number of groups to create
    num_groups = (len(output_data) + 3) // 4

    for group_num in range(num_groups):
        # Calculate the starting index and ending index for the current group
        start_index = group_num * 4
        end_index = min(start_index + 4, len(output_data))

        # Extract the "text" values from the current group of dictionaries
        combined_text = " ".join([item["text"] for item in output_data[start_index:end_index]])

        # Calculate the "start" and "end" for the current group
        group_start = output_data[start_index]["start"]
        group_end = output_data[end_index - 1]["end"]

        # Create the combined JSON for the current group
        combined_json = {
            "text": combined_text,
            "start": group_start,
            "end": group_end,
        }

        combined_json_list.append(combined_json)

    # Save the combined JSON list to a new file
    with open(output_file_path, 'w') as output_file:
        json.dump(combined_json_list, output_file)

