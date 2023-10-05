import json

def combine_and_calculate(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        output_data = json.load(file)

    combined_json_list = []

    # Calculate the number of groups to create
    num_groups = (len(output_data) + 7) // 8

    for group_num in range(num_groups):
        # Calculate the starting index and ending index for the current group
        start_index = group_num * 8
        end_index = min(start_index + 8, len(output_data))

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

# Replace 'output_file.json' with the path to the output JSON file you created previously
input_file_path = '/home/bharathi/langchain_experiments/GenAI/transcript_end.json'

# Replace 'combined_output_file.json' with the desired path and filename for the combined JSON file
output_file_path = '/home/bharathi/langchain_experiments/GenAI/chunks.json'

# Call the function to create the combined JSON and save it to a new file
combine_and_calculate(input_file_path, output_file_path)
