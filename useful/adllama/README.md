<img width="806" alt="Screenshot 2023-09-18 at 11 27 06 PM" src="https://github.com/panchambanerjee/adllama/assets/17071658/f83f1c57-1d1f-41e8-84b1-cdcfcb0863cb">

# ad-llama
Create everything you need to start advertising your product ideas!!

## Example Product Ideas::

* Organic Dog Food
* Sugar-free Soda
* Coffee
* Electric Car
* Toothpaste

## Preamble
Originally built in a weekend for the Streamlit LLM Hackathon 2023 (https://streamlit.io/community/llm-hackathon-2023), the idea originated from some Langchain documentation about using models from Replicate (https://replicate.com/explore) in a SimpleSequentialChain (https://api.python.langchain.com/en/latest/chains/langchain.chains.sequential.SimpleSequentialChain.html), and a desire to move out of the OpenAI ecosystem and start using Llama 2 (https://ai.meta.com/llama/). 

* The app combines several language and text to image models and uses Streamlit for the User Interface.
* It uses a SequentialChain from LangChain to generate the product name, slogan and logo description in sequence with calls to Llama 2.
* Then this logo description is fed into 3 different text to image models to generate the logos.

## How this works

Enter an API key for Replicate (create an account, and follow the standard steps), enter a short description of a product, and sit back and let the app give you the following::
* A name for the product
* A slogan for the product
* 3 possible logos you can use for the product

## Models Used

#### Large Language Models:
* meta/llama-2-13b-chat: https://replicate.com/meta/llama-2-13b-chat

#### Text To Image Models:
  
* galleri5/icons: https://replicate.com/galleri5/icons
* mejiabrayan/logoai: https://replicate.com/mejiabrayan/logoai
* cjwbw/magifactory-t-shirt-diffusion: https://replicate.com/cjwbw/magifactory-t-shirt-diffusion

## To-Do and Notes

* Parametrize inputs for all the different Replicate models
* Llama 2 temperature, top_k, etc need to be experimented with to standardize text output format
* Understand how to use negative prompting better for the text2image models
* Try non-logo image models, Stable diffusion based
* Sometimes the logo description (which is fed into the image models) triggers an NSFW filter warning, the way to fix this is to usually just re-run, but is there a better solution?
* Some of the slogans are repetitive and a bit.. cheesy?, changing Llama 2 temperature does not seem to affect this too much.
* Sometimes the logo models don't understand that they need to generate a product logo, but generate images instead. Needs to be addressed. 
* Try llama-70b
* The code needs to be modularized
* Image resolutions need to be optimized
* Add in another step in the pipeline:: placing ad logos on products (rucksacks, bottles, coffee mugs etc.)
* Perhaps also try to generate an ad jingle
  
