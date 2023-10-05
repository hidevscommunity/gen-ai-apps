# After Call Work (ACW) Automation
## Step-by-step instructions for using the demo/MVP product:
1. Please go to https://after-call-work.streamlit.app, hosted on Streamlit cloud.
2. On the landing page, you can see the product highlights and terminologies.
3. On the left side navigation bar, you can see the features or option this product supports for now (version 1)
4. To play around and test this product head over to 'ACW Playground' allows you to upload an call recording file of types mp3, wav, ogg, m4a for now. If you don't have a sample call recordings, you can download a audio file from the sample files we have provided in the next section of ACW Playground. (we have 3 types of audio file representing sentiment of the call recording). Once you download any of the file, you can upload the file in the first section. File gets uploaded to cloud storage and pipeline of events gets triggered.
5. Once the processing of the audio file is completed, which is usually takes between 1-2 mins, the extracted data including summary, intent will be displayed in 'ACW Records' option from the navigation bar. Before you upload any file, the ACW Records display the historical data from previously uploaded files. The newly uploaded audio file's record will be shown in the first row after processing is completed.
6. 'ACW Charts' provides charts for metrics representation which helps in understanding the metrics thats happening in the contact center. We are showing the metrics of 'Caller Sentiment' and 'Caller Intent'. This is displayed as a pie chart here.
7. The 'Documentation' feature provides detailed explanation of the product, usage, why and how we did this including architecture diagram, sequence of events starting from uploading a file and report generation. We also have a dedicated section with benefits of this automation using Generative AI.
8. finally the 'Contact us' section provides the details how to reach us for any inquiry.

## Sequence Diagram - Application Flow (end-to-end)
![image](https://github.com/technocouple/acw-ui/assets/127013183/a0952e2e-7a6e-4bd6-a63b-f82a3d295002)

## System Architecture
![image](https://github.com/technocouple/acw-ui/assets/127013183/784b34c6-6082-462f-82d1-2e22d73ce7ff)

## Future Enhancements
1. Highlight the newly added record in "ACW Records" table after file was uploaded for processing in playground.
2. Allow switching between dark and light theme once Streamlit allows to do so programatically.
3. Multiple audio file upload in playground screen.
4. Customization and add more varieties of charts and metrics in ACW charts section.
5. Login/RBAC (Role based Access) support for the portal.
