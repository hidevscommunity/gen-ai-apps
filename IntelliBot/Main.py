import streamlit as st

st.set_page_config(
    page_title="IntelliBot",
    page_icon="🤖",
    layout="wide"
)

st.title("🌐 IntelliBot: Your Advanced Web-Enabled Chat Assistant 🤖💬")
st.write("")
st.write("")
st.write("")
description = """
    <div style="text-align: center;">
        <h3>🚀 Meet IntelliBot, an innovative web-based chat assistant that combines the power of Web data, cloud vector stores, and ChatGPT to revolutionize your conversational experience. By seamlessly integrating Web resources, cloud vector store data, and the intelligence of ChatGPT, IntelliBot ensures you receive optimal and intelligent responses to your queries!</h3>
    </div> """
# text-align: center;

st.write("""<div align="center">

</div>


- 🔍 <b>Explore, Inquire, Understand: Your Ultimate Query Companion</b>
  - ⚡️ IntelliBot simplifies the process of asking questions and seeking answers.
  - ⚡️ Whether it's scouring the vast expanse of the Web for information or drawing insights from a comprehensive database, IntelliBot ensures that your interactions are imbued with human-like responses, ensuring an exceptional user experience.

- 🔗 <b>The Power of Pinecone: Cloud Vector Store at Your Fingertips</b>
  - ⚡️ Empowered by Pinecone, a robust cloud vector store, IntelliBot harnesses advanced indexing and retrieval techniques to its advantage.
  - ⚡️ This translates to lightning-fast access to pertinent information, allowing for swift and precise responses to your queries.

- 💬 <b>Conversations that Matter: Save and Retrieve for Deeper Understanding</b>
  - ⚡️ IntelliBot doesn't stop at single queries; it allows you to save and archive entire conversations, fostering continuity and enabling a deeper level of comprehension.
  - ⚡️ Retrieve past interactions seamlessly to gain valuable insights and enrich your knowledge.

- ☁️ <b>Streamlit Cloud: Simplified Deployment for You</b>
  - ⚡️ Deployed on the reliable Streamlit Cloud platform, IntelliBot offers a seamless and scalable experience.
  - ⚡️ Accessible from anywhere, anytime, you can effortlessly harness its capabilities and embark on a frictionless journey of knowledge discovery.

- 🚀 <b>Unlocking Potential: Your Trusted Knowledge Companion</b>
  - ⚡️ IntelliBot stands as your trusted companion in unraveling the vast realm of knowledge.
  - ⚡️ Whether you're on a quest for answers, exploring innovative solutions, or engaging in meaningful conversations, IntelliBot is poised to make your pursuit of knowledge effortless.

Discover IntelliBot today and embark on a transformative journey of information exploration! 🌟


""", unsafe_allow_html=True)
st.write("---")
# st.markdown(description_1, unsafe_allow_html=True)
# st.write("---")
st.markdown("""
<div style="text-align: center;">
    <p>Made with ❤️</p>
</div> """, unsafe_allow_html=True)
