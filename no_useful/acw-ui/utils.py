import streamlit as st
import base64


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(http://localhost:8501/app/static/acws1.png);
                background-repeat: no-repeat;
                padding-top: 200px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
#background-image: url(https://cdn-icons-png.flaticon.com/128/2706/2706962.png?ga=GA1.1.1108328850.1694773165);

def set_acw_header(headerstr):
    st.markdown('''
    <style>
    .stApp [data-testid="block-container"]{
        padding-top: 0rem;
        padding-left: 2rem;
    }
    </style>
    ''', unsafe_allow_html=True)

    st.markdown(""" <style>
    #MainMenu {visibility: hidden; display: none;}
    footer {visibility: hidden; display: none;}
    header {visibility: hidden; display: none;}
    </style> """, unsafe_allow_html=True)

    st.write("# " + headerstr)
    st.header('', divider='rainbow')

    #Sidebar margin reduction
    st.markdown("""
    <style>
        .css-10oheav.eczjsme4 {
        margin-top: -75px;
        }
    </style>
    """, unsafe_allow_html=True)

# Another Way to Reduce top margin
# st.markdown("""
#         <style>
#                .block-container {
#                     padding-top: 0rem;
#                     padding-bottom: 0rem;
#                     padding-left: 3rem;
#                     padding-right: 3rem;
#                 }
#         </style>
#         """, unsafe_allow_html=True)
#############

def file_download(download_filename, file_path, label_text):
    in_file = open(file_path, "rb") # opening for [r]eading as [b]inary
    data = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
    in_file.close()
    file_str = base64.b64encode(data).decode()
    href =  f'<a href="data:audio/mp4;base64,{file_str}" download="{download_filename}">{label_text}</a>'
    return href

def add_footer():
    # Footer
    st.markdown("""<a href="Home" target="_self">< Home</a>""", unsafe_allow_html=True)

def export_to_csv(df):
    csv = df.to_csv(index=False).encode('utf-8')
    st.markdown(
    """
<style>
button {
    width: auto;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
    overflow: visible;
}
</style>
""",
    unsafe_allow_html=True,
)
    st.download_button(label="Export to CSV", data=csv, file_name='acw-records.csv', mime='text/csv')
