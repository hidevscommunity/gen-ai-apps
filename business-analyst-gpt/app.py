import streamlit as st

from constants import WEB_APPLICATION, ANDROID_APP, IOS_APP, DESKTOP
from generate_features import generate_features_description, generate_features_list
from generate_srs import generate_software_requirement_specification_document
from generate_urd import generate_user_requirement_document


def main():
    st.title("Generate User Requirements Document and SRS")

    # Add URLs to the URD and SRS at the top of the page
    st.markdown(
        f"[User Requirements Document (URD) - Sample]("
        f"https://docs.google.com/document/d/1-q_nYiMjXCLs59W-z80Alsq9gv-XU4NcIRlxUS1Cut4/edit?usp=sharing)"
    )

    st.markdown(
        f"[Software Requirements Specification (SRS) - Sample]("
        f"https://docs.google.com/document/d/1xSWBieXChgttZ83rmg_s7GKioO8y2ltTtJJIgShoAg0/edit?usp=sharing)"
    )

    # Provide a brief introduction or context
    st.write(
        "Welcome to the User Requirements Document (URD) and Software Requirements Specification (SRS) generation "
        "app. Please fill in the following information to create your documents:"
    )

    st.subheader('Questions')

    answer1 = st.text_area(
        "What specific issue or challenge are you going to solve with this product? To solve those problems, what "
        "are you hoping to build?",
        placeholder='Write a detailed description of the problem you are aiming to solve. Make sure you include'
                    ' as many challenges as possible. Use the "?" icon above to see an example.',
        help='Hair salons don\'t get a steady stream of appointments (and income) in their business. They tend to have '
             'very busy weekends and very vacant weekdays. I want to build a platform that maximizes the revenue for '
             'hair salons without a need to increase the workforce. I want to build an intelligent system that can '
             'send out curated offers to their customers.',
        height=120
    )

    st.write("What platforms will this application be available for?")
    checkbox1 = st.checkbox(WEB_APPLICATION)
    checkbox2 = st.checkbox(ANDROID_APP)
    checkbox3 = st.checkbox(IOS_APP)
    checkbox4 = st.checkbox(DESKTOP)

    answer2 = st.text_area(
        "What is the main goal of the product you'd like to be developed",
        placeholder='Be very concise but include an exhaustive list of all the goals you want to focus with this'
                    'product. Use the "?" icon above to see an example.',
        help='Maximize revenue for hair salons, Give hair salon owners insights about their business, Increase '
             'efficiency of the hair salon business',
        height=60
    )

    st.subheader("Features")
    st.write("Describe the features")
    if 'num_features' not in st.session_state:
        st.session_state.num_features = 1

    features_list = []

    # Display the text areas for each feature
    st.caption('Try to be as descriptive as possible. Do not worry about structuring the input details. Attemp to add'
            'an exhaustive list of features that you need.')
    for i in range(st.session_state.num_features):
        feature = st.text_area(
            f"New Feature {i + 1}",
            placeholder=f"A detailed description or list of sub-features within a feature.",
            height=100,
            key=f'new_feature_{i}'
        )
        features_list.append(feature)

    # Button to add more features
    if st.button("Add Feature"):
        st.session_state.num_features += 1

    answer3 = "\n".join([f"{i + 1}. {item}" if item else "" for i, item in enumerate(features_list)])

    answer4 = st.text_area(
        "Who will be using this software or system? Can you describe the users briefly?",
        height=60
    )

    platform = []
    if st.button("Generate URD") and all([answer1, answer2, answer3, answer4]):
        if checkbox1:
            platform.append(WEB_APPLICATION)
        if checkbox2:
            platform.append(ANDROID_APP)
        if checkbox3:
            platform.append(IOS_APP)
        if checkbox4:
            platform.append(DESKTOP)

        answers = {"answer1": answer1, "platform": ",".join(platform) if platform else "", "answer2": answer2,
                   "answer4": answer4}

        with st.spinner("Refining features..."):
            pre_req_features_list = generate_features_list(answer3)
            features_description = generate_features_description(answer1, pre_req_features_list)
            answers["answer3"] = features_description

        with st.spinner("Generating User Requirements Document..."):
            st.session_state.urd_content = generate_user_requirement_document(answers)

            st.write(st.session_state.urd_content)
    else:
        if "urd_content" in st.session_state and st.session_state.urd_content:
            st.write(st.session_state.urd_content)
        else:
            st.warning("Please enter the missing fields.")

    if "urd_content" in st.session_state:
        if st.button("Generate SRS"):
            with st.spinner("Generating SRS Document..."):
                srs_content = generate_software_requirement_specification_document(st.session_state.urd_content)

                st.write(srs_content)


if __name__ == "__main__":
    main()
