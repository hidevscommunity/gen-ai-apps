import streamlit as st
from streamlit_feedback import streamlit_feedback

def reset_feedback():
    st.session_state.feedback_update = None
    st.session_state.feedback = None

def user_feedback(client):
    if st.session_state.get("run_id"):
        feedback = streamlit_feedback(
            feedback_type="thumbs",
            key=f"feedback_{st.session_state.run_id}",
        )
        scores = {"👍": True, "👎": False}
        if feedback:
            score = scores[feedback["score"]]
            feedback = client.create_feedback(st.session_state.run_id, "user_score", score=score)
            st.session_state.feedback = {"feedback_id": str(feedback.id), "score": score}

    if st.session_state.get("feedback"):
        feedback = st.session_state.get("feedback")
        feedback_id = feedback["feedback_id"]
        score = feedback["score"]
        if not score:
            correction = st.text_input(
                label="What could have been the appropriate or preferred response?",
                key=f"correction_{feedback_id}",
            )
            if correction:
                st.session_state.feedback_update = {
                    "comment": correction,
                    "feedback_id": feedback_id,
                }
        else:
            comment = st.text_input(
                label="Any additional information you'd like to share !",
                key=f"comment_{feedback_id}",
            )
            if comment:
                st.session_state.feedback_update = {
                    "comment": comment,
                    "feedback_id": feedback_id,
                }

    if st.session_state.get("feedback_update"):
        feedback_update = st.session_state.get("feedback_update")
        feedback_id = feedback_update.pop("feedback_id")
        client.update_feedback(feedback_id, **feedback_update)
        reset_feedback()