# EmoPulse: The Psychological Counselor

## Overview
EmoPulse is a psychological counseling platform that uses Computer Vision and Signal Processing for emotion recognition, and heart rate analysis.

## Project Links
1. [Webapp](https://louisljz-emopulse.streamlit.app/) *Reboot if faced with memory issues*
2. [Webapp Demo](https://youtu.be/6UgtocM-v2g)
3. [Pitch Deck Presentation](https://youtu.be/0R5s9t_auLU)

## Usage
1. Start Monitor, and get live data of emotion recognition.
2. Stop Monitor, and get emotion tracking and heart metric reports.
3. Go to Counsel Tab, Select informations that you want to give to the chatbot.
4. Fill-up required values, press counsel button, and recieve feedback from AI.

## Technology used
- Streamlit for web application
- GPT-4 for LLM integration (Clarifai Model wrapped in LangChain)
- Photoplethysmography (PPG) for heart rate analysis
- AssemblyAI speech recognition and GTTS
- DeepFace Facial Atrribute Analysis

## Directory Structure
```
EmoPulse-main/
├── .gitignore
├── app.py # webapp
├── helpers.py # heart metric calculations
├── packages.txt
├── requirements.txt
└── text/ # prompt templates
    ├── human_template.txt
    ├── instructions.txt
    └── system_role.txt
```

## Running the App Locally

1. **Clone the Repository**:  
   ```
   git clone https://github.com/Louisljz/EmoPulse.git
   ```

2. **Install Virtual Environment**:  
   ```
   python -m venv venv
   ```
   Activate the virtual environment:
   - On Windows: `venv\Scripts\Activate`
   - On macOS and Linux: `source venv/bin/activate`

3. **Install Required Packages**:  
   ```
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**:  
   ```
   streamlit run app.py
   ```

5. **Open the App**:  
   The app should now be running. Open your web browser and go to `http://localhost:8501/` to interact with the app.

## Applications

1. **Mental Health Assessment**: Useful for psychologists and therapists.
2. **Fitness and Wellness**: Monitor cardiovascular health.
3. **Telehealth Services**: Provide real-time data to healthcare providers.

## User Trust & Ethics
- Immediate deletion after processing speech transcription.
- Encrypted data transmission to trusted sources.

## Future Directions
- Mobile applications for iOS and Android
- Expanded monitoring capabilities, including blood pressure and respiratory rate

## Disclaimer
- Emotion Recognition and Pulse Signal Processing are still in BETA stage, so it may present some inaccuracies.
- Factors like room lighting and stability significantly impact the readings.

## Contact
- Louis JZ: louis.ljz08@gmail.com
- Sreekanth Gopi: sree0912555@gmail.com
