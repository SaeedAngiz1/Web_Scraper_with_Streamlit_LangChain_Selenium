from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are an expert web scraping assistant. Extract specific information from the following web page content based on the user's request.\n\n"
    "WEB PAGE CONTENT:\n{dom_content}\n\n"
    "USER REQUEST: {parse_description}\n\n"
    "INSTRUCTIONS:\n"
    "1. Analyze the web page content carefully.\n"
    "2. Extract ONLY the information that matches the user's request: '{parse_description}'\n"
    "3. If extracting multiple items (like prices, names, etc.), list them clearly, one per line or in a structured format.\n"
    "4. If the information is in a table or list format, preserve that structure.\n"
    "5. If no matching information is found, return 'No matching information found.'\n"
    "6. Do NOT include explanations, comments, or meta-text. Only return the extracted data.\n"
    "7. Be thorough - extract ALL instances that match the request.\n\n"
    "EXTRACTED INFORMATION:"
)

model = OllamaLLM(model="llama3.2")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parse_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})
        parse_result.append(response)
        print(f"parsed batch {i} of {len(dom_chunks)}")

    return "\n".join(parse_result)
 