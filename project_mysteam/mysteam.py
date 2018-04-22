
from pymorphy2 import MorphAnalyzer
from flask import Flask
from flask import render_template,request
import random
morph = MorphAnalyzer()
#['NOUN', 'PREP', 'VERB', 'ADJF', 'CONJ', 'PRTS', 'PRCL', 'ADVB', 'NPRO', 'INTJ', 'GRND', 'ADJS', 'INFN', 'PRED', None, 'PRTF', 'NUMR', 'COMP']

app = Flask(__name__)

def vocabulary():
    words = []
    with open('text.txt', 'r', encoding = 'utf-8') as t:
         text = t.read()
         text = text.split()
         for item in text:
            item = item.strip('[!?.,:;()\ufeff]').lower()
            if item != '—':
                words.append(item)
    return words

def partsofspeach(vocab):
    #создать словари, в каждом из которых массив слов нужных, нужной части речи. потом будем выбирать рандомное слово
    pos = {}
    for item in vocab:
        anna = morph.parse(item)
        first = anna[0]
        if str(first.tag).split()[0] not in pos:
            pos[str(first.tag).split()[0]] = [first.word]
        else:
            pos[str(first.tag).split()[0]].append(first.word)
    return pos

def new_one(vocab, pos, sent):
    grammar = GrammarSequence(vocab, pos, sent) #массив из двух в массивов: в первом по порядку все неизменные признаки слова, во втором - изменяемые
    response = ''
    for i in range(0, len(grammar[0])):
        if grammar[0][i] in pos and grammar[1] != []:
            word = random.choice(pos[grammar[0][i]])
            ann = morph.parse(word)[0]
            if (grammar[1][i] != ' ')  and (ann.tag.POS != 'NPRO') and (ann.tag.POS != 'PREP') and (ann.tag.POS != 'CONJ'):
                if ',' in grammar[1][i]:
                    a = grammar[1][i].split(',')
                for item in a:
                        print(ann)
                        ann = ann.inflect({item})
            response = response + ' ' + ann.word
        else:
            response  = response + ' ' + sent.split()[i]
    return response




def GrammarSequence(vocab, pos, sent):
    grammarobl= []
    grammaropt = []
    sent = sent.split()
    for item in sent:
        anna = morph.parse(item)
        grammar = str(anna[0].tag)
        grammarobl.append(grammar.split()[0])
        if ' ' in grammar:
            grammaropt.append(grammar.split()[1])
        else:
            grammaropt.append(' ')
    return [grammarobl, grammaropt]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
   if request.args:
       vocab = vocabulary()
       pos = partsofspeach(vocab)
       sent = request.args['sent']
       text = new_one(vocab, pos, sent)
   return render_template('result.html', text = text)

if __name__ == '__main__':
    app.run(debug=True)


