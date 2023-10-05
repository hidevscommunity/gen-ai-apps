import asyncio
from utils.index_helper import retrieve_context
from utils.chain_helper import async_generate, get_chain


async def generate_company_info_job_requirement(job_description, index_company=None):
    # Define chain 1
    company_info_template = """
    The following text delimited by triple asterisks contains some information or introduction of a company:

    ```
    {company_info}
    ```

    Extract the information about the company mention in the text above and return the information in paragraphs
    """
    company_info_chain = get_chain(company_info_template)

    # Define chain 2
    job_description_template = """
    The following text delimited by triple asterisks is a job description:

    ```
    {job_description}
    ```

    extract all the requirements (technical skills and soft skills) and job duties of this role and return them in a single list of bullet points
    """
    job_description_chain = get_chain(job_description_template)

    # Async generated results
    jobs = [(job_description_chain, job_description)]
    if index_company: 
        company_info_query = "What are the mission and vision, culture, products or services, challenges, market position, history, size and structure of the company?"
        related_company_info = retrieve_context(index_company, company_info_query)
        jobs.append((company_info_chain, related_company_info))

    tasks = [async_generate(chain, arg_dict) for chain, arg_dict in jobs]
    
    # Get the results and return
    result = await asyncio.gather(*tasks)

    if len(result) == 2:
        return result
    return result[0], None


def generate_role_challenge(position, job_description, extracted_company_info=None):
    if extracted_company_info:
        template = """You are a very experienced recruiter and imagine someone is applying for the position {position}.

        The following text delimited by triple backticks is the job description of this position.

        ```
        {description}
        ```

        And the following text delimited by triple asterisks is an introduction of the company which is hiring for this position:

        ***
        {company_info}
        ***

        Based on ONLY the job description and the company's information above, what is the biggest challenge for someone in this position would face day-to-day, especially in this company? Explain your answer in detail by beginning your reply with the phrase "The biggest challenge someone in this position from this company".
        """

        prompt_arg = {"position": position, "description": job_description, "company_info": extracted_company_info}

    else:
        template = """You are a very experienced recruiter and imagine someone is applying for the position {position}.

        The following text delimited by triple backticks is the job description of this position.

        ```
        {description}
        ```

        Based on ONLY the job description above, what is the biggest challenge for someone in this position would face day-to-day? Explain your answer in detail by beginning your reply with the phrase "The biggest challenge someone in this position".
        """
        prompt_arg = {"position": position, "description": job_description}

    job_description_chain = get_chain(template)
    job_challenge = job_description_chain.run(prompt_arg)
    
    return job_challenge


def generate_first_paragraph(position, company, job_challenge, index_user):
    related_user_info = retrieve_context(index_user, job_challenge)
    
    template = """You are a very experienced career coach with over 20 years of experience, and your client is applying for the position of {position} at {company}.

    The following text delimited by triple asterisks is a statement highlighting the major challenges for someone in this position:

    ***
    {job_challenge}
    ***
    
    And following text delimited by tiple backticks contains some information or introduction of your client, whcih can be part of the client's personal statements or resume:

    ```
    {user_info}
    ```

    Write a short, single-paragraph attention-grabbing hook for your client's cover letter. You writing show fulfill all the below criteria:

    - Shows your client's understanding on the specific challenges someone will face as the position {position} at {company}.
    - If your client has achievements or expereinces related to those challenges, point out how your client can be a suitable candidate for/ the {position} position.
    - DO NOT make up your client's achievements or expereinces that are not explicitly mentioned the text delimited by triple asterisks above
    - Your writing should use a confident yet humble language, and it should be within 100 words.

    """
    prompt_arg = {"position": position, "company": company, "job_challenge": job_challenge, "user_info": related_user_info}

    first_paragraph_chain = get_chain(template, llm_model="gpt-4", temperature=0.7)
    first_paragraph = first_paragraph_chain.run(prompt_arg)

    return first_paragraph


def generation_final_letter(name, position, company, job_requirement, first_paragraph, index_user):
    user_info = retrieve_context(index_user, job_requirement)

    template = """You are a very experienced career coach,your client {name} is asking you to help them in writing the cover letter for applying for the position {position} at {company}.

    The following list delimited by triple backticks contains the skillset requirements and the job duties of this position:

    ```
    {job_requirement}
    ```

    And the following text delimited by triple asterisks contains some information or introduction of your client, which can be the client's personal statements or resume, and may not be directly related to this position:

    ***
    {user_info}
    ***

    Also, the first paragraph of this cover letter is provided as below, delimited by triple dashes:

    ---
    {first_paragraph}
    ---

    Finish writing the entire cover letter by following each of the steps below:

    1. Start by including a placeholder for the salutation of the letter.
    2. The first paragraph must be exactly the same as the one provided above which delimited by triple dashes.
    3a. The following paragraphs must extend on the first paragraph, which highlights you client's relavant achievements or experiences that tie into the main responsibilities of the role without repeating what was mentioned in the first paragraph.
    3b. The client's relavant achievements or experiences you wrote MUST be what the client actually mentioned in the text delimited by triple asterisks. Do not make them up just to meet the role's requirement.
    3c. You don't need to consider all the responsibilities of the role, just pick 1 to 3 responsibilities which are most relavent to those mentioned in the first paragraph and can be supported by the client's achievements or experiences.
    4. The last paragraph should express gratitude, reinforcing your interest in the role and include a call to action.
    5. End the letter with an appropriate closing using the client's name ({name}).

    Your writing should use a confident yet humble language and the entire letter should be around 300 - 400 words.
    """
    prompt_arg = {"name": name, "position": position, "company": company, "job_requirement": job_requirement, "user_info": user_info, "first_paragraph": first_paragraph}

    final_letter_chain = get_chain(template, llm_model="gpt-4", temperature=0.7)
    final_letter = final_letter_chain.run(prompt_arg)
    return final_letter
