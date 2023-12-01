# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, request

import langchain_processing

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "Welcome to Crosshack APIs"


@app.post("/answer")
def give_me_ans():
    if request.is_json:
        body = request.get_json()
        # res = get_data("What is the main point of the transcript?")
        res = langchain_processing.get_answer(body["query"])
        print(res)
        return res

    return {"error": "Request must be JSON"}, 415


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    data = langchain_processing.load_data([
        "https://help.autodesk.com/view/DOCS/ENU/?guid=What_Is_Desktop-Connector",
        "https://milvus.io/docs/overview.md",
        "https://wiki.autodesk.com/display/PDF/Deployment+Schedule",
        "https://wiki.autodesk.com/pages/viewpage.action?pageId=144721761"
    ])
    # print(data)

    tokens = langchain_processing.split_data(data)
    # print(tokens)

    # query = "\nWhat is the main point of the transcript?"
    # result = langchain_processing.get_chain(tokens)({"query": query})
    # print(query)
    # print(result["result"])

    langchain_processing.store_data(tokens)

    # res = get_data("What is the main point of the transcript?")
    # print(res)
