import whisper
from pytube import YouTube
import gradio as gr
import os
import re
import logging
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def main():
    logging.basicConfig(level=logging.INFO)
    model = whisper.load_model("base")


    def get_linkedin_post(data, api_key):

        llm = OpenAI(temperature=0,openai_api_key=api_key)

        prompt_template = """Transform the following text into an engaging LinkedIn post that will capture the attention of your 
        professional network. Craft a compelling hook to grab your audience's interest, add relevant hashtags for increased engagement, 
        and include any necessary links. Feel free to incorporate emojis and bullet points if they enhance the post's readability and 
        impact. Your goal is to make this post informative, eye-catching, and shareable within the LinkedIn community. Now, create the 
        post that will make a lasting impression.
        data: {text} """
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )
        chain = LLMChain(llm=llm, prompt=PROMPT)
        resp = chain.run(text=data)

        return resp


    def get_text(url):
        #try:
        if url != '':
            output_text_transcribe = ''

        yt = YouTube(url)
        #video_length = yt.length --- doesn't work anymore - using byte file size of the audio file instead now
        #if video_length < 5400:
        video = yt.streams.filter(only_audio=True).first()
        out_file=video.download(output_path=".")

        file_stats = os.stat(out_file)
        logging.info(f'Size of audio file in Bytes: {file_stats.st_size}')
        
        if file_stats.st_size <= 30000000:
            base, ext = os.path.splitext(out_file)
            new_file = base+'.mp3'
            os.rename(out_file, new_file)
            a = new_file
        
            result = model.transcribe(a)
            return result['text'].strip()
        else:
            logging.error('Videos for transcription on this space are limited to about 1.5 hours. Sorry about this limit but some joker thought they could stop this tool from working by transcribing many extremely long videos. Please visit https://steve.digital to contact me about this space.')
        #finally:
        #    raise gr.Error("Exception: There was a problem transcribing the audio.")

    with gr.Blocks() as demo:
        gr.Markdown("<h1><center>Youtube2Linkedin</center></h1>")
        gr.Markdown("<center>Enter the link of any YouTube video to generate a Linkedin Post</center>")
        gr.Markdown("<center>Transcription takes 5-10 seconds per minute of the video (bad audio/hard accents slow it down a bit). #patience<br />If you have time while waiting, drop a ♥️ and check out our <a href=https://hidevscommunity.wixsite.com/hidevs target=_blank>website</a> (opens in new tab).</center>")

        open_api_key = gr.Textbox(placeholder='Open Api Key', label='Your OPEN API Key')
        
        input_text_url = gr.Textbox(placeholder='Youtube video URL', label='YouTube URL')
        result_button_transcribe = gr.Button('Step 1. Transcribe')
        output_text_transcribe = gr.Textbox(placeholder='Transcript of the YouTube video.', label='Transcript')
        
        result_button_summary = gr.Button('Step 2. Linkedin Post')
        linkedin_post = gr.Textbox(placeholder='Linkedin Post from the YouTube Video.', label='Linkedin Post')
        
        result_button_transcribe.click(get_text, inputs = input_text_url, outputs = output_text_transcribe)
        result_button_summary.click(get_linkedin_post, inputs = [output_text_transcribe,open_api_key], outputs = linkedin_post)

    demo.queue(default_enabled = True).launch(debug = True)