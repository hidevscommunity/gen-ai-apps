import streamlit as st
import utils as ut
from google.cloud import firestore
from google.oauth2 import service_account
import pandas as pd

st.set_page_config(page_title='ACW Records', layout='wide')
ut.add_logo()
ut.set_acw_header("ACW - Records")

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["secrets-gcp"]
)

def load_dataframe(calledFrom):
    print(f"called from === {calledFrom}")
    db = firestore.Client(credentials=credentials)
    acw = list(db.collection(u'acw').order_by("timestampAdded", direction=firestore.Query.DESCENDING).stream())
    acw_dict = list(map(lambda x: x.to_dict(), acw))
    # print(f"acw_dict ======> {acw_dict}")
    return acw_dict

col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([1,1,1,1,1,1,1,1,8,2.5])

with st.spinner(text="Getting ACW data..."):
    css = r'''
    <style>
        [data-testid="baseButton-secondary"] {
            border-style: solid;
            }
        .css-7ym5gk:hover {
            border-color: black;
            color: black;
        }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

    # Change the font side of button 
    # st.markdown("""
    #     <style>
    #         div[data-testid="stMarkdownContainer"] p {
    #             font-size: 15px;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)
   
    acw_dict = load_dataframe("Main")
    df = pd.DataFrame(acw_dict)
    df.columns = df.columns.str.replace('_', ' ')
    df.columns = df.columns.str.title()

    col_list = df.columns.tolist()
    tsIndex = col_list.index('Timestampadded')
    col_list[tsIndex] = 'Timestamp Added'
    df.columns = col_list

    df.index = df.index + 1
    df.index.name = 'Sr No.'
    with col10:
        st.button("Refresh", on_click=load_dataframe, args=['refresh button'])
    
    st.dataframe(df, use_container_width=True)
    
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([3,1,1,1,1,1,1,1,5,3])
    with col10:
        ut.export_to_csv(df)
    with col1:
        st.markdown("""<a href="Home" target="_self">< Home</a>""", unsafe_allow_html=True)
# ut.add_footer()