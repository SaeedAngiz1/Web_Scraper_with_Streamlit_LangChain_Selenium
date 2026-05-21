import time
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate

def mock_invoke(inputs):
    time.sleep(0.5)
    class Response:
        content = f"Parsed: {inputs.to_string()}"
    return Response()

def test_sequential(dom_chunks, parse_description):
    template = "Prompt: {dom_content} {parse_description}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | RunnableLambda(mock_invoke)

    start_time = time.time()
    parse_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke({"dom_content": chunk, "parse_description": parse_description})

        if hasattr(response, "content"):
            parse_result.append(response.content)
        else:
            parse_result.append(str(response))

        print(f"parsed batch {i} of {len(dom_chunks)}")

    seq_time = time.time() - start_time
    return "\n".join(parse_result), seq_time

def test_concurrent(dom_chunks, parse_description):
    template = "Prompt: {dom_content} {parse_description}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | RunnableLambda(mock_invoke)

    start_time = time.time()

    inputs = [{"dom_content": chunk, "parse_description": parse_description} for chunk in dom_chunks]

    # Using chain.batch which executes concurrently by default
    responses = chain.batch(inputs)

    parse_result = []
    for i, response in enumerate(responses, start=1):
        if hasattr(response, "content"):
            parse_result.append(response.content)
        else:
            parse_result.append(str(response))
        print(f"parsed batch {i} of {len(dom_chunks)}")

    con_time = time.time() - start_time
    return "\n".join(parse_result), con_time

chunks = ["chunk1", "chunk2", "chunk3", "chunk4", "chunk5"]
print("Running Sequential")
_, seq_time = test_sequential(chunks, "desc")
print("\nRunning Concurrent")
_, con_time = test_concurrent(chunks, "desc")

print(f"\nSequential Time: {seq_time:.2f}s")
print(f"Concurrent Time: {con_time:.2f}s")
