import streamlit as st
import re
import pyperclip  # Import pyperclip to copy text to clipboard

# Function to remove spaces, tabs, and newlines from JS code
def compress_js(js_code):
    # Remove all spaces, tabs, and newlines using regex
    minified_code = re.sub(r'\s+', '', js_code)
    return minified_code

# Streamlit app UI
st.title('JS Compressor')

st.markdown("""
This app removes spaces, tabs, and newlines from JavaScript code to create a compressed version.
Just paste your JavaScript code in the input box below and hit the button to Compress it!
""")

# User input (paste JS code)
js_input = st.text_area("Paste your JavaScript code here", height=300)

# Define a container to hold the state
if 'minified_code' not in st.session_state:
    st.session_state.minified_code = None

# Initialize show_copy_button if it doesn't exist
if 'show_copy_button' not in st.session_state:
    st.session_state.show_copy_button = False

# Button to trigger the minification
if st.button('Compress Code'):
    if js_input.strip():  # Ensure input is not empty
        # Minify the code
        st.session_state.minified_code = compress_js(js_input)
        
        # Show the minified code
        st.subheader("Compressed JavaScript Code")
        st.code(st.session_state.minified_code, language="javascript")
        
        # Show "Copy Code" button only after compression
        st.session_state.show_copy_button = True
    else:
        st.error("Please enter some JavaScript code to compress.")

# Only show "Copy Code" button after minified code exists
if st.session_state.show_copy_button:
    if st.button('Copy Code'):
        # Use pyperclip to copy the minified code to clipboard
        pyperclip.copy(st.session_state.minified_code)
        st.success("Code copied to clipboard!")  # Display success message
        # Reset the state after copying (optional)
        st.session_state.show_copy_button = False
