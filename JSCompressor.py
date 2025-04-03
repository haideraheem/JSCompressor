import streamlit as st
import re
from jsbeautifier import beautify

# Function to compress JavaScript code
def compress_js(js_code):
    def preserve_strings(m):
        return m.group(0)

    string_pattern = r'(["\'`])(?:\\.|(?!\1).)*\1'
    js_code = re.sub(string_pattern, preserve_strings, js_code)

    url_pattern = r'https?://[^\s]+|(?<=\s)//[^\s]+'
    urls = re.findall(url_pattern, js_code)
    url_placeholders = {url: f"__URL_{i}__" for i, url in enumerate(urls)}

    for url, placeholder in url_placeholders.items():
        js_code = js_code.replace(url, placeholder)

    js_code = re.sub(r'(?<!:)//.*', '', js_code)
    js_code = re.sub(r'/\*[\s\S]*?\*/', '', js_code)

    for url, placeholder in url_placeholders.items():
        js_code = js_code.replace(placeholder, url)

    js_code = re.sub(r'\s*([{};,:=()<>+\-*/&|!])\s*', r'\1', js_code)
    js_code = re.sub(r'\s*\?\s*', '?', js_code)

    reserved_words = r'\b(await|break|case|catch|class|const|continue|debugger|default|' \
                     r'delete|do|else|enum|export|extends|false|finally|for|function|' \
                     r'if|import|in|instanceof|new|null|return|super|switch|this|throw|' \
                     r'true|try|typeof|var|void|while|with|yield|arguments|eval|' \
                     r'implements|interface|package|private|protected|public|static|let)\b'
    js_code = re.sub(rf'{reserved_words}\s+', r'\1 ', js_code)

    return js_code

# Function to beautify JavaScript code
def beautify_js(js_code):
    return beautify(js_code)

# Streamlit interface
st.title('JavaScript Code Processor')

# Tabs for Compress and Beautify
tabs = st.tabs(["Compress", "Beautify"])

with tabs[0]:
    st.markdown("""
    This app compresses JavaScript code by removing unnecessary spaces, tabs, newlines, and comments, while preserving strings and template literals.
    Paste your code below and click "Compress Code" to compress it.
    """)
    js_input = st.text_area("Paste your JavaScript code here", height=300, key="compress_input")

    if 'minified_code' not in st.session_state:
        st.session_state.minified_code = None

    if st.button('Compress Code', key="compress_button"):
        if js_input.strip():
            st.session_state.minified_code = compress_js(js_input)
            st.subheader("Compressed JavaScript Code")
            st.code(st.session_state.minified_code, language="javascript")
            st.success("Compression successful!")
        else:
            st.error("Please enter some JavaScript code to compress.")

    if st.session_state.minified_code:
        st.download_button("Download Compressed JS", st.session_state.minified_code, "compressed.js", "text/javascript", key="download_compressed")

with tabs[1]:
    st.markdown("""
    This app beautifies JavaScript code by adding appropriate indentation and formatting.
    Paste your code below and click "Beautify Code" to beautify it.
    """)
    js_input_beautify = st.text_area("Paste your JavaScript code here", height=300, key="beautify_input")

    if 'beautified_code' not in st.session_state:
        st.session_state.beautified_code = None

    if st.button('Beautify Code', key="beautify_button"):
        if js_input_beautify.strip():
            st.session_state.beautified_code = beautify_js(js_input_beautify)
            st.subheader("Beautified JavaScript Code")
            st.code(st.session_state.beautified_code, language="javascript")
            st.success("Beautification successful!")
        else:
            st.error("Please enter some JavaScript code to beautify.")

    if st.session_state.beautified_code:
        st.download_button("Download Beautified JS", st.session_state.beautified_code, "beautified.js", "text/javascript", key="download_beautified")
