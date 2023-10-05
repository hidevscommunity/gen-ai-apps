# Importing the 'pipeline' function from the 'transformers' library
from transformers import pipeline

# Define a function called 'image2text' that takes an image URL as input
def image2text(url):
    """
    Convert an image to text using the Salesforce blip-image-captioning-base model.
    
    Parameters:
    url (str): The URL of the image to be converted to text.
    
    Returns:
    str: The generated text from the image.
    """
    
    # Initialize the image-to-text pipeline using Salesforce's model
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    
    # Generate text from the image
    # The pipeline returns a list of dictionaries, we extract the 'generated_text' from the first dictionary
    text = image_to_text(url)[0]["generated_text"]
    
    # Return the generated text
    return text
