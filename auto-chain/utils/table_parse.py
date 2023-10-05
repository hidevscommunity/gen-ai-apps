
def get_substrings_with_cuts(input_string, cut_indices):
    substrings = []
    start_index = 0
    
    for cut_index in cut_indices:
        sub = input_string[start_index:cut_index+1].strip()
        if(not sub):
            sub = ' '
        substrings.append(sub)    
            
        start_index = cut_index+1
    
    # Add the substring after the last cut index
    sub =input_string[start_index:].strip()
    if(sub):
        substrings.append(sub)

    return substrings

def merge_tables(tables):
    # Initialize an empty merged_array
    # Extract the first elements from the innermost arrays
    final_table = []
    #Check if first column of each table is equal
    first_col = [row[0] for row in tables[0]]
    same_first_col = False
    for table in tables:
        col = [row[0] for row in table]
        if(col == first_col):
            same_first_col = True
            break

    for i in range(len(tables[0])):
        if(same_first_col):
            merged_row = [sublist[i][1:] for sublist in tables]
            # Flatten the merged_row list and convert it to a single list
            merged_result =[tables[0][i][0]]+ [item for sublist in merged_row for item in sublist]
        else:
            merged_row = [sublist[i] for sublist in tables]
            # Flatten the merged_row list and convert it to a single list
            merged_result =[item for sublist in merged_row for item in sublist]
        final_table.append(merged_result)
    
    return final_table

def get_table(tables):
    tables,merges = extract_tables(tables)
    if(len(tables) == 0):
        return False
    for j,table in enumerate(tables):
        test = table[0]
        cut_indices = [0]
        for k,char in enumerate(test):
            cut = True
            if(char == ' '):
                for line in table:
                    if(line[k] != ' '):
                        cut = False
                        break
                if(cut):
                    for l,line in enumerate(table):
                        substring = line[cut_indices[-1]:k]
                        
                        if(substring.strip() == '' and len(cut_indices)!=1):
                            cut = False
                    if(cut):   
                        cut_indices.append(k)
        cut_indices.pop(0)

        
        for s,line in enumerate(table):
            tables[j][s] = get_substrings_with_cuts(line, cut_indices)  
    final_tables = []

    for merge in merges:
        if(len(merge)>1):
            selected_tables = [tables[index] for index in merge]
            final_tables.append(merge_tables(selected_tables))  
        else:
            final_tables.append(tables[merge[0]])      
    
    return final_tables

def extract_tables(table):
    lines = table.split('\n')
    length_array = [len(item) for item in lines]

    chunks = []
    current_chunk = []

    for i in range(1, len(length_array)):
        if length_array[i] == length_array[i - 1] and length_array[i]!=0:
            current_chunk.append(i - 1)
        else:
            if len(current_chunk) > 0:
                current_chunk.append(i - 1)
                chunks.append(current_chunk)
                current_chunk = []
    
    if len(current_chunk) > 0:
        current_chunk.append(len(length_array) - 1)
        chunks.append(current_chunk)
    for i in range(len(chunks)):
        for j in range(len(chunks[i])):
            chunks[i][j] = lines[chunks[i][j]]
    merges = []
    merge = []
    for i in range(len(chunks)):
        merge.append(i)
        if(chunks[i][0][-1] != '\\'):
            merges.append(merge)
            merge = []
        else:
            chunks[i][0] = chunks[i][0][:-1]+' '

    return chunks,merges

