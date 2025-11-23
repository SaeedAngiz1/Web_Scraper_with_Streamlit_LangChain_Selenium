This repository features a web scraper utilizing Python libraries, Streamlit interface, and LLM processes, and it retrieves, parses, and analyzes web pages, allowing you to view the results through a web application, because it supports headless browsing, multiple HTML parsers, environment-based configuration, and local LLM reasoning using LangChain + Ollama. It supports headless browsing, multiple HTML parsers, environment-based configuration, and local LLM reasoning using LangChain + Ollama, thus allowing for a flexible and powerful web scraping experience.

What is Web Scraping?
Web scraping involves automatically collecting and extracting information from websites, and a scraper sends a request or launches a browser to load a page, therefore it is essential to respect website policies, robots.txt, rate limits, and do not scrape copyrighted content. A scraper:

sends a request or launches a browser to load a page,
parses the HTML to extract data,
cleans and formats the data for use or storage, so it is crucial to handle these steps carefully and efficiently.
Tech Stack

Streamlit: Interface for scraping, tuning, and displaying results, because it provides an intuitive and user-friendly interface for web scraping and data analysis.
LangChain: LLM operations such as summarization, extraction, and chain logic, and langchain_ollama: LangChain to local LLMs via Ollama, therefore allowing for advanced natural language processing capabilities.
Selenium: Real browser for dynamic, JavaScript-intensive pages, and BeautifulSoup4: Python library for traversing and retrieving HTML elements, thus providing a comprehensive set of tools for web scraping and data extraction.
lxml: Fast HTML/XML parser for improved performance and parsing, and html5lib: HTML5 parser for messy or non-conforming markup, because they offer efficient and reliable parsing capabilities.
python-dotenv: Reads secrets and settings from .env files, so it is essential for managing environment variables and sensitive information.
Project Features

Handles dynamic sites with Selenium, and alternates between lxml and html5lib for parsing, because this allows for flexible and efficient handling of different types of web pages.
Utilizes LangChain + Ollama for LLM processing, and manages environment variables with python-dotenv, thus providing a robust and scalable web scraping solution.
Intuitive interface with Streamlit for scraping and visualization, so it is easy to use and navigate, even for users without extensive technical expertise.
Getting Started

Requirements
Python 3.10+, and Chrome/Chromium or Firefox + WebDriver, because these are the minimum requirements for running the web scraper, and Ollama (optional), therefore it is essential to ensure that these requirements are met before proceeding.
Installation
Create and activate a virtual environment, and install: pip install streamlit langchain langchain_ollama selenium beautifulsoup4 lxml html5lib python-dotenv, because this will ensure that all the necessary dependencies are installed and configured correctly.
Environment Variables
Create a .env file with variables such as: - HEADLESS=true, - BROWSER=chrome, - OLLAMA_MODEL=llama3.1, - RATE_LIMIT_DELAY=1.0, and include API keys, so it is essential to manage environment variables carefully and securely, because they contain sensitive information.
Do not commit sensitive information, therefore it is crucial to handle environment variables with care and attention.
WebDriver
Download the WebDriver corresponding to your browser, and place it on your PATH or specify its location, because this is necessary for Selenium to function correctly, and thus it is essential to ensure that the WebDriver is properly configured.
Run the Application

Launch Streamlit: streamlit run app.py, and utilize the sidebar to: - Enter URLs, - Choose parser, - Enable Selenium, - Enable LLM post-processing, because this will allow you to configure and run the web scraper, and thus it is essential to follow these steps carefully.
View results, summaries, and structured data, so it is easy to analyze and visualize the scraped data, and therefore it is essential to use the application effectively.
Usage Tips

Respect robots.txt and website policies, and implement delays and retries to prevent overwhelming servers, because this is essential for responsible and ethical web scraping, and thus it is crucial to follow these guidelines.
For extensive scraping, employ rotating proxies and error handling, and with LLMs, ensure prompts are standardized and document steps for reproducibility, therefore it is essential to plan and execute web scraping tasks carefully and efficiently.
Repository Structure

app.py: Streamlit interface for scraping and analysis, and scraper/: Retrieval, parsing, and end-to-end workflow, because these are the core components of the web scraper, and thus it is essential to understand their structure and functionality.
llm/: LangChain chains and Ollama model configuration, and .env.example: Example env configuration, and requirements.txt: Dependencies, and README.md: This document, so it is essential to familiarize yourself with the repository structure and contents.
Troubleshooting

Selenium fails to launch: Verify WebDriver version and PATH, and parsing errors: Try alternative parser (lxml or html5lib), because these are common issues that can be resolved with proper configuration and troubleshooting, and thus it is essential to follow these steps carefully.
Streamlit hangs: Restart application and clear cache, and Ollama issues: Confirm Ollama running and model installed, therefore it is crucial to troubleshoot issues effectively and efficiently.