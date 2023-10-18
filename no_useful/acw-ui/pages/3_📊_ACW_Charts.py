import streamlit as st
import utils as ut
import plotly.express as px
from google.cloud import firestore
import pandas as pd
from google.oauth2 import service_account
import plotly.express as px

st.set_page_config(page_title='ACW Charts', layout='wide')
ut.add_logo()
ut.set_acw_header("ACW - Charts and Metrics")

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["secrets-gcp"]
)

db = firestore.Client(credentials=credentials)
acw = list(db.collection(u'acw').order_by("timestampAdded", direction=firestore.Query.DESCENDING).stream())
acw_dict = list(map(lambda x: x.to_dict(), acw))
print(f"acw_dict ======> {acw_dict}")
df = pd.DataFrame(acw_dict)

df.columns = df.columns.str.replace('_', ' ')
df.columns = df.columns.str.title()

col_list = df.columns.tolist()
tsIndex = col_list.index('Timestampadded')
col_list[tsIndex] = 'Timestamp Added'
df.columns = col_list

df.index = df.index + 1
df.index.name = 'Sr No.'

fig_sentiment = px.pie(df, names='Sentiment',
                 title=f'ACW by Caller Sentiment',
                 height=300, width=200, color_discrete_sequence=px.colors.sequential.Bluered)
fig_sentiment.update_layout(margin=dict(l=20, r=20, t=30, b=0),)

fig_intent = px.pie(df, names='Intent',
                 title=f'ACW by Caller Intent',
                 height=300, width=200, color_discrete_sequence=px.colors.sequential.Emrld)
fig_intent.update_layout(margin=dict(l=20, r=20, t=30, b=0),)

col1, col2 = st.columns([1,1])
with col1:
    st.plotly_chart(fig_sentiment, use_container_width=True)

with col2:
    st.plotly_chart(fig_intent, use_container_width=True)

disclaimer = '<p style="color:Grey; font-size: 12px;">(Hover over charts to see the data pertinent to legends given on the right)</p>'
st.markdown(disclaimer, unsafe_allow_html=True)
# st.markdown("""
#     <br/><br/>
#     """, unsafe_allow_html=True)

# fig_tags = px.pie(df, names='Sentiment',
#                  title=f'ACW by tags',
#                  height=300, width=200)
# fig_tags.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
# col1, col2, col3 = st.columns([2,3,2])
# with col2:
#     st.plotly_chart(fig_tags, use_container_width=True)

# chart_data = pd.DataFrame(
#     df,
#     columns=["a", "b", "c"])

# st.bar_chart(chart_data)
ut.add_footer()