# Description: Main App File
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from constants import EMAIL_API, OPENAI_API
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import eda_functions as eda
import pyperclip
import requests
from pycaret import classification, regression
import openai
from joblib import dump as jb_dump, load as jb_load
import random, string
import socket
import pickle
import time
import os

# Config Variables
user_id = socket.gethostbyname(socket.gethostname())
url = 'https://api.openai.com/v1/chat/completions'
headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API}'
        }
length_captcha = 4
width = 200
height = 150


# Functions
def data_preprocessing(df):
    # Missing values
    with st.spinner('Missing values...'):
        time.sleep(1)
        for column in df.columns:
            if df[column].dtype == 'object' or df[column].dtype == 'bool':
                most_frequent_value = df[column].mode()[0]
                df[column].fillna(most_frequent_value, inplace=True)
            else:
                df[column].fillna(df[column].mean(), inplace=True)

    # Outliers
    with st.spinner('Outliers...'):
        time.sleep(1)
        numeric_cols = df.select_dtypes(include=['int', 'float']) 
        outlier_cols = [] 

        for column in numeric_cols:
            Q1 = df[column].quantile(0.25)  # 1st quartile
            Q3 = df[column].quantile(0.75)  # 3rd quartile
            IQR = Q3 - Q1 

            lower_bound = Q1 - 1.5 * IQR 
            upper_bound = Q3 + 1.5 * IQR 

            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

            if len(outliers) > 0:
                outlier_cols.append(column)
                x_train = df[~df[column].isin(outliers[column])][column].values.reshape(-1, 1)
                y_train = df[~df[column].isin(outliers[column])][column].values.reshape(-1, 1)
                x_pred = outliers[column].values.reshape(-1, 1)

                reg = LinearRegression()
                reg.fit(x_train, y_train)
                y_pred = reg.predict(x_pred)

                df.loc[outliers.index, column] = y_pred.flatten()

    # Categorical encoding
    with st.spinner('Performing categorical encoding...'):
        time.sleep(1)
        for column in df.select_dtypes(include='object'):
            encoder = LabelEncoder()
            df[column] = encoder.fit_transform(df[column])

    # Data polishing steps
    with st.spinner('Performing data polishing steps...'):
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
        df_cleaned = df_scaled.dropna().reset_index(drop=True)

    return df_cleaned

def send_simple_message(text):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxebd1ff2187ca4bf6a7610daf43c30c0a.mailgun.org/messages",
        auth=("api", EMAIL_API),
        data={"from": "Mailgun Sandbox <postmaster@sandboxebd1ff2187ca4bf6a7610daf43c30c0a.mailgun.org>",
            "to": "Gregor Melon <supwithproject@gmail.com>",
            "subject": "User Feedback",
            "text": text})


# Set Page Config
st.set_page_config(
    page_title = 'DataFlow App',
    page_icon = '📊',
    layout = 'wide',
    initial_sidebar_state = 'auto',
)

# Set Page Style
with st.sidebar:
    st.sidebar.image('media/logo.png', use_column_width=True)
    selected = option_menu(
        menu_title = None,
        options = ['Home', 'Definition', 'Collection', 'Upload', 'Profiling', 'Normalizing', 'Training', 'Download', 'Deploying'],
        icons = ['house', 'book', 'bi-database-add', 'cloud-upload', 'bi-graph-up-arrow', 'bi-funnel-fill', 'bi-hypnotize', 'cloud-download', 'rocket'],
        default_index = 0
    )
    st.info('Educational Low-Code ML Web Platform for beginners in Data Science.')
    st.caption('Made with ❤️ by [DataFlow](https://dataflow.kz) team.')

# Set Main Content
if selected == 'Home':
    st.header('DataFlow: Your Path to Simplified Machine Learning', help='Educational Low-Code ML Web Platform for beginners in Data Science.')
    
    st.markdown("<code style='font-size: 14px;'>Learn and Apply Machine Learning Methods without Deep Programming and Data Analytics Knowledge</code>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Advantages of Learning on Dataflow")

    st.markdown("Dataflow is an educational Low-Code web platform, perfect for beginners in the field of Data Science.")
    st.markdown("- Convenient Environment: Dataflow provides an intuitive interface, reducing barriers in terms of programming complexity and data analytics.")
    st.markdown("- Creating Real Projects: The platform allows you to create and implement real ML projects for practical application.")
    st.markdown("- Low Entry Barrier: Even with limited programming knowledge, users can learn the concepts and methods of machine learning on Dataflow.")
    st.markdown("- Bridging the Gap: Dataflow bridges the gap between complex machine learning algorithms and users who may not have extensive data analytics and programming skills.")

    st.markdown("---")
    st.subheader("Additional Information")

    st.markdown("Begin your journey into the world of Data Science with Dataflow and immerse yourself in learning and applying machine learning methods without unnecessary complexity!")

    st.markdown("---")
    st.subheader("Contact Information")

    st.markdown("If you have any questions or suggestions, feel free to contact us:")
    st.markdown("- Email: info@dataflow.com")
    st.markdown("- Phone: +7(777)-7777-777")
    st.markdown("- Address: Mangilik El, 58, Astana")

    st.markdown("---")
    st.subheader("Leave a Feedback")

    feedback = st.text_area("Enter your feedback", "")

    if st.button("Submit Feedback"):
        send_simple_message(feedback)
        st.markdown("Thank you for your feedback!")


########################
# Data Science Section #
########################

####################
# Definition Stage #
####################
if selected == 'Definition':
    st.title('Bussiness Objective Definition', help='Business objective definition refers to the process of clearly identifying and defining the specific goals and objectives that the machine learning project aims to achieve in a business context.')
    st.subheader('💬 Chat Window')
    request = st.text_area('Chat Here', height=100, max_chars=None, key=None, placeholder='Type your business problem or ideas here...')
    send = st.button('Send')
    data = None
    if send:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f'Act as a professional business analyst with experience in data processing and evaluate the idea for integrating a machine learning model. Write no more than 5 sentences. \nIdea: {request}'}],
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()['choices'][0]['message']['content']
        st.subheader('Response: ')
        st.write(data)
    if data:
        st1, st2, _, __ = st.columns(4)
        with st1:
            st.download_button('save', data=data, file_name='business_objective.txt')
        
        with st2:
            copy = st.button('copy')
            if copy:
                pyperclip.copy(data)
                st.success("Copied to clipboard!")
    
    expander = st.expander("See explanation")
    expander.write("""
        In machine learning, a `business objective` refers to the specific goal or problem that an organization aims to solve using machine learning techniques. It defines the desired outcome or value that the machine learning model is expected to deliver in order to address a business challenge or opportunity. The business objective provides the foundation for developing an effective machine learning solution tailored to the organization's needs.

        Here's a more detailed explanation of business objective definition in machine learning:

        * Identify the problem or opportunity.
        * Set specific and measurable goals.
        * Define the scope and constraints.
        * Establish success criteria for evaluation.
        * Align with stakeholders' needs and expectations.

        By clearly defining the business objective in machine learning, organizations can focus their efforts on developing models and solutions that directly address the identified problem or opportunity. It provides a clear direction and evaluation framework for building and deploying machine learning models that deliver measurable value to the business.
    """)
    
        

###################
# Data Collection #
###################        
if selected == 'Collection':
    st.title('Data Collection', help='Data collection refers to the process of gathering and accumulating the necessary data to train and build a machine learning model.')
    st.subheader('📃 Table Auto-Maker')
    text = st.text_area('Chat here', placeholder='Type your colum names, give examples or just write about your table ideas...', height=100, max_chars=None, key=None)
    make_table = st.button('Make Table')
    data = None
    if make_table:
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f'Act as Professional Data Engineer with 10+ year experience, using your skills generate table by this details. \nTable details: {text}'}],
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()['choices'][0]['message']['content']
        with st.spinner('Generating table...'):
            time.sleep(2)
            st.success('Table is generated successfully!')
            st.write(data)
    if data:
        st1, st2, _, __ = st.columns(4)
        with st1:
            st.download_button('save', data=data, file_name='datatable.xlsx')
        
        with st2:
            copy = st.button('copy')
            if copy:
                pyperclip.copy(data)
                st.success("Copied to clipboard!")
    expander = st.expander("See explanation")
    expander.write("""
        `Data collection in machine learning` refers to the process of gathering relevant and representative data from various sources to build a high-quality dataset for training and testing machine learning models. It involves systematically collecting and organizing data that is essential for addressing the problem or achieving the business objective at hand.
        * Identify data requirements.
        * Determine data sources.
        * Obtain permissions and ensure compliance.
        * Perform data sampling.
        * Preprocess the data.
        * Annotate or label the data.
        * Store and manage the data.
        * Consider data augmentation techniques.
        * Iterate and refine data collection efforts.
    """)

##################
# Upload Dataset #
##################
if selected == 'Upload':
    st.title('Upload Dataset', help='Click «Upload» to upload dataset for further Data Engineering.')
    file_format = st.radio('Select file format:', ('csv', 'excel'), key='file_format')
    dataset = st.file_uploader(label='Upload Dataset', type=['csv', 'xlsx'], key='dataset')
    # default dataset
    use_defo = st.checkbox('Use default dataset', key='use_defo')
    if use_defo:
        dataset = 'test/titanic.csv'
        file_format = 'csv'

    if dataset:
        st.success('Dataset is uploaded successfully!')
        try:
            if file_format == 'csv':
                df =  pd.read_csv(dataset)
                user_id += '.csv'
            else:
                df = pd.read_excel(dataset)
                user_id += '.xlsx'
            st.subheader('Dataframe:')
            n, m = df.shape
            st.write(f'<p style="font-size:130%">Dataset contains {n} rows and {m} columns.</p>', unsafe_allow_html=True)   
            st.dataframe(df)
            df.to_csv(f'datasets/{user_id}', index=False)
            st.session_state['user_id'] = user_id
        except Exception as e:
            st.error(f'Please, upload correct dataset! \nError: {e}')

###############
# EDA Section #
###############
# Title: Exploratory Data Analysis in Streamlit
# Medium: https://medium.com/analytics-vidhya/streamlit-app-for-exploratory-data-analysis-293a6c3f841
# Github: https://github.com/anarabiyev/EDA_Streamlit_App 
if selected == 'Profiling':
    st.title('Exploratory Data Analysis (EDA)', help='Exploratory Data Analysis (EDA) is a crucial initial step in the data analysis process, which involves exploring and summarizing the main characteristics, patterns, and relationships present in a dataset.')
        
    if 'user_id' in st.session_state:
        st.write(st.session_state)
        df = pd.read_csv(f'datasets/{st.session_state["user_id"]}')

        st.subheader('Data Statistics')
        all_vizuals = ['Info', 'NA Info', 'Descriptive Analysis', 'Target Analysis', 
                   'Distribution of Numerical Columns', 'Correlation Heatmap', 'Count Plots of Categorical Columns', 
                   'Box Plots', 'Outlier Analysis', 'Variance of Target with Categorical Columns']
        vizuals = st.multiselect('Select Visualizations', all_vizuals, default = all_vizuals)
        if 'Info' in vizuals:
            st.subheader('Info:')
            c1, c2, c3 = st.columns([1, 2, 1])
            c2.dataframe(eda.df_info(df))
        if 'NA Info' in vizuals:
            st.subheader('NA Value Information:')
            if df.isnull().sum().sum() == 0:
                st.write('There is not any NA value in your dataset.')
            else:
                c1, c2, c3 = st.columns([0.5, 2, 0.5])
                c2.dataframe(eda.df_isnull(df), width=1500)
                eda.space(2)
        if 'Descriptive Analysis' in vizuals:
            st.subheader('Descriptive Analysis:')
            st.dataframe(df.describe())
        if 'Target Analysis' in vizuals:
            st.subheader("Select target column:")    
            target_column = st.selectbox("", df.columns, index = len(df.columns) - 1)

            st.subheader("Histogram of target column")
            fig = px.histogram(df, x = target_column)
            st.plotly_chart(fig)
        
        num_columns = df.select_dtypes(exclude = 'object').columns
        cat_columns = df.select_dtypes(include = 'object').columns
        
        if 'Distribution of Numerical Columns' in vizuals:
            if len(num_columns) == 0:
                st.write('There is no numerical columns in the data.')
            else:
                selected_num_cols = eda.sidebar_multiselect_container('Choose columns for Distribution plots:', num_columns, 'Distribution')
                st.subheader('Distribution of numerical columns')
                i = 0
                while (i < len(selected_num_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_num_cols)):
                            break

                        fig = px.histogram(df, x = selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width = True)
                        i += 1

        if 'Correlation Heatmap' in vizuals:
            if len(num_columns) == 0:
                st.write('There are no numerical columns in the data.')
            elif len(num_columns) > 0:
                st.subheader('Correlation Heatmap')
                corr_matrix = df[num_columns].corr()
                fig = px.imshow(corr_matrix,
                                x=corr_matrix.columns,
                                y=corr_matrix.columns,
                                color_continuous_scale='Viridis')
                fig.update_layout(title='Correlation Heatmap',
                      xaxis=dict(title='Features'),
                      yaxis=dict(title='Features'))
                st.plotly_chart(fig, use_container_width = True)
                

        if 'Count Plots of Categorical Columns' in vizuals:
            if len(cat_columns) == 0:
                st.write('There is no categorical columns in the data.')
            else:
                selected_cat_cols = eda.sidebar_multiselect_container('Choose columns for Count plots:', cat_columns, 'Count')
                st.subheader('Count plots of categorical columns')
                i = 0
                while (i < len(selected_cat_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:

                        if (i >= len(selected_cat_cols)):
                            break

                        fig = px.histogram(df, x = selected_cat_cols[i], color_discrete_sequence=['indianred'])
                        j.plotly_chart(fig)
                        i += 1
        
        if 'Box Plots' in vizuals:
            if len(num_columns) == 0:
                st.write('There is no numerical columns in the data.')
            else:
                selected_num_cols = eda.sidebar_multiselect_container('Choose columns for Box plots:', num_columns, 'Box')
                st.subheader('Box plots')
                i = 0
                while (i < len(selected_num_cols)):
                    c1, c2 = st.columns(2)
                    for j in [c1, c2]:
                        
                        if (i >= len(selected_num_cols)):
                            break
                        
                        fig = px.box(df, y = selected_num_cols[i])
                        j.plotly_chart(fig, use_container_width = True)
                        i += 1

        if 'Outlier Analysis' in vizuals:
            st.subheader('Outlier Analysis')
            st.dataframe(eda.number_of_outliers(df))

        if 'Variance of Target with Categorical Columns' in vizuals:
            df_1 = df.dropna()
            high_cardi_columns = []
            normal_cardi_columns = []

            for i in cat_columns:
                if (df[i].nunique() > df.shape[0] / 10):
                    high_cardi_columns.append(i)
                else:
                    normal_cardi_columns.append(i)


            if len(normal_cardi_columns) == 0:
                st.write('There is no categorical columns with normal cardinality in the data.')
            else:
            
                st.subheader('Variance of target variable with categorical columns')
                model_type = st.radio('Select Problem Type:', ('Regression', 'Classification'), key = 'model_type')
                selected_cat_cols = eda.sidebar_multiselect_container('Choose columns for Category Colored plots:', normal_cardi_columns, 'Category')
                
                if 'Target Analysis' not in vizuals:   
                    target_column = st.selectbox("Select target column:", df.columns, index = len(df.columns) - 1)
                
                i = 0
                while (i < len(selected_cat_cols)):
                    if model_type == 'Regression':
                        fig = px.box(df_1, y = target_column, color = selected_cat_cols[i])
                    else:
                        fig = px.histogram(df_1, color = selected_cat_cols[i], x = target_column)

                    st.plotly_chart(fig, use_container_width = True)
                    i += 1

                if high_cardi_columns:
                    if len(high_cardi_columns) == 1:
                        st.subheader('The following column has high cardinality, that is why its boxplot was not plotted:')
                    else:
                        st.subheader('The following columns have high cardinality, that is why its boxplot was not plotted:')
                    for id, i in enumerate(high_cardi_columns):
                        st.write(f'{id+1}) `{i}`')
                    
                    st.write('<p style="font-size:140%">Do you want to plot anyway?</p>', unsafe_allow_html=True)    
                    answer = st.selectbox("", ('No', 'Yes'))

                    if answer == 'Yes':
                        for i in high_cardi_columns:
                            fig = px.box(df_1, y = target_column, color = i)
                            st.plotly_chart(fig, use_container_width = True)
    else:
        st.warning('Dataset is not uploaded yet!')
    expander = st.expander("See explanation")
    expander.write("""
        `Exploratory Data Analysis (EDA)` is an approach to analyzing and summarizing data to gain insights and better understand the underlying patterns, relationships, and distributions within the dataset. It involves using various statistical and visualization techniques to explore the data and uncover meaningful information.

        The primary goals of EDA are as follows:

        * Data Familiarity;

        * Data Quality;

        * Descriptive Statistics;

        * Data Visualization;

        * Feature Selection;
        
        * Hypothesis Generation;

        * Insights and Decision Making;

        Overall, exploratory data analysis is a crucial step in the data analysis workflow. It helps analysts develop an intuition for the data, identify potential issues, and form the basis for more advanced statistical modeling or machine learning techniques. EDA enables data-driven decision-making and provides a solid foundation for extracting valuable insights from the data.
    """)

#####################
# Normalizing Stage #
#####################
if selected == 'Normalizing':
    st.title('Data Preprocessing', help='Data preprocessing refers to the steps and techniques used to prepare and transform raw data into a format that is suitable for machine learning algorithms.')
    if 'user_id' in st.session_state:
        df = pd.read_csv(f'datasets/{st.session_state["user_id"]}')
        normalized_df = []

        # Tabs Manipulation
        tab1, tab2, tab3, tab4 = st.tabs(["Missing Values", "Outliers", "Categorical Encoding", "Polishing Steps"])

        with tab1:
            st.header("Missing Values")
            st.text("Missing values refer to the absence of data in certain variables or columns of a dataset.")

        with tab2:
            st.header("Outliers")
            st.text("Outliers are extreme values that significantly differ from the majority of the data points in a dataset.")

        with tab3:
            st.header("Categorical Encoding")
            st.text("Categorical encoding is the process of converting categorical variables or features into numerical representations that machine learning algorithms can process.")
        
        with tab4:
            st.header("Polishing Steps")
            st.text("Polishing steps refer to the final stages of data preprocessing and preparation, where the focus is on refining and improving the quality and structure of the dataset before analysis or modeling.")

        dataprep = st.button('Start Data Preprocessing')
        if dataprep:
            normalized_df = data_preprocessing(df)
            st.subheader('Normalized Dataset: ')
            st.dataframe(normalized_df)
            normalized_df.to_csv(f'datasets/{st.session_state["user_id"]}', index=False)
            if isinstance(normalized_df, pd.DataFrame):
                st.download_button('Save as CSV', data=normalized_df.to_csv(index=False), file_name='normalized_dataset.csv')
    else:
        st.warning('Dataset is not uploaded yet!')
    expander = st.expander("See explanation")
    expander.write("""
        `Data preprocessing` is an essential step before analyzing or modeling data. It involves cleaning the data by handling missing values, outliers, and inconsistencies. Integration combines multiple data sources, while transformation modifies data to meet analysis requirements, such as scaling or encoding. Data reduction reduces dimensionality, and techniques like oversampling address imbalanced data. Preprocessing ensures data quality, improves analysis accuracy, and enables more effective modeling and decision-making.`
    """)
######################
# Training & Testing #
######################
if selected == 'Training':
    st.title('ML Model Training & Testing', help='Training a machine learning model involves teaching it to learn from examples, while testing is when the model predicts outcomes and compares them to the correct answers.')
    if 'user_id' in st.session_state:
        try:
            ml_type = st.selectbox('Select ML Algorithm Type', ['Classification', 'Regression'], key='ml_type', index=0)
            df = pd.read_csv(f'datasets/{st.session_state["user_id"]}')
            if ml_type == 'Classification':
                target = st.selectbox('Select You Target', df.columns)
                if st.button('Start Training'):
                    classification.setup(df, target=target, index=True)
                    setup_df = classification.pull()
                    with st.spinner('Generating Experiment Settings...'):
                        st.info('This is the ML Experiment Settings')
                        st.dataframe(setup_df)
                    st.session_state['target'] = target
                    st.session_state['df_columns'] = df.columns
                    with st.spinner('Training...'):
                        best_model = classification.compare_models()
                        compare_df = classification.pull()
                        st.info('This is the ML Experiment Results')
                        st.dataframe(compare_df)
                    with st.spinner('Saving Model...'):
                        time.sleep(2)
                        best_model
                        classification.save_model(best_model, f'models/{user_id}')
                        st.success('Training is completed!')
                        st.info('You can download trained model in «Download» section.')
            else:
                target = st.selectbox('Select You Target', df.columns)
                if st.button('Start Training'):
                    regression.setup(df, target=target, index=True)
                    setup_df = regression.pull()
                    st.info('This is the ML Experiment Settings')
                    st.dataframe(setup_df)
                    st.session_state['target'] = target
                    st.session_state['df_columns'] = df.columns
                    with st.spinner('Training...'):
                        best_model = regression.compare_models()
                        compare_df = regression.pull()
                        st.info('This is the ML Experiment Results')
                        st.dataframe(compare_df)
                    with st.spinner('Saving Model...'):
                        time.sleep(2)
                        best_model
                        regression.save_model(best_model, f'models/{user_id}')
                        st.success('Training is completed!')
                        st.info('You can download trained model in «Download» section.')
                    st.session_state['best_model'] = user_id + '.pkl'
        except Exception as e:
            st.warning(f'Something Went Wrong, Please Try Again. Error: {e}!')
    else:
        st.warning('Dataset is not uploaded yet!')
    
    expander = st.expander("See explanation")
    expander.write("""
        `ML model training` involves teaching an algorithm on a labeled dataset to learn patterns and make accurate predictions. Model testing evaluates the trained model's performance on unseen data using metrics like accuracy and precision. Training optimizes model parameters, while `testing` assesses its generalization and effectiveness.
    """)

##########################
# Download Trained Model #
##########################
if selected == 'Download':
    st.title('Download ML Model', help='Click «Download» to download the latest generated ML model.')
    if 'best_model' in st.session_state:
        with open(f'models/{st.session_state["best_model"]}', 'rb') as f:
            st.download_button('Download the Model', f, 'best_model.pkl')
    else:
        st.warning('Model is not trained yet!')

######################
# Deploying ML Model #
######################
if selected == 'Deploying':
    st.title('Deploying ML Model', help='Deploying machine learning model means making it available and operational for use in real-world applications.')
    if 'best_model' in st.session_state:
        st.subheader('Prediction Form')
        # Load the model
        nb_predict_train = jb_load(f'models/{st.session_state["best_model"]}')
        columns = st.session_state['df_columns']
        target = st.session_state['target']
        inputs = []

        # Add input fields for user input
        for column in columns:
            if column == target:
                continue
            inputs.append(st.text_input(column))
        
        # Add a button to trigger the prediction
        if st.button("Predict"):
            # Perform prediction using the loaded model
            prediction = nb_predict_train.predict(inputs) 
            
            # Display the prediction result
            st.write("Prediction:", prediction)
        
        st.code('''
            import streamlit as st
            from joblib import load as jb_load
            import numpy as np

            st.subheader('Prediction Form')

            # Load the model
            nb_predict_train = jb_load('best_model.pkl')

            # Get the column names
            columns = nb_predict_train.named_steps['preprocessor'].get_feature_names_out()

            # Get the target column
            target = 'your_target_column'

            # Create an empty list to store user inputs
            inputs = []

            # Add input fields for user input
            for column in columns:
                if column == target:
                    continue
                inputs.append(st.text_input(column))

            # Add a button to trigger the prediction
            if st.button("Predict"):
                # Perform prediction using the loaded model
                input_array = np.array(inputs).reshape(1, -1)
                prediction = nb_predict_train.predict(input_array)
                
                # Display the prediction result
                st.write("Prediction:", prediction)
        ''', language='python')
        button = st.button('Finish')
        if button:
            st.success('Congratulations! You have successfully completed the DataFlow ML Web Platform.')
            st.balloons()
    else:
        st.warning('Model is not trained yet!')
    expander = st.expander("See explanation")
    expander.write("""
        `Deploying a machine learning (ML) model` refers to making the trained model available for use in real-world applications or systems. Here's a brief explanation of the deployment process:

        * Package the trained model and dependencies.

        * Set up the required infrastructure.

        * Serve the model through an interface or API.

        * Monitor and maintain the model's performance.

        * Ensure scalability and integration with other systems.

        * Address security and privacy concerns.

        Deploying an ML model enables its use in real-world scenarios, where it can provide valuable predictions, insights, or decision-making support. Effective deployment ensures that the model is accessible, reliable, and performs well within the intended production environment.
    """)
