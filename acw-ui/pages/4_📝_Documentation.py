import streamlit as st
from PIL import Image
import utils as ut

# This should be the first line of the code
st.set_page_config(page_title='Documentation', layout='wide')
ut.add_logo()
ut.set_acw_header("ACW - Product Documentation")

def apply_style():
  st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
    list-style-type: square;
}
[data-testid="stMarkdownContainer"] p{
    margin: 0px 0px 0px;
}
</style>''', unsafe_allow_html=True)

# st.expander label font change
st.markdown("""
  <style>
    div[data-testid="stExpander"] div[role="button"] p {
    font-size: 25px;
    font-weight: bold;
    }
    .st-c8:hover {
            color: #3371FF !important;
        }
  </style>
""", unsafe_allow_html=True)

heading1 = st.expander("Introduction", expanded=False)
with heading1:
  st.markdown("Welcome to the official documentation for the ACW Automation Suite, a cutting-edge software solution crafted to streamline After Call Work (ACW) processes within contact centers. ACW plays a pivotal role in contact center operations, involving the systematic recording of vital customer interaction data after each call. This documentation serves as your comprehensive guide to unlock the full potential of the ACW Automation Suite, offering enhanced efficiency, improved productivity, and elevated customer service standards.", unsafe_allow_html=True)
  apply_style()

heading2 = st.expander("Improving the ACW Process", expanded=False)
with heading2:
  st.markdown("The ACW Automation Suite is designed to revolutionize post-call procedures in contact centers:")
  st.markdown("<br/><h6 style='text-align: left;'>Data Optimization</h6>", unsafe_allow_html=True)
  st.markdown("ACW data is a valuable resource with various applications, including improving customer interactions, generating insightful reports, supporting agent-assist applications, conducting in-depth data analysis, creating informative dashboards, and enhancing agent training programs.", unsafe_allow_html=True)
  st.markdown("<br/><h6 style='text-align: left;'>Efficiency Boost</h6>", unsafe_allow_html=True)
  st.markdown("Traditional ACW procedures can be time-consuming, as agents are required to take detailed notes during customer interactions, which can inadvertently affect their efficiency.", unsafe_allow_html=True)
  st.markdown("<br/><h6 style='text-align: left;'>Average Handling Time (AHT)</h6>", unsafe_allow_html=True)
  st.markdown("Efficient ACW management directly impacts Average Handling Time (AHT), a critical metric for contact center efficiency, which includes talk time, hold time, and ACW time.", unsafe_allow_html=True)
  st.markdown("<br/><h6 style='text-align: left;'>Automation Advantages</h6>", unsafe_allow_html=True)
  st.markdown("Automating ACW tasks with the ACW Automation Suite frees agents from note-taking and manual data entry into CRM applications, allowing them to focus exclusively on resolving customer inquiries.", unsafe_allow_html=True)
  apply_style()

heading3 = st.expander("The ACW Automation Ecosystem", expanded=False)
with heading3:
  st.markdown("The ACW Automation Suite is built on a robust architecture that seamlessly integrates a suite of essential components:", unsafe_allow_html=True)
  st.markdown("<br/><h6 style='text-align: left;'>Data Handling Hub</h6>", unsafe_allow_html=True)
  st.markdown("This core module acts as the central hub for data ingestion, effortlessly accommodating a variety of audio formats, including wav, mp3, ogg, and m4a.", unsafe_allow_html=True)
  st.markdown("<br/><h6 style='text-align: left;'>Intelligent Trigger Management</h6>", unsafe_allow_html=True)
  st.markdown("Comprising serverless orchestrations, this component vigilantly monitors designated Cloud Storage repositories for newly deposited call recordings, promptly triggering subsequent actions.", unsafe_allow_html=True)
  st.markdown("<br/><h6 style='text-align: left;'>ACW Control Center</h6>", unsafe_allow_html=True)
  st.markdown("The control center of the suite, this component is home to a potent REST API hosted on Cloud Run. It meticulously oversees transcription tasks, utilizing AssemblyAI’s transcription API, and conducts advanced analysis through ClarifAI. Insights such as call purpose, sentiment analysis, annotations, action items, conversation highlights, and agent performance evaluations are skilfully extracted.", unsafe_allow_html=True)
  st.markdown("<br/><h6 style='text-align: left;'>Data Storage Vault</h6>", unsafe_allow_html=True)
  st.markdown("Relying on the robust GCP Firestore as its document database, the suite securely preserves both structured and unstructured data, serving as the foundation for comprehensive reporting, enriched dashboard visualizations, agent assist applications, and advanced agent training initiatives.", unsafe_allow_html=True)
  apply_style()

heading4 = st.expander("The ACW Automation Process", expanded=False)#✔️☑️
with heading4:
  st.markdown("The ACW Automation Suite executes its transformative sequence of events with precision:")
  st.markdown("✅ Following the conclusion of a customer call, the recording is promptly secured within a designated Cloud Storage repository.", unsafe_allow_html=True)
  st.markdown("✅ The Cloud Function, an automation sentinel, springs into action upon detecting the arrival of a new recording.", unsafe_allow_html=True)
  st.markdown("✅ This trigger activates a RESTful invocation of the ACW Control Center, hosted on Cloud Run.", unsafe_allow_html=True)
  st.markdown("✅ The Control Center oversees audio transcription, tapping into AssemblyAI’s transcription API. Subsequently, it employs ClarifAI’s semantic brilliance, enriched by prompt engineering, to uncover valuable insights from call recordings.", unsafe_allow_html=True)
  st.markdown("✅ These insights are securely stored within GCP Firestore, preserving them for reporting, dashboards, agent assist applications, and advanced agent training endeavours.", unsafe_allow_html=True)
  st.markdown("This process is shown in the below sequence diagram for reference (figure 1.0 - ACW Automation - Sequence Of Events)", unsafe_allow_html=True)
  image = Image.open('static/sequence_diagram.png')
  st.image(image, caption='figure 1.0 - ACW Automation - Sequence Of Events')
  # st.markdown("Here is the overall architecture diagram for this application:")
  st.markdown("<br/><h6 style='text-align: left;'>Here is the overall architecture diagram for this application:</h6>", unsafe_allow_html=True)
  image = Image.open('static/arch-diag.jpeg')
  st.image(image, caption='figure 1.1 - ACW - System Architecture')
  st.markdown("This suite consists of two main components:")
  st.markdown("✅ UI Layer - Developed using Streamlit and hosted on Streamlit cloud.", unsafe_allow_html=True)
  st.markdown("✅ Backend Layer - This layer consists of Cloud function and ACW Orchestrator.", unsafe_allow_html=True)
  st.markdown("- The Cloud function detects a new object upload event on GCP cloud storage. And then triggers REST API of Orchestrator running on Cloud Run.", unsafe_allow_html=True)
  st.markdown("- The Orchestrator executes series of tasks in series through pipeline designed in Springboot application and hosted on Cloud run by dockerising the Springboot application. ACW Orchestrator talks to AssemblyAI for call recording Transcription. Then uses ClarifAI’s API (internally uses Google Vertex AI - Text-Bison model) for transcription analysis on call recording.", unsafe_allow_html=True)
  st.markdown("- Finally, the sequence of pipeline tasks ends by inserting this key information to Cloud Firestone for further analysis.", unsafe_allow_html=True)
  apply_style()

heading5 = st.expander("ACW Benefits", expanded=False)
with heading5:
  st.markdown("Some key benefits this solution brings in to Contact Center according to us:")
  st.markdown("<p style='font-weight: bold'>📌 Efficiency Enhancement:</p> The ACW Automation Suite streamlines the ACW process, reducing the time agents spend on manual note-taking and data entry. This leads to a substantial increase in operational efficiency, alleviating the pain point of productivity and cost reduction.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Data Accuracy:</p> By automating the transcription and data extraction process, the suite significantly improves the accuracy of ACW data. This ensures that vital customer interaction information is precise and reliable, mitigating the pain point of data inaccuracies.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Advanced Analytics:</p> Leveraging AI-driven analysis, the suite provides deep insights into call recordings, including call purpose, sentiment analysis, action items, and more. This empowers contact centers to make data-driven decisions, addressing the pain point of transparency and trust.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Privacy Compliance:</p> The ACW Automation Suite prioritizes data privacy and security. It ensures that sensitive customer data is handled with utmost care and complies with privacy regulations, addressing the pain point of ethics and privacy concerns.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Cost Reduction:</p> By automating ACW tasks and reducing AHT, the suite indirectly leads to cost reduction. Contact centers can optimize their resources and allocate them more efficiently, mitigating the pain point of operational costs.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Enhanced Agent Focus:</p> With the burden of manual tasks lifted, agents can focus entirely on delivering exceptional customer service and resolving queries. This helps in building trust with customers and addressing the pain point of trust and transparency.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Scalable Solutions:</p> The ACW Automation Suite is designed to evolve and adapt to the changing needs of contact centers. It can easily accommodate additional functionalities like agent assist applications, further enhancing its value proposition.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Improved Customer Service:</p> With agents empowered to provide quicker and more accurate responses, the quality of customer service is elevated. This contributes to higher customer satisfaction and trust in the contact center.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Comprehensive Reporting:</p> The suite's data storage vault enables comprehensive reporting and dashboards. Contact centers can gain a holistic view of their operations, addressing the pain point of transparency and trust.",unsafe_allow_html=True)
  st.markdown("<p style='font-weight: bold'>📌 Agent Training:</p> Valuable insights derived from call recordings can be used for advanced agent training, improving agent performance and boosting trust in agent competence.",unsafe_allow_html=True)
  st.markdown("<br/>In Conclusion, the ACW Automation Suite offers a comprehensive solution that not only addresses the pain points associated with After Call Work but also brings significant benefits in terms of efficiency, data accuracy, privacy, cost reduction, and ethics compliance, fostering transparency and trust in contact center operations.",unsafe_allow_html=True)
  apply_style()
ut.add_footer()