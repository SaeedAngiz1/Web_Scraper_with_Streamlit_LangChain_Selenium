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

def get_model(provider, base_url, api_key, model_name):
    if provider == "Ollama":
        from langchain_ollama import OllamaLLM
        kwargs = {"model": model_name}
        if base_url:
            kwargs["base_url"] = base_url
        return OllamaLLM(**kwargs)

    elif provider == "OpenAI":
        from langchain_openai import ChatOpenAI
        kwargs = {"model": model_name, "api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        return ChatOpenAI(**kwargs)

    elif provider == "Anthropic":
        from langchain_anthropic import ChatAnthropic
        kwargs = {"model_name": model_name, "api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        return ChatAnthropic(**kwargs)

    elif provider == "Google GenAI":
        from langchain_google_genai import ChatGoogleGenerativeAI
        kwargs = {"model": model_name, "google_api_key": api_key}
        return ChatGoogleGenerativeAI(**kwargs)

    else:
        raise ValueError(f"Unsupported provider: {provider}")

def parse_content(dom_chunks, parse_description, provider, base_url, api_key, model_name):
    model = get_model(provider, base_url, api_key, model_name)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parse_result = []

    inputs = [{"dom_content": chunk, "parse_description": parse_description} for chunk in dom_chunks]

    responses = chain.batch(inputs)

    for i, response in enumerate(responses, start=1):
        # Handle string response vs Message response object depending on the chat model
        if hasattr(response, "content"):
            parse_result.append(response.content)
        else:
            parse_result.append(str(response))

        print(f"parsed batch {i} of {len(dom_chunks)}")

    return "\n".join(parse_result)
