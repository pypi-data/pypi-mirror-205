import json


from langpack import tester, tools


def _test_001_vectordbqa(app):
    q = "What did the president say about Ketanji Brown Jackson"
    print("Question: ---------------------------------------------------")
    print(q)
    print("processing ...")
    result = app({"query": q})
    print("Answer: ---------------------------------------------------")
    print(result)


def _test_002_summarize_doc(app):
    import urllib.request

    url = "https://raw.githubusercontent.com/hwchase17/langchain/master/docs/modules/state_of_the_union.txt"
    with urllib.request.urlopen(url) as response:
        state_of_the_union = response.read().decode("utf-8")

    print("Input: ---------------------------------------------------")
    print(state_of_the_union[:1000])
    if len(state_of_the_union) > 1000:
        print("(ONLY show the first 1000 characters of the article)")
    print("processing ...")
    result = app.run(state_of_the_union)
    print("Summary: ---------------------------------------------------")
    print(result)


def _test_003_qa_doc(app):
    import urllib.request

    url = "https://raw.githubusercontent.com/hwchase17/langchain/master/docs/modules/state_of_the_union.txt"
    with urllib.request.urlopen(url) as response:
        state_of_the_union = response.read().decode("utf-8")

    q = "what did the president say about justice breyer?"
    print("Input: ---------------------------------------------------")
    print(state_of_the_union[:1000])
    if len(state_of_the_union) > 1000:
        print("(ONLY show the first 1000 characters of the article)")
    print("Question: ---------------------------------------------------")
    print(q)

    print("processing ...")
    result = app.run(
        input_document=state_of_the_union,
        question=q,
    )

    print("Answer: ---------------------------------------------------")
    print(result)


def _test_004_transformation_chain(app):
    import urllib.request

    url = "https://raw.githubusercontent.com/hwchase17/langchain/master/docs/modules/state_of_the_union.txt"
    with urllib.request.urlopen(url) as response:
        state_of_the_union = response.read().decode("utf-8")

    print("Input: ---------------------------------------------------")
    print(state_of_the_union[:1000])
    if len(state_of_the_union) > 1000:
        print("(ONLY show the first 1000 characters of the article)")

    print("processing ...")
    result = app.run(state_of_the_union)

    print("Summary: ---------------------------------------------------")
    print(result)


def _test_005_chat_index(app):
    chat_history = []
    query = "What did the president say about Ketanji Brown Jackson"
    result = app({"question": query, "chat_history": chat_history})
    print("First round --------------------------")
    print("Question: " + query)
    print("Answer: " + result["answer"])
    chat_history = [(query, result["answer"])]
    query = "Did he mention who she suceeded"
    result = app({"question": query, "chat_history": chat_history})
    print("Second round --------------------------")
    print("Question: " + query)
    print("Answer: " + result["answer"])


def _test_006_hypothetical_document_embedding(app):
    q = "Where is the Taj Mahal?"
    result = app.embed_query(q)

    print("Question: " + q)
    print("Embeddings: ")
    print(result)


def _test_007_api_chain(app):
    q = "What is the weather like right now in Rome, Italy in degrees Celsius? Do not use hourly info."
    result = app.run(q)
    print(result)


def _test_008_getting_started_agent(app):
    q = "Who is Bill Gate's girlfriend? What is her current age raised to the 0.43 power?"
    result = app(q)
    print("result: --------------------------------------------")
    print(result)
    print(type(result))
    print("----------------------------------------------------")


def _test_009_apify_agent(app):
    q = "What is ChatGPT?"
    print(app.vectorstore.as_retriever().get_relevant_documents(q))


def _test_010_custom_agent(app):
    q = "Which team did Golden State Warriors played against last againt?"
    result = app(q)
    print("result: --------------------------------------------")
    print(result)
    print(type(result))
    print("----------------------------------------------------")


def _test_011_custom_llm_agent(app):
    q = "Which team did Golden State Warriors played against last againt?"
    result = app(q)
    print("result: --------------------------------------------")
    print(result)
    print(type(result))
    print("----------------------------------------------------")


def _test_012_conversation_agent(app):
    q = "hi, i am bob"
    print(f"question: {q}")
    result = app(q)
    print(result)
    print("-----------------------------------")
    q = "what's my name"
    print(f"question: {q}")
    app(q)
    result = app(q)
    print(result)
    print("-----------------------------------")


def _test_013_react_docstore_agent(app):
    q = "Author David Chanoff has collaborated with a U.S. Navy admiral who served as the ambassador to the United Kingdom under which President?"
    result = app(q)
    print("-----------------------------------")
    print(result)
    print(type(result))
    print("-----------------------------------")


def _test_014_conversational_agent(app):
    q = "hi, i am bob"
    result = app(q)
    print("-----------------------------------")
    print(result)
    print("-----------------------------------")


def _test_015_babyagi_chain(app):
    q = "Write a weather report for SF today"
    result = app({"objective": q})
    print("-----------------------------------")
    print(result)
    print("-----------------------------------")


def _test_016_babyagi_agent(app):
    q = "Write a weather report for SF today"
    result = app({"objective": q})
    print("-----------------------------------")
    print(result)
    print("-----------------------------------")


def _test_000_babyagi_agent_unformatted(app):
    q = "Write a weather report for SF today"
    app({"objective": q})


type_to_test_dict = {
    "000_babyagi_agent_unformatted": _test_000_babyagi_agent_unformatted,
    "001_vectordbqa": _test_001_vectordbqa,
    "002_summarize_doc": _test_002_summarize_doc,
    "003_qa_doc": _test_003_qa_doc,
    "004_transformation_chain": _test_004_transformation_chain,
    "005_chat_index": _test_005_chat_index,
    "006_hypothetical_document_embedding": _test_006_hypothetical_document_embedding,
    "007_api_chain": _test_007_api_chain,
    "008_getting_started_agent": _test_008_getting_started_agent,
    "009_apify_agent": _test_009_apify_agent,
    "010_custom_agent": _test_010_custom_agent,
    "011_custom_llm_agent": _test_011_custom_llm_agent,
    "012_conversation_agent": _test_012_conversation_agent,
    "013_react_docstore_agent": _test_013_react_docstore_agent,
    "014_conversational_agent": _test_014_conversational_agent,
    "015_babyagi_chain": _test_015_babyagi_chain,
    "016_babyagi_agent": _test_016_babyagi_agent,
}


def test(app, type):
    flag = False

    for key in type_to_test_dict:
        if key in type:
            tester = type_to_test_dict[key]
            tester(app)
            flag = True
            break

    if not flag:
        raise ValueError(f"{type} is not supported.")


def test_package():
    app_path = "app.json"
    with open(app_path, "r") as f:
        config = json.load(f)
    app = tools.unpack(app_path)
    tester.test(app, config["source_name"])
