import os

original_document_names = [
    "act_1.txt", "act_2.txt", "act_3.txt"
]

original_document_general_path = "../documents/original_texts/acts"

def split_by_headers(filename):
    # Extract the original document name (without extension) from the path
    original_name = os.path.splitext(os.path.basename(filename))[0]
    new_directory = f"../documents/knowledge_base/{original_name}/"

    # Create the directory if it doesn't exist
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    # Read the file into memory
    with open(filename, 'r') as f:
        content = f.read().splitlines()  # splitlines will split without retaining newline chars

    buffer = []
    title = None

    def save_section(title, buffer):
        if title and buffer:
            filename = os.path.join(new_directory, title.strip().replace(' ', '_') + ".txt")
            with open(filename, 'w') as f:
                f.write('\n'.join(buffer))

    for line in content:
        if line.startswith('# '):  # If we hit a H1 header
            save_section(title, buffer)  # Save the previous section if any
            title = line[2:].strip()  # Get the new title
            buffer = [line]  # Start a new buffer with the title
        else:
            buffer.append(line)

    save_section(title, buffer)  # Save the last section

if __name__ == "__main__":
    for document_name in original_document_names:
        split_by_headers(original_document_general_path + document_name)
    print("File splitting completed!")
