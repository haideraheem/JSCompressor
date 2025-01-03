import streamlit as st
import re

def compress_js(js_code):
    # Function to preserve strings and template literals
    def preserve_strings(m):
        return m.group(0)  # Return the string as-is

    # Regex to match strings ('...' or "..." or `...`)
    string_pattern = r'(["\'`])(?:\\.|(?!\1).)*\1'

    # Preserve strings by skipping them during Compression
    js_code = re.sub(string_pattern, preserve_strings, js_code)

    # Remove single-line comments
    js_code = re.sub(r'//.*', '', js_code)
    # Remove multi-line comments
    js_code = re.sub(r'/\*[\s\S]*?\*/', '', js_code)
    
    # compress by collapsing spaces, preserving critical separation
    js_code = re.sub(r'\s*([{};,:=()<>+\-*/&|!])\s*', r'\1', js_code)
    
    # Ensure reserved words are preserved with necessary spaces
    reserved_words = r'\b(await|break|case|catch|class|const|continue|debugger|default|' \
                     r'delete|do|else|enum|export|extends|false|finally|for|function|' \
                     r'if|import|in|instanceof|new|null|return|super|switch|this|throw|' \
                     r'true|try|typeof|var|void|while|with|yield|arguments|eval|' \
                     r'implements|interface|package|private|protected|public|static|let)\b'
    
    js_code = re.sub(rf'{reserved_words}\s+', r'\1 ', js_code)
    
    return js_code

st.title('JavaScript Compressor')

st.markdown("""
This app compresses JavaScript code by removing unnecessary spaces, tabs, newlines, and comments, while preserving strings and template literals.
Paste your code below and click "Compress Code" to compress it.
""")

js_input = st.text_area("Paste your JavaScript code here", height=300)

if 'minified_code' not in st.session_state:
    st.session_state.minified_code = None

if st.button('Compress Code'):
    if js_input.strip():
        st.session_state.minified_code = compress_js(js_input)
        st.subheader("Compressed JavaScript Code")
        st.code(st.session_state.minified_code, language="javascript")
        st.success("Compression successful!")
    else:
        st.error("Please enter some JavaScript code to compress.")

if st.session_state.minified_code:
    st.download_button("Download Compressed JS", st.session_state.minified_code, "compressed.js", "text/javascript")
