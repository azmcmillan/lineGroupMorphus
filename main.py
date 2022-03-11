
from flask import Flask

import lineGroupMorphus

app=Flask(__name__)
@app.route('/')
def index():
    return 'This is a test one'

@app.route('/')
def lineGroupMorphus():
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
