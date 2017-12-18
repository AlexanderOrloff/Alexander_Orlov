from flask import Flask
from flask import render_template,request
import urllib.request
import re
import os
# в папке также должен лежать майстем и бутстрап, словаь был скачан заранее
#  я писал программу по тому заданию, что находится на сайте, то есть она не записывает информацию в файл, а выводит в браузере страницу, переведённую в доревалюционную орфографию

app = Flask(__name__)


def weather(): #собираем информацию о погоде и предоставляем её в удобном для нас виде
   url = "https://yandex.ru/pogoda/10463"
   page = urllib.request.urlopen(url)
   text = page.read().decode('utf-8')
   forecast = re.search('<time class="time fact__time"(.*?)<dl class="term fact__water">', text)
   regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
   regSpace = re.compile('\s{2,}', re.DOTALL)
   clean_t = regTag.sub(" ", forecast.group(0))
   clean_t = regSpace.sub(' ', clean_t)
   regYesterday = re.compile('Вчера в это время..\d..')
   forecast1 = regYesterday.sub('', clean_t)
   return forecast1

def htmler(url):
   page = urllib.request.urlopen(url)
   text = page.read().decode('utf-8')
   return text

def change_trigger(text): #в html'е заменяем все строки на доревалюционные
   d = {}
   alllines = re.findall('[А-Яа-яЁё\s.,!?:;\\-0-9]+', text )
   lines = []
   for line in alllines:
       if re.search ('[А-Яа-яЁё]',line ) != None:
           lines.append(line)
   for index, line in enumerate(lines):
       d.update(mystem(index, line))  #создаётся словарь соответствий: ключ - наша орфографию, значение - дореволюц
   for key in d:
       text = re.sub(key, d[key], text) #получаем html с новыми значениями
   word = counter(d)
   with open(r'.\templates\html.html', 'w', encoding = 'utf-8') as t:
       t.write(text)
   return word

def mystem(index, line):
    d = {}
    filepath = ".\\\\" + str(index) + '.txt'
    with open(filepath, 'w', encoding='utf-8') as f:
        s = line + '\n'
        f.write(s)
    myfilepath = ".\\\\" + str(index) + 'my.txt'
    os.system(r'.\mystem.exe' + ' ' + '-nidc --eng-gr' + ' ' + filepath + ' ' + myfilepath)
    new_line = change_engine(myfilepath)
    d[line] = new_line  # создаётся словарь соответствий: ключ - наша орфографию, значение - дореволюц
    return d

def counter(d):
   num = {}
   for  key in d.keys():
       arr = key.split()
       for item in arr:
           if item not in num.keys():
               num[item] = 1
           else:
               num[item] += 1
       number = 0
       word = ''
       for key in num.keys():
           if num[key] > number:
               number = num[key]
               word = key
   return word

def change_engine(myfilepath):
    with open(myfilepath, 'r', encoding='utf-8') as j:
        text = j.readlines()
        new_line = ''
        for line in text:  # на каждой строке по одному слову или пробел, знак препинания
            if re.search('[А-Яа-яЁё]', line) != None:
                arr = []
                m = re.search('([\w-]*?){([\w-]*?)[?=](.*?)}', line)
                arr.append(m.group(1))  # wordform
                arr.append(m.group(2))  # lemma
                arr.append(m.group(3))  # information on grammar
                new_word = dictionary(arr)
                semifinal_word = positions(new_word)
                final_word = case(arr, semifinal_word)
            elif '_' in line:
                final_word = re.sub('_', ' ', line)
                final_word = re.sub('\\\\n', '', final_word)
                final_word = re.sub('\n', '', final_word)
            else:
                final_word = line
                final_word = re.sub('\\\\n', '', final_word)
                final_word = re.sub('\n', '', final_word)
            new_line += final_word
    return new_line

def dictionary(arr):  # словарные случаи
    with open('dictionary.txt', 'r', encoding="utf-8") as d:
        dict = d.read()
    s = '\s{2,}' + arr[1] + "\s{2,}([\w']+?)[,\s]"
    m = re.search(s, dict)
    vowels = {'ѣ', 'ѳ', 'ѵ'}
    if m != None:
        if m.group(1).endswith('ъ'):
            old_word = m.group(1)[:-1]
        else:
            old_word = m.group(1)
        if len(arr[0]) - len(
                old_word) <= 0:  # иногда встречаются неточные соотвествия так в словаре "Слово" соответствует "С" (название буквы)
            # все такие вещи руками сложно удалить
            old_word = re.sub("'", "", old_word)
            for i in range(0, len(arr[1])):  # нас не волнуют окончания и буква i, так как она расчитывается позиционо
                new_word = arr[0]
                if arr[1][i] != old_word[i] and old_word[
                    i] in vowels:  # и в начальной форме может быть, а в косвенном падеже не быть
                    new_word = arr[0][:i] + old_word[i] + arr[0][i + 1:]

                    arr[0] = new_word
        else:
            new_word = arr[0]
    else:
        new_word = arr[0]
    if type(new_word) != 'NoneType':
        return new_word
    else:
        return arr[0]


def positions(word): #позиционные замены
    new_word = ''
    target = {'И', 'и', 'Й', 'й'}
    vowels = {'у', 'е', 'ы', 'а', 'о', 'э', 'я', 'и', 'ю', 'й', 'ь', 'ъ', 'У', 'Е', 'Ы', 'А', 'О', 'Э', 'Я', 'И', 'Ю' } # и все равно не может быть перед ъ и ь, а нам пригодится
    if len(word) > 1:
        for i in range(0,len(word)-1): # замена и на i перед гласными
            if word[i] in target and word[i+1] in vowels:
                new_word += 'i'
            else:
                new_word += word[i]
        new_word += word[-1]
        if new_word[-1] not in vowels and new_word.isupper() == False: # добавление ъ
            new_word += 'ъ'
        if new_word.startswith('бес'): #заменяем приставки
            base = new_word[3:]
            new_word = 'без' + base
        if new_word.startswith('черес'):
            base = new_word[5:]
            new_word = 'через' + base
        if new_word.startswith('чрес'):
            base = new_word[4:]
            new_word = 'чрес' + base
    else:
        new_word = word
    return new_word


def case(arr, word): #замена падежей
    if 'S' in arr[2] and word.endswith('е'):
        if ('dat' in arr[2] and 'sg' in arr[2]) or ('loc' in arr[2] and 'sg' in arr[2] ):
            new_word = word[:-1] + 'ѣ'
            return new_word
        else:
            return word
    else:
        return word


def verify(answer): #верифицируем ответы
    if answer == 'right':
        return 1
    else:
        return 0



@app.route('/')
def index():
   text = weather()
   return render_template('index.html', text = text)

@app.route('/request')
def  requesting():
   return render_template('request.html')


@app.route('/result')
def result():
   if request.args:
       url = request.args['url']
       word = change_trigger(htmler(url))
   return render_template('result.html', word = word)

@app.route('/resultword')
def  resultword():
   if request.args:
       word = request.args['word']
       d = mystem('index',word)
       new_word = d[word]
       return render_template('resultword.html', text = new_word)


@app.route('/test')
def  test():
    return render_template('test.html')

@app.route('/resultletter')
def resultletter():
    if request.args:
        score = 0
        answers = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7', 'answer8', 'answer9','answer10' ]
        for answer in answers:
            verified = request.args[answer]
            score += verify(verified)
    return render_template('resultletter.html', text = score)

@app.route('/html')
def html():
    return render_template('html.html')


if __name__ == '__main__':
   app.run(debug=True)