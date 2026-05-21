from dataclasses import dataclass
from langchain_core.prompts import ChatPromptTemplate

@dataclass
class LLMConfig:
    provider: str
    model_name: str
    base_url: str = ""
    api_key: str = ""


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

def get_model(config: LLMConfig):
    if config.provider == "Ollama":
        from langchain_ollama import OllamaLLM
        kwargs = {"model": config.model_name}
        if config.base_url:
            kwargs["base_url"] = config.base_url
        return OllamaLLM(**kwargs)

    elif config.provider == "OpenAI":
        from langchain_openai import ChatOpenAI
        kwargs = {"model": config.model_name, "api_key": config.api_key}
        if config.base_url:
            kwargs["base_url"] = config.base_url
        return ChatOpenAI(**kwargs)

    elif config.provider == "Anthropic":
        from langchain_anthropic import ChatAnthropic
        kwargs = {"model_name": config.model_name, "api_key": config.api_key}
        if config.base_url:
            kwargs["base_url"] = config.base_url
        return ChatAnthropic(**kwargs)

    elif config.provider == "Google GenAI":
        from langchain_google_genai import ChatGoogleGenerativeAI
        kwargs = {"model": config.model_name, "google_api_key": config.api_key}
        return ChatGoogleGenerativeAI(**kwargs)

    else:
        raise ValueError(f"Unsupported provider: {config.provider}")

def parse_content(dom_chunks, parse_description, config: LLMConfig):
    model = get_model(config)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parse_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})

        # Handle string response vs Message response object depending on the chat model
        if hasattr(response, "content"):
            parse_result.append(response.content)
        else:
            parse_result.append(str(response))

        print(f"parsed batch {i} of {len(dom_chunks)}")

    return "\n".join(parse_result)
