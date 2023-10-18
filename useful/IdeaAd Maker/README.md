# IdeaAd Maker - Unleash Your Product Ideas!

## Check out these example product ideas:

- Organic Dog Food
- Sugar-free Soda
- Coffee
- Electric Car
- Toothpaste

This app brings together multiple language and text-to-image models while providing a user-friendly interface via Streamlit. It uses a SequentialChain from LangChain to generate product names, slogans, and logo descriptions sequentially with calls to Llama 2. These logo descriptions are then processed by three different text-to-image models to create unique logos.

## How it Operates:

Simply enter your Replicate API key (create an account and follow the standard steps), provide a brief product description, and watch as the app generates:

- A catchy product name
- A compelling product slogan
- Three potential logos for your product

## Models Utilized:

#### Large Language Models:
- [meta/llama-2-13b-chat](https://replicate.com/meta/llama-2-13b-chat)

#### Text To Image Models:

- [galleri5/icons](https://replicate.com/galleri5/icons)
- [mejiabrayan/logoai](https://replicate.com/mejiabrayan/logoai)
- [cjwbw/magifactory-t-shirt-diffusion](https://replicate.com/cjwbw/magifactory-t-shirt-diffusion)
