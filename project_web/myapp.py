from flask import Flask
from flask import render_template, redirect, url_for, request
import json

app = Flask(__name__)

def answers(ans):
    with open ('answers.txt', 'a', encoding = 'utf-8') as f:
        s =''
        for word in ans:
            answer = word.lower()
            answer = answer.replace(' ', '_')
            s = s + answer + '\t'
        s = s.strip()
        s = s + '\n'
        f.write(s)


def arr_answers():
    with open('answers.txt', 'r', encoding='utf-8') as f:
        arr = []
        answers = f.readlines()
        for line in answers:
            s = line.strip()
            data = s.split()
            arr.append(data)
    return arr


def complete_json(arr):
    with open('complete_json', 'w', encoding='utf-8')as j:
        s = json.dumps(arr)
        j.write(s)


def dicts(arr):
    colors = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    for a in arr:
        for i in range(0, 10):
            s = a[i]
            if s in colors[i]:
                colors[i][s] += 1
            else:
                colors[i][s] = 1
    with open('dict.json', 'w', encoding='utf-8') as j:
        s = json.dumps(colors)
        j.write(s)


def dict():
    with open('dict.json', 'r', encoding='utf-8')as d:
        text = d.read()
        data = json.loads(text)
        return data


def number():
    with open('answers.txt', 'r', encoding='utf-8')as f:
        n = len(f.readlines())
        return n


def search(word):
    res = ['', '', '', '', '', '', '', '', '', '']
    data = dict()
    n = number()
    for i in range(0, 10):
        s = ''
        for answer in data[i]:
            w = answer.replace('_', ' ')
            if word in w:
                k = data[i][answer] / n * 100
                if k < 20:
                    s = s + ' ' + w + ' (' + str(k) + '%);'
                else:
                    s = s + ' <b>' + w + '</b> (' + str(k) + '%);'
        res[i] = s
    return res


@app.route('/')
def index():
    if request.args:
        one = request.args['0101DF']
        two = request.args['2E9AFE']
        three = request.args['01A9DB']
        four = request.args['04B4AE']
        five = request.args['A9BCF5']
        six = request.args['2EFEF7']
        seven = request.args['58D3F7']
        eight = request.args['81F7F3']
        nine = request.args['04B486']
        ten = request.args['0B2F3A']
        ans = [one, two, three, four, five, six, seven, eight, nine, ten]
        answers(ans)
        arr = arr_answers()
        complete_json(arr)
        dicts(arr)
    return render_template('index.html')


@app.route('/stats')
def stats():
    data = dict()
    n = number()
    data2 = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    for i in range(0, 10):
        for ans in data[i]:
            k = data[i][ans] / n * 100
            if k < 20:
                data2[i][ans] = str(k) + '%'
            else:
                s = '<b>' + ans + '</b>'
                data2[i][s] = str(k) + '%'
    return render_template('stats.html', data=data2)


@app.route('/json')
def jsn():
    with open('complete_json', 'r', encoding='utf-8') as f:
        text = f.read()

    return render_template('json.html', text=text)


@app.route('/results')
def results():
    if request.args:
        word = request.args['word']
        a = search(word)
        return render_template('results.html', a=a, word=word)
    else:
        return redirect(url_for('search'))


@app.route('/search')
def searching():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)