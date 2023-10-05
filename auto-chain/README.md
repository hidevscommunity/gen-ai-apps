# Auto-Chain

## Description

Autochain is a versatile and dynamic `streamlit` application specifically crafted to simplify the process of prototyping Langchain agents. With Autochain, developers can effortlessly create and iterate on agent prototypes, streamlining the testing and development process. This user-friendly tool allows for easy agent management and behavior adjustments with exceptional precision.

Autochain comes equipped with a range of features designed to enhance the prototyping experience. These include efficient memory management, automatic agent selection based on input data, and advanced functionalities like parsing tables, images, and charts from agent observations. All of these capabilities are seamlessly integrated into an intuitively designed user interface, making it a breeze to visualize and fine-tune agent prototypes.

<p align="center">
  <img src="https://i.ibb.co/QQrtRq0/Home-Page.png">

</p>

## Branches

We maintain two main branches in this repository:

- **stable**: The `stable`` branch is intended to provide a reliable and well-tested version of Auto-Chain.

- **master**: The `master` branch is used for the latest updates and development of Auto-Chain. It may include new features, enhancements, and bug fixes. Please note that this branch may occasionally be less stable due to ongoing development efforts.

## Features

- **Agent Management**: Easily create, modify, and manage Langchain agents.
- **Chat Models**: Develop and fine-tune chat models for seamless interactions.
- **Granular Behavior Control**: Address agent behavior issues with fine-grained adjustments.
- **Efficient Memory Management**: Optimize memory usage for better performance.
- **Automatic Agent Selection**: Choose agents automatically based on input data.
- **Advanced Functionality**: Parse tables, images, and charts from agent observations.
- **Intuitive User Interface**: A user-friendly design for a hassle-free experience.

## Tutorial Video

Learn how to use Autochain with our tutorial video: [Watch Tutorial](https://www.youtube.com/watch?v=ZpgRYeSTwlU)

## Getting Started

Follow these instructions to get Autochain up and running on your local machine for development and testing purposes.


### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed on your system.
- [Git](https://git-scm.com/) for version control.
- Tesseract OCR Engine
### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/auto-chain.git
   ```
2. Installing Tesseract OCR
- Windows
   - Download the Tesseract OCR installer for Windows from the official repository: https://github.com/UB-Mannheim/tesseract/wiki
   - Run the installer and follow the installation instructions.
   - Add the Tesseract installation directory to your system's PATH environment variable.
- Linux
   - On Linux, you can install Tesseract using your distribution's package manager. For example, on Ubuntu:
     ```bash
     sudo apt-get install tesseract-ocr
     ```
3. Navigate to the project directory:
   ```bash
   cd auto-chain
   ```
4. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Environment Variables
Before running Auto-Chain, you need to configure your environment variables. Follow these steps:

1. Locate the `.env_template` file in the project root directory.

2. Rename `.env_template` to `.env`. Make sure the file is named exactly `.env`.

3. Open the newly renamed `.env` file in a text editor.

4. Replace the placeholder values in the `.env` file with your actual API keys, credentials, and configuration settings.

5. Save the changes to the `.env` file.

### Usage
1. Start Autochain:
   ```bash
   streamlit run init.py
   ```
2. Open your web browser and access Autochain at http://localhost:8501.


## Deploy on Streamlit Sharing
If you want to deploy on Streamlit platform, follow these steps:

1. Visit the Streamlit Sharing website: https://www.streamlit.io
2. Log in with your Streamlit account.
3. Click "New App."
4. Connect your GitHub repository to Streamlit Sharing.
5. Configure deployment settings, including the branch to deploy from and the command to run your app.
6. Click "Deploy."

## Contributing
We welcome contributions to Autochain! To contribute, follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your feature or bug fix.
4. Make your changes and commit them with descriptive commit messages.
5. Push your changes to your GitHub fork.
6. Open a pull request to the master branch of the original repository.

## Contact
For any questions or inquiries, please contact us at ali.attieh.30797@gmail.com.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/AAAATTIEH/auto-chain/blob/master/LICENSE) file for details.

Enjoy using Autochain! We look forward to your contributions and feedback.