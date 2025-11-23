import streamlit as st
from scrape import scrape_website, split_dom_content,clean_body_content,extract_body_content
from parse import parse_with_ollama


st.title("AI Web Scraper")

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
                results = parse_with_ollama(dom_chunks, parse_description)
            
            if results.strip():
                st.success(" Extraction completed!")
                st.text_area("Extracted Results:", results, height=300)
            else:
                st.warning("No matching content found. Try a different description.")
        else:
            st.warning("Please enter a description of what you want to extract.")






