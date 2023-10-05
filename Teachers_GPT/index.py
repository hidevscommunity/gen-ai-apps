import streamlit as st
import tlangchain_helper
import openai
import io
import pandas as pd


#Header Warning
st.warning('I’ve initially launched the curriculum generator with limited features in response to the high query rates from end users. As soon as we establish an API model for end users, I will unlock all the additional features within the app. Until 19th Sept 2023 I am allowing my personal API so no need to add your api on left corner for now. Thank you!', icon='⚠')
# Header Image
st.image("school.png", use_column_width=True)

# Page Title and Description
st.title("American Elementary School Curriculum Generator")
st.markdown("Generate curriculum outlines for elementary school grade levels. You can also export curriculam by clicking on export curriculam button given below")

# Sidebar for Additional Information
with st.sidebar:
    openai_key = st.text_input("OpenAI API Key", key="openai_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/syedabbast/Teachers_GPT)"
st.sidebar.title("Welcome, Teachers!")
# Message to Teachers
st.sidebar.markdown(
    """
    Welcome to the America Elementary Grade Curriculum Generator! 
    This user-friendly website is designed to assist you in creating curriculum outlines for various grade levels in elementary schools.
    
    **How to Use:**
    1. Start by selecting the desired grade level from the dropdown menu. You can choose from Kindergarten to Grade 5.
    2. Click on the grade level of your choice.
    3. The curriculum outline for the selected grade will be generated and displayed on the page.
    4. Feel free to explore the curriculum details, and use them as a valuable resource for your teaching plans.
    5. Don't forget to check the additional information below, including the source of this content.
    6. Enjoy the convenience of creating curriculum outlines effortlessly!
    7. Feel free to export by clicking on export button below.
    8. Once you export as it is CSV it can be opened in excel sheet and you can copy it to word document. 
    
    If you have any questions or need assistance, please don't hesitate to reach out. Happy teaching!
    
    Best regards,  
    Syed Abbas  
    tahasyed110@gmail.com  
    Twitter:[X](https://twitter.com/SyedAbbasT)
    https://medium.com/@SyedAbbasT
    """
)
st.sidebar.markdown("This is beta version, Feel free to write me and let me know what you want to generate next from chat GPT")
st.sidebar.markdown("⚠️ **Warning:** As we are short on API balance, please try it one time. Thank you! I am workin to add end user api soon.")


# Grade Level Selection Dropdown
level = st.selectbox("Select Grade Level", ["Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])

if level:
    # Generate Curriculum
    response = tlangchain_helper.generate_curriculum(level)
    
    # Display Curriculum with Styling
    st.header(f"Curriculum for {level}")
    st.write(response['level_name'])

    # Export Curriculum to CSV
    curriculum_df = pd.DataFrame({"Curriculum": [response['level_name']]})
    curriculum_csv = curriculum_df.to_csv(index=False, encoding='utf-8')
    
    # Export Button
    if st.button("Export Curriculum"):
        # Prepare curriculum file for download
        curriculum_bytes = curriculum_csv.encode('utf-8')
        curriculum_io = io.BytesIO(curriculum_bytes)
        st.download_button(
            label="Download Curriculum",
            data=curriculum_io,
            file_name=f"curriculum_{level}.csv",
            key="download_curriculum"
        )
   
    # Additional Information with Styling
   

    # Add a footer with custom HTML
    st.markdown(
        """
        <footer style="text-align:center;">
            <p>&copy; 2023 America Elementary School</p>
        </footer>
        """,
        unsafe_allow_html=True
    )
