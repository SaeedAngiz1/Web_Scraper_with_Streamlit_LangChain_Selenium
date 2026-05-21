import streamlit as st
from scrape import scrape_website, split_dom_content,clean_body_content,extract_body_content
from parse import parse_content, LLMConfig


st.title("AI Web Scraper")

# Sidebar for LLM Provider settings
st.sidebar.title("LLM Settings")
provider = st.sidebar.selectbox("Select Provider", ["Ollama", "OpenAI", "Anthropic", "Google GenAI"])

base_url = ""
api_key = ""

if provider == "Ollama":
    model_name = st.sidebar.text_input("Model Name", value="llama3.2")
    base_url = st.sidebar.text_input("Base URL (optional, e.g., http://localhost:11434)", value="")
else:
    model_name = st.sidebar.text_input("Model Name", value="")
    api_key = st.sidebar.text_input("API Key", type="password")
    base_url = st.sidebar.text_input("Base URL / Provider URL (optional)", value="")


url = st.text_input("Enter the URL of the website to scrape")

if st.button("Scrape Site"):
    if not url.strip():
        st.error(" Please enter a valid URL.")
    else:
        st.write("Scraping the website... please wait.")

        try:
            result = scrape_website(url)
            st.success("Scraping completed!")

            # Extract & clean body content
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)

            # Store in session state for parsing
            st.session_state.dom_content = cleaned_content

            with st.expander("View Raw HTML"):
                st.text_area("HTML Output:", result, height=200, disabled=True)

            with st.expander("View Cleaned Content"):
                st.text_area("DOM Content", cleaned_content, height=300, disabled=True)

        except Exception as e:
            st.error(f" Error: {e}")



if "dom_content" in st.session_state:
    st.divider()
    st.subheader(" AI Content Parser")
    parse_description = st.text_area(
        "Enter what you want to extract (e.g., 'all product prices', 'email addresses', 'headings', 'links')",
        height=100,
        placeholder="Example: Extract all product names and prices"
    )

    if st.button(" Parse Content"):
        if parse_description:
            with st.spinner("AI is analyzing and extracting content... This may take a moment."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                try:
                    config = LLMConfig(provider=provider, model_name=model_name, base_url=base_url, api_key=api_key)
                    results = parse_content(dom_chunks, parse_description, config)
                except Exception as e:
                    results = ""
                    st.error(f"Error parsing content: {e}")

            if results and results.strip():
                st.success(" Extraction completed!")
                st.text_area("Extracted Results:", results, height=300)
            else:
                st.warning("No matching content found. Try a different description.")
        else:
            st.warning("Please enter a description of what you want to extract.")
