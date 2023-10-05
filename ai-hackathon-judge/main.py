import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler

from judge import get_judge


DEFAULT_TITLE = "Streamlit LLM Hackathon"

DEFAULT_INTRO = """Build an innovative LLM-based Streamlit app that incorporates at least one of the following LLM technologies: LangChain, AssemblyAI, Weaviate, LlamaIndex, or Clarifai.
There are five “Most Innovative Use” prize categories, one for each partner listed above.
In each category, there will be two lucky app winners. You can submit your app alone, or as a team of two.
Winners will be announced by October 5.
Join the #llm-hackathon channel on Discord to get inspiration, ask questions, and participate in mini-giveaways.
Representatives from all partners will be available to guide you as you build your LLM-based apps."""

DEFAULT_JUDGING = """1. Inventive
Your app offers new features not found in other Streamlit apps. The more unique, the better.
2. Error-Free
Your app doesn’t produce any errors during testing.
3. Public GitHub Repository
Your app’s source code is public—using secrets management to protect your API keys and credentials.
4. Hosted on Community Cloud
Your app must be publicly accessible on Streamlit's Community Cloud.
5. Tools Used
Your app uses at least one partner: LangChain, LlamaIndex, Weaviate, AssemblyAI, or Clarifai.
6. LLM Pain Points
You’ll get bonus points if your app addresses common LLM pain points like transparency, trust, accuracy, privacy, cost reduction, or ethics."""

DEFAULT_APPS = """mmz-001/knowledge_gpt
kinosal/tweet
"""


st.set_page_config(page_title="AI Hackathon Judge", page_icon="🤖")
st.title("🏅 AI Hackathon Judge 🏃🏻")


ss = st.session_state

with st.sidebar:
    with st.form("config"):
        st.header("Configuration")
        show_intermediate_steps = st.toggle("Show judge thoughts", True)
        st.divider()
        openai_api_key = st.text_input("Your OpenAI API key", placeholder="sk-xxxx", type="password")
        model = st.selectbox(
            "Model", 
            options=("gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k", "gpt-4-16k"),
            index=1,
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1, format="%.1f")
        max_retries = st.slider("Max Retries", 0, 10, 2, 1)
        if st.form_submit_button("Save"):
            ss.model_config = {
                "openai_api_key": openai_api_key,
                "model": model,
                "temperature": temperature,
                "max_retries": max_retries,
            }
            ss.show_intermediate_steps = show_intermediate_steps


st.info("""
[AI Hackathon Judge](https://github.com/xleven/ai-hackathon-judge) is an AI judge for hackathons.
Built by [xleven](https://github.com/xleven) with [LangChain](https://github.com/langchain-ai/langchain) and [Streamlit](https://streamlit.io).
""", icon="ℹ️")

with st.form("hackathon_info"):
    
    st.header("Hackathon Info")
    title = st.text_input("Title", DEFAULT_TITLE)
    intro = st.text_area("Introduction", DEFAULT_INTRO, height=200)
    judging = st.text_area("Judging Criteria", DEFAULT_JUDGING, height=200)

    st.divider()

    st.header("Submit Apps")
    apps = st.text_area(
        "Repos", DEFAULT_APPS,
        help="Support GitHub repos. One repo each line in the form of `user/repo`"
    )

    submit_button = st.form_submit_button(label="Submit", disabled="model_config" not in ss)


if submit_button:
    st.header("Judging Result")
    hackathon_info = {"title": title, "intro": intro, "judging": judging}
    repos = apps.splitlines()
    for repo in repos:
        st.subheader(repo)
        if len(repo.split("/")) != 2:
            st.error("Repo must be in the form of `user/repo`")
            continue
        try:
            judge = get_judge(hackathon_info, ss.model_config, verbose=st.secrets.get("LANGCHAIN_VERBOSE")==True)
            if ss.show_intermediate_steps:
                handler = StreamlitCallbackHandler(st.container(), max_thought_containers=10)
                result = judge.run(repo, callbacks=[handler])
            else:
                with st.status("Judging..."):
                    result = judge.run(repo)
                    st.write("Judging finished.")
        except Exception as err:
            st.error(err)
        else:
            st.success(result, icon="✅")