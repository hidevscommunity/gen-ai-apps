import streamlit as st
from gtts import gTTS
import os
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

st.title("VidDirector")
storyname = st.text_input("Create a video about:")
video_tone = st.selectbox("Select video tone:", ["Happy", "Sad", "Inspirational", "Playful", "Mysterious", "Energetic", "Custom"])
if video_tone == "Custom":
    custom_tone = st.text_input("Enter custom video tone:")
    video_tone = custom_tone if custom_tone else video_tone
video_type = st.selectbox("Select video type:", ["Story", "Poem", "Fairy Tale", "Documentary", "Tutorial", "Review", "Custom"])
if video_type == "Custom":
    custom_type = st.text_input("Enter custom video type:")
    video_type = custom_type if custom_type else video_type
video_style = st.selectbox("Select video style:", ["Animation", "Anime", "Natural Art", "Retro", "Digital Art", "Photographic", "Cinematic", "Sci-Fi", "Neon Punk", "Custom"])
if video_style == "Custom":
    custom_style = st.text_input("Enter custom video style:")
    video_style = custom_style if custom_style else video_style
video_aspect = st.selectbox("Select aspect ratio:(In development)", ["1:1","16:9", "9:16", "3:4", "Custom"])
if video_aspect == "Custom":
    custom_aspect = st.text_input("Enter custom aspect ratio:")
    video_aspect = custom_aspect if custom_aspect else video_aspect

# Button to generate script
if st.button("Generate Video"):
    #streamlit success
    st.success("Generating script...")
    st.write("Please note that video creation may take up to 10 minutes.")
    prompt = f"""
    Generate a fully compelling video story script for a YouTube video about "{storyname}".
    You choose the video tone: {video_tone}, style: {video_style}, and the length of the entire video (1 minute). The story must have an ending, and it must be meaningful. For each sentence in the story, provide a related visual image scene description to enhance the storytelling.

    Remember to format the output as follows:

    Image: Insert image description or scene here aspect:{video_aspect} style: {video_style}
    Narrator: Write the narration or dialogue for the sentence 

    Image: Insert image description or scene here aspect:{video_aspect}  
    Narrator: Write the narration or dialogue for the sentence 

    Image: Insert image description or scene here aspect:{video_aspect}
    Narrator: Write the narration or dialogue for the sentence 

    And so on until the end of the story.

    Return without commentary. Only the narrator should speak no other characters in the story. Give highly detailed 2 lines image prompts that relate to previous scenes. The prompts should be similar, and the images generated should be similar to each other because I am going to create a video using that."""

    clarifai_pat = st.secrets.CLARIFAI_PAT

    PAT = clarifai_pat
    USER_ID = 'openai'
    APP_ID = 'chat-completion'
    MODEL_ID = 'GPT-3_5-turbo'
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', 'Key ' + PAT),)
    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject, 
            model_id=MODEL_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]
    st.write("Scripts:\n")
    print(output.data.text.raw)
    text=output.data.text.raw
    image_prompts = []
    narrator_prompts = []

    # Split the text into paragraphs
    paragraphs = text.split('\n')

    # Iterate through paragraphs and categorize them as image or narrator prompts
    current_prompt_type = None
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph.startswith("Image:"):
            current_prompt_type = "Image Prompts"
            paragraph = paragraph[len("Image: "):]  # Remove "Image: " from the beginning
        elif paragraph.startswith("Narrator:"):
            current_prompt_type = "Narrator Prompts"
            paragraph = paragraph[len("Narrator: "):]  # Remove "Narrator: " from the beginning
        
        if current_prompt_type == "Image Prompts":
            image_prompts.append(paragraph)
        elif current_prompt_type == "Narrator Prompts":
            narrator_prompts.append(paragraph)

    # Print the separated prompts
    print("Image Prompts:")
    image_prompts = [prompt for prompt in image_prompts if prompt.strip()]
    for image_prompt in image_prompts:
        print(image_prompt)
    narrator_prompts = [prompt for prompt in narrator_prompts if prompt.strip()]
    for narrator_prompt in narrator_prompts:
        st.write(narrator_prompt)
    st.success("Scripts Generated Sucessfully")
    os.makedirs("audio", exist_ok=True)

    
    st.success("Generating audio files using Eleven Labs speech synthesis model")
   
    USER_ID = 'eleven-labs'
    APP_ID = 'audio-generation'
    MODEL_ID = 'speech-synthesis'
    if not os.path.exists("audio"):
        os.makedirs("audio")
    for idx, narrator_prompt in enumerate(narrator_prompts):
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=narrator_prompt
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
        output = post_model_outputs_response.outputs[0]

        print(f"{idx+1}Audio Generated")
        for concept in output.data.concepts:
            print("%s %.2f" % (concept.name, concept.value))

        base64_audio = output.data.audio.base64
        audio_filename = f"audio/audio_{idx}.mp3"  # Save audio in the "audio" folder with the .mp3 extension
        with open(audio_filename, 'wb') as f:
            f.write(base64_audio)

    st.success("Audio files Generated Sucessfully")

    st.success("Generating images using Stable Diffusion XL model")
    USER_ID = 'stability-ai'
    APP_ID = 'stable-diffusion-2'
    MODEL_ID = 'stable-diffusion-xl'
    if not os.path.exists("image"):
        os.makedirs("image")
    for idx, image_prompt in enumerate(image_prompts):
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=image_prompt
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
        output = post_model_outputs_response.outputs[0]
        print(f"{idx+1}image generated")
        for concept in output.data.concepts:
            print("%s %.2f" % (concept.name, concept.value))

        base64_image = output.data.image.base64
        image_filename = f"image/image_{idx}.jpg"   
        with open(image_filename, 'wb') as f:
            f.write(base64_image)
    
    st.success("Images Generated Sucessfully")
    st.success("Generating video using moviepy")
    from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
    import os

    # Define your output video filename
    output_video_filename = "output_video.mp4"

    # Get a list of image and audio files in their respective folders
    image_folder = "image"  # Replace with the path to your image folder
    audio_folder = "audio"  # Replace with the path to your audio folder

    image_filenames = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(".jpg")]
    audio_filenames = [os.path.join(audio_folder, filename) for filename in os.listdir(audio_folder) if filename.endswith(".mp3")]

    # Sort the file lists to ensure they are in the right order
    image_filenames.sort()
    audio_filenames.sort()

    # Create lists to hold image and audio clips
    image_clips = []
    audio_clips = []

    # Load image and audio clips
    for image_filename, audio_filename in zip(image_filenames, audio_filenames):
        if os.path.exists(image_filename) and os.path.exists(audio_filename):
            audio_clip = AudioFileClip(audio_filename)
            image_clip = ImageClip(image_filename, duration=audio_clip.duration)
            audio_clips.append(audio_clip)
            image_clips.append(image_clip)
        else:
            print(f"Skipping image or audio file due to missing files.")

    # Create final video clips by setting audio to images with transitions
    final_clips = []
    for idx in range(len(image_clips)):
        image_clip = image_clips[idx]
        audio_clip = audio_clips[idx]
        
        # Apply a crossfade transition to the image (you can adjust the duration)
        transition_duration = 1  # Adjust the duration of the transition in seconds
        if idx > 0:
            image_clip = image_clip.crossfadein(transition_duration)
        
        # Set audio to the image
        video_clip = image_clip.set_audio(audio_clip)
        final_clips.append(video_clip)
        #streamlit progress bar
        my_bar = st.progress(idx+1)
        my_bar.progress(idx+1)

    # Concatenate the video clips
    final_video = concatenate_videoclips(final_clips, method="compose")

    # Write the final video to the specified output file
    final_video.write_videofile(output_video_filename, codec='libx264', threads=4, audio_codec='aac', fps=24)
    st.success("Video Generated Sucessfully")
    st.video("output_video.mp4")
    st.snow()
    

    

    

            
