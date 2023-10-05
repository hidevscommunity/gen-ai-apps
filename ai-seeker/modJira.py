from jira.client import JIRA
import pandas as pd
import streamlit as st

def get_details(project_id, atlassian_username, atlassian_password):
        # Specify a server key. It should be your
    # domain name link. yourdomainname.atlassian.net
    jiraOptions = {'server': "https://srikanthnm.atlassian.net"}
    
    # Get a JIRA client instance, pass,
    # Authentication parameters
    # and the Server name.
    # emailID = your emailID
    # token = token you receive after registration
    jira = JIRA(options=jiraOptions, basic_auth=(
        atlassian_username, atlassian_password))
    
    # Search all issues mentioned against a project name.
    lstKeys = []
    lstSummary = []
    lstReporter = []
    for singleIssue in jira.search_issues(jql_str=f'project = {project_id}'):
        lstKeys.append(singleIssue.key)
        lstSummary.append(singleIssue.fields.summary)
        lstReporter.append(singleIssue.fields.assignee.displayName)

    df_output = pd.DataFrame()
    df_output['Key'] = lstKeys
    df_output['Summary'] = lstSummary
    df_output['Assignee'] = lstReporter

    df_output.to_csv('jira.csv', index=False)

    return df_output

def ask_question(strQuery):
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import pandas as pd

    tokenizer = AutoTokenizer.from_pretrained("Yale-LILY/reastap-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Yale-LILY/reastap-large")

    table = pd.read_csv("jira.csv")

    query = strQuery
    encoding = tokenizer(table=table, query=query, return_tensors="pt")

    outputs = model.generate(**encoding)

    return (tokenizer.batch_decode(outputs, skip_special_tokens=True)[0])
