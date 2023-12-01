# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask

from dataload import load_data, split_data, get_db, get_chain

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    data = load_data([
        "https://help.autodesk.com/view/DOCS/ENU/?guid=What_Is_Desktop-Connector",
        "https://milvus.io/docs/overview.md",
        "https://wiki.autodesk.com/display/PDF/Deployment+Schedule",
        "https://wiki.autodesk.com/pages/viewpage.action?pageId=144721761"
    ])
    print(data)

    tokens = split_data(data)
    print(tokens)

    db = get_db(tokens)
    print(db)

    query = "\nWhat is the main point of the transcript?"
    result = get_chain(db)({"query": query})
    print(query)
    print(result["result"])

    query = "\nWhat is the speaker's tone throughout the transcript?"
    result = get_chain(db)({"query": query})
    print(query)
    print(result["result"])


