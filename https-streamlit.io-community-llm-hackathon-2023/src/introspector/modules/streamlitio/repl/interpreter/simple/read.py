import streamlit as st

# Define the s and y combinators
def s(f, x, y):
    return f(x, y)

def y(f):
    st.write(f"y({f})", f)
    if callable(f):
        return f(lambda x: y(f)(x))
    else:
        st.write(f"y({f}) not callable", f)
        return f

# Define the emojis and their meanings
emojis = {
    "➡️": s,
    "🔄": y,
    "🧱": None,
    "📄": "file",
    "🔤": "str",
    "🧾": "dict",
    "🧮": "int",
    "🔢": "list",
    "🔠": "word",
    # Add more emojis and meanings as needed
}

# Define the interpreter function
def interpret(expression):
    # Check if the expression is a list
    if isinstance(expression, list):
        # Check if the expression is empty
        if not expression:
            # Return an empty list
            return []
        # Check if the first element is an emoji
        elif isinstance(expression[0] ,list):
            st.write("expr:", expression[0])
            expression = expression[0]
            if expression[0] in emojis:
                # Get the meaning of the emoji
                meaning = emojis[expression[0]]
                # Check if the meaning is a function
                if callable(meaning):
                    # Apply the function to the rest of the expression
                    exp = expression[1:]
                    v= interpret(exp)
                    st.write("Interpreted exp:", exp)
                    st.write("Interpreted val:", v)
                    #st.write("Interpreted val2:", list(v))
                    return meaning(v)
                else:
                    return None
            else:
                return None

        elif expression[0] in emojis:
            # Get the meaning of the emoji
            meaning = emojis[expression[0]]
            # Check if the meaning is a function
            if callable(meaning):
                # Apply the function to the rest of the expression
                exp = expression[1:]
                v= interpret(exp)
                st.write("Interpreted exp:", exp)
                st.write("Interpreted val:", v)
                #st.write("Interpreted val2:", list(v))
                return meaning(v)
            # Check if the meaning is None
            elif meaning is None:
                # Return None
                return None
            # Otherwise, return the meaning as a string
            else:
                return str(meaning)
        # Otherwise, return the expression as a string
        else:
            return str(expression)
    # Otherwise, return the expression as it is
    else:
        return expression

# Streamlit app
st.title("Emoji Combinator Interpreter")

# Text input for the user to enter an expression


# Interpret and display the result when the user clicks a button
if st.button("Interpret"):
    result = interpret(eval(expression))
    st.write("Interpreted Result:", result)
