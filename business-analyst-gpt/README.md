# Hackathon-Task
It is a task to generate the Software Requirement Specification document from the user questionnaire.

### Stack Details
- Python = 3.9

### Steps to Execute:
- Create the virtual environment using the command
  ```
  python3 -m venv your-env-name`
  ```
- Activate the virtual environment using the command
  ```
   source env_name/bin/activate
  ``` 
- Install the requirements using the command
  ```
  pip install -r requirements.txt
  ```
- Execute the Streamlit app on local host using the command
  ```
  streamlit run app.py
  ```
  
### How it Works?
The following app is divided into two tasks.

#### Generate URD from Questionnaire:
In this task, we generate a User Requirement Document taking on the user questionnaire regarding the challenges, solutions, features, and users involved in it.

#### Generate SRS from URD:
In this task, we generate an appropriate Software Requirement Document taking in the URD Document.
