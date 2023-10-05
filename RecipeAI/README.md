# RecipeAI

This is the submission for the Streamlit LLM Hackathon.

## Setup

### Prerequisites

Python (at least 3.9.0) must be installed on your system.

After Python has been set up, install the `virtualenv` package to create and manage a virtual environment for this project. This helps you maintain the project's dependencies in a hassle-free manner, without installing any unnecessary packages globally throughout your system.

```
pip install virtualenv
```

### 1. Clone the Project

Clone this project to create a local copy of it on your system:

```shell
git clone "https://github.com/Iam-SilentEyes/RecipeAI.git"
```

Then, move into the project folder:

```shell
cd RecipeAI
```

### 2. Create a Virtual Environment

Create a virtual environment inside the project folder to isolate its dependencies:

```shell
python -m venv env

# or

python3 -m venv env
```

Next, activate the virtual environment:

```shell
# on Windows:
.\env\Scripts\activate

# on MacOS or Linux
source env/bin/activate
```

You can deactivate this environment when you are done working with the project:

```shell
# on Windows, MacOS or Linux
deactivate
```

### 3. Install Dependencies

Set up your project with the necessary packages and libraries. After activating the virtual environment, enter the following command:

```shell
pip install -r requirements.txt
```

### 4. Setup Streamlit Secrets

To store your Clarifai <b>PAT</b> (Personal Access Token) and other sensitive information, create a folder named `.streamlit` within the project folder.

Next, create a file named `secrets.toml` within that folder. Enter the following into that file:

```
PAT = "a-very-random-string-of-characters"
APP_ID = "foo"
USER_ID = "bar"
WORKFLOW_ID = "foo-bar"
```

1. You can obtain your `PAT` from your <a href="https://clarifai.com/settings">Clarifai Account Settings</a>.
2. The `APP_ID` is the unique ID of whatever app you have created and wish to connect to from your Streamlit app.
3. The `USER_ID` is simply your username.
4. The `WORKFLOW_ID` will be set up in the next step.

### 5. Setup Clarifai Workflow

After you have created an app on the Clarifai platform and completed the above steps, create a new <b>Workflow</b> in that app.

Next, press "Edit workflow" to add the Llama2 model to the Workflow.

In the window that opens up, drag and drop a `text-to-text` chip, connect it to the `IN` node, and set the `text-to-text` chip's model as one of the Text to text LLMs.

Finally, copy the name of the workflow and include it in the `WORKFLOW_ID` of `.streamlit/secrets.toml` that was created earlier.

### 6. Start Streamlit

After you have completed the above steps, you can start the Streamlit app.

```shell
streamlit run <filename>.py
```

For example,

```shell
streamlit run app.py
```

Streamlit will start up in `localhost:8501`.
