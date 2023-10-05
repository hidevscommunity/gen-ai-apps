**Overview:**

The combined application utilizes three individual applications to achieve a specific workflow. Each application serves a distinct purpose and is integrated to streamline the process. This documentation provides an overview of how these applications work together.

See video demo here :
https://x.com/introsp3ctor/status/1703481100545253807

Here is the overview updated with links, images, and GitHub info in Markdown format:

# Compose Application Suite

## Overview 

The Compose Application Suite utilizes apps like [OrgClarifai](https://org-clarifai.streamlit.app/), [ZipData](https://zipdata.streamlit.app/), [jwtjwt](https://jwtjwt.streamlit.app/), [inspirationals](https://introspector.streamlit.app/), [compose.tool](https://compose.streamlit.app/), and [text-split-explorer](https://splitt.streamlit.app/) to enable secure workflows for composing and sharing messages.

## Applications

### [[Streamlit/OrgClarifai]](https://org-clarifai.streamlit.app/)

- Allows browsing and exploring Clarifai inputs organized by concepts.  
- Provides interface to run Clarifai inference on sets of inputs.
- Uses Clarifai APIs and machine learning behind the scenes.

![https://github.com/meta-introspector/https-streamlit.io-community-llm-hackathon-2023/raw/images/resources/org-clarifai.streamlit.app.jpg](https://github.com/meta-introspector/https-streamlit.io-community-llm-hackathon-2023/raw/images/resources/org-clarifai.streamlit.app.jpg)

**Repositories:**

- [Community Cloud](https://org-clarifai.streamlit.app/)
- [GitHub Repository](https://github.com/meta-introspector/https-streamlit.io-community-llm-hackathon-2023)

### [[Streamlit/ZipData]](https://zipdata.streamlit.app/)
- Enables viewing and searching zip files containing IDs and text.
- Useful for exploring and analyzing zipped datasets.

![https://github.com/meta-introspector/https-streamlit.io-community-llm-hackathon-2023/raw/images/resources/zipdata.jpg](https://github.com/meta-introspector/https-streamlit.io-community-llm-hackathon-2023/raw/images/resources/zipdata.jpg)

- Enables viewing and searching zip files containing IDs and text.
- Useful for exploring and analyzing zipped datasets.

Streamlit app for viewing and searching zip files containing IDs and text inputs.

**Repositories:**

- [Community Cloud](https://zipdata.streamlit.app/)
- [GitHub Repository](https://github.com/meta-introspector/https-streamlit.io-community-llm-hackathon-2023/blob/data/src/streamlit_data.py)


### [jwtjwt](https://jwtjwt.streamlit.app/) (Approval Application)

Streamlit app that generates URLs with JSON Web Tokens (JWTs) for embedding content or sharing resources securely.

- Interactive app for generating and sharing JSON Web Tokens (JWTs).
- Allows creating and verifying JWTs for authentication workflows.
- Implements JWT encoding/decoding using PyJWT library.

### [inspirationals](https://introspector.streamlit.app/)

- Displays RDF graphs for exploring relationships.

### [compose.tool](https://compose.streamlit.app/) (Compose Application)

- Allows composing messages by selecting approved content. 
- Provides interface to arrange messages into final output.

### [text-split-explorer](https://splitt.streamlit.app/)

- App for splitting and analyzing text data.

## Example Workflow

1. Generate JWT URL in [jwtjwt](https://jwtjwt.streamlit.app/).
2. Approve JWT URL message in [jwtjwt](https://jwtjwt.streamlit.app/).
3. Select approved message in [compose.tool](https://compose.streamlit.app/).
4. Arrange content into final composed message. 
5. Share message securely.

## GitHub

See the code for these apps in the [meta-introspector GitHub org](https://github.com/meta-introspector).
