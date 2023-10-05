import streamlit as st

st.header(f'How it\'s built')
st.video("https://youtu.be/N0Q0CbguTjo")
st.markdown("""🌟Goal of the Demonstrating the prowess of using LLM to "Replace" traditional NLP programming 🚀

Given the textual data of a News article, we want to build a 🏗️

📋 I've Structed the LLM to complete 3 Major Tasks:

1️⃣ Supply Chain Disruption Event Classifier 
   - Classify if the News article talks about an event that will potentially affect the supply chain industry 📦🌐

2️⃣ Extract location --> Geopy API get coordinates 🗺️

3️⃣ Extract Attributes:
   - Disruption Type (E.g. Geo-political, Flooding) 🌊🌍
   - Severity Metrics 📊
   - Estimated Radius of Impact 🌎📏

Each Task is comprised into a "Chain" 
   ➡️ LLM 
   ➡️ Task specific Prompt
   ➡️ Output Parser 🧩
""")
# Example LLM Chain:
x = st.expander("Example LLM Chain Code for Binary Classifier", expanded=True)
with x:
    st.code('''
        # OpenAI Model
    classifier_llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature=1)
            
    # JSON Output Schema for Function Calling
    classifier_article_schema = {
        "name": "binary_classifier_article_schema",
        "description": "Binary Classifier Schema for Article, is a disruption event or not",
        "type": "object",
        "properties": {
        "isDisruptionEvent": {
            "type": "boolean"
        },
        "disruptionType":{
            "type": "string",
            "description": "Type of disruption event. Must be one of the example the Full list given in conditions"
        },
        "Reason": {
            "type": "string",
            "description": "Reason for your decision"
        }
        },
        "required": ["isDisruptionEvent","disruptionType","Reason"]
    }

    # Task Prompt Template
    classifierprompt = PromptTemplate(
        template = """Role:You are a Binary Classifier,your goal is to classify if the given news article is a vaild disruption event article or not.
        Conditions:
        1. A disruption event can be defined as "An event that potentially impacts the supply chain and have a vaild disruption type".
        Full List of possible disruption types: a) Airport Disruption b) Bankruptcy c) Business Spin-off d) Business Sale e) Chemical Spill f) Corruption g) Company Split h) Cyber Attack i) FDA/EMA/OSHA Action j) Factory Fire k) Fine l) Geopolitical m) Leadership Transition n) Legal Action o) Merger & Acquisition p) Port Disruption q) Protest/Riot r) Supply Shortage a) Earthquake b) Extreme Weather c) Flood d) Hurricane e) Tornado f) Volcano g) Human Health h) Power Outage.
        2. The disruption event the news article is reporting, must be a 'live' event, meaning it is currently happening. Not an article reporting on a past event.

        Article Title:{articleTitle}\n{articleText}\nEnd of article\n\nFeedback:{feedback}\n

        TASK: Given youre Role and the Conditions, Classify if the given news article is a vaild disruption event article or not.A vaild disruption event article is classified as "An event that potentially impacts the supply chain and have a vaild disruption type",  Select the disruption type only based on the given full list of possible disruption types. Think through and give reasoning for your decision. Must Output boolean value for isDisruptionEvent.
        """,
        input_variables=["articleTitle","articleText","feedback"]
    )
    
    # Initialize the chain
    articleClassifier = create_structured_output_chain(output_schema=classifier_article_schema,llm = classifier_llm,prompt=classifierprompt)
    '''
    )
    