def get_company_name_prompt(user_input: str):
    return f"""
                Identify the following items from the Input Text: 
                - is there a valid company name present in the input text ? (True or False)
                - Extract valid company name from input text
                - return name as the actual company name in the response.(string or None)
                
                Input Text is delimited with <>. \
                Format your response as a JSON object with \
                "company_present" and "name" as the keys.
                If the information isn't present, use "None" \
                as the value.
                Make your response as short as possible.
                Format the company_present value as a boolean.
                Format the name value as string.
                Input Text: <{user_input}>
                """


def get_income_statement_prompt(user_input: str):
    return f"""
                Forget all the past interactions.
                Identify the following items for the Input Query:
                - Use current year value as 2023
                - is the input query can be answered using company's Income ? (True or False)
                - Extract valid year from input text
                - return year as the actual year in the response.(int or None)
                
                Input Text is delimited with <>. \
                Format your response as a JSON object with \
                "income_statement_useful" and "year" as the keys.
                If the information isn't present, use "None" \
                as the value.
                Make your response as short as possible.
                Format the income_statement_useful value as a boolean.
                Format the year value as int.
                Input Query: <{user_input}>
                """


def get_balance_sheet_prompt(user_input: str):
    return f"""
                Forget all the past interactions.
                Identify the following items from the Input Query: 
                - Use current year value as 2023
                - is the input query can be answered using company's Balance Sheet or it's related to Balance Sheet ? (True or False)
                - Extract valid year from input text
                - return year as the actual year in the response.(int or None)
                
                Input Text is delimited with <>. \
                Format your response as a JSON object with \
                "balance_sheet_useful" and "year" as the keys.
                If the information isn't present, use "None" \
                as the value.
                Make your response as short as possible.
                Format the balance_sheet_useful value as a boolean.
                Format the year value as int.
                Input Query: <{user_input}>
                """


def get_cash_flow_prompt(user_input: str):
    return f"""
                Identify the following items from the Input Query: 
                - Use current year value as 2023
                - is the input query can be answered using company's Cash Flow or it's related to Cash Flow ? (True or False)
                - Extract valid year from input text
                - return year as the actual year in the response.(int or None)
                
                Input Text is delimited with <>. \
                Format your response as a JSON object with \
                "cash_flow_useful" and "year" as the keys.
                If the information isn't present, use "None" \
                as the value.
                Make your response as short as possible.
                Format the cash_flow_useful value as a boolean.
                Format the year value as int.
                Input Query: <{user_input}>
                """


def get_earnings_prompt(user_input: str):
    return f"""
                Identify the following items from the Input Query:
                - Use current year value as 2023
                - is the input query can be answered using company's Earnings or it's related to Earnings ? (True or False)
                - Extract valid year from input text
                - return year as the actual year in the response.(int or None)
                
                Input Text is delimited with <>. \
                Format your response as a JSON object with \
                "earning_useful" and "year" as the keys.
                If the information isn't present, use "None" \
                as the value.
                Make your response as short as possible.
                Format the earning_useful value as a boolean.
                Format the year value as int.
                Input Query: <{user_input}>
                """


def get_summary_prompt(name, user_input, context):
    return f"""
            - Use current year value as 2023
            - You role is to generate a answer summary of the user question: {user_input} for the company {name} based on the context.
            - Highlight important information using markdown. Do not include the question.
            - Format the response in paragraph-style like a report.
            - Context is delimited with <>.             
            - Make your response less than 300 words.
            - Don't mention "Some highlights of the company" in the response
            - Don't mention "As an expert business analyst" in the response
            Context: <{context}>
            """


def get_generic_answer_prompt(user_query):
    return f"""
                - You are an expert business analyst.
                - Use current year value as 2023
                - Your task is to help me provide an answer summary to the below question delimited by <>
                - Generate a paragraph-style response with bullet points in raw Markdown javascript format.
                - Don't mention "Based on your input", in the response.
                - Don't mention "Based on the information available", in the response.
                
                UserInput: <{user_query}>
                """
