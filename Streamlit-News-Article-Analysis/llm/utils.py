import tiktoken
from typing import Optional
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def extract_json_schema(llm_kwargs: dict) -> Optional[dict]:
    """Extracts the JSON schema from the LLM kwargs. To construct Validator objects."""
    # Check if the 'functions' key exists in the data
    if 'functions' in llm_kwargs:
        # Iterate through the functions
        for function in llm_kwargs['functions']:
            # Check if the 'parameters' key exists in the function
            if 'parameters' in function:
                # Check if the 'type' key is 'object' in the parameters
                if function['parameters'].get('type') == 'object':
                    # Return the properties and required fields of the object schema
                    properties = function['parameters'].get('properties', {})
                    required = function['parameters'].get('required', [])
                    return {'type': 'object', 'properties': properties, 'required': required}
    
    # If schema extraction fails, return None
    return None