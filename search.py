from thefuzz import process
import json
from flask import Flask, request, escape, render_template

app = Flask(__name__)

def load_data():
    with open("badges.json") as f:
        d = json.load(f)
    names = list(d.keys())
    return d, names

def search(keyword, data, names):
    try:
        result = process.extractOne(keyword, names)
        return data[result[0]]['badge']
    except Exception as e:
        print("couldn't find match")
        print(e)
        return None
    
@app.route("/")
def home():
    if not request.args.get("q"):
        args = "python,java,php,github"
    else:
        args = request.args.get("q")
    args = args.split(",")
    data, names = load_data()
    all_badges = []
    for kw in args:
        result = search(kw, data, names)
        if result:
            all_badges.append(result)

    unescaped = ['<p align="center">']
    for badge in all_badges:
        line = f'<img src="{badge}">'
        unescaped.append(line)
    unescaped.append("</p>")
    unescaped = '\n'.join(unescaped)
    return render_template("index.html", unescaped=unescaped, q=",".join(args))

if __name__ == '__main__':
    app.run()




