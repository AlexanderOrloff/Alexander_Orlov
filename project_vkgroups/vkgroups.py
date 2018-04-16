import urllib.request
import json
import os
import math
from datetime import date
import matplotlib.pyplot as plt

token = 'eb5ca534eb5ca534eb5ca53488eb3e8942eeb5ceb5ca534b18e5d8caa9b1e92f322b97d'

def main (token):
    TextComment ={}
    AgeComment = {}
    TownComment = {}
    AgeText = {}
    TownText = {}
    offsets = [0, 100, 200]
    for off in offsets:
        line = 'https://api.vk.com/method/wall.get?owner_id=-14088108&count=100&v=5.7&offset=' + str(off)+ '&access_token=' + token
        data = requesting(line)
        for i in range(0, 100):
            text_id = data['response']['items'][i]['id']
            text = data['response']['items'][i]['text']
            LengthText = length_text(text)
            write_text(text, off,i)
            a = get_comments (text_id, token, off, i)
            TextComment = dictionarize(LengthText, TextComment, a[0] )
            for key in  a[1].keys():
                TownComment = dictionarize(key,TownComment, a[1][key] )
            for key in  a[2].keys():
                AgeComment = dictionarize(key,AgeComment, a[2][key] )
            TownText = TownAge(data, i, TownText, 'town', LengthText)
            AgeText = TownAge(data, i, AgeText, 'age', LengthText)
    graph_textcomment(TextComment)
    graph_bar(AgeComment, 'комментарии', 'возраста')
    graph_bar(TownComment, 'комментарии', 'города')
    graph_bar(AgeText, 'посте', 'возраста')
    graph_bar(TownText, 'посте', 'города')


def requesting(line):
    req = urllib.request.Request(line)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    return data

def length_text(text):
    text = text.split()
    return len(text)

def write_text(text, offset, i):
    directory = os.path.join('.', 'texts', str(offset + i))
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, 'text'+ str(offset+i) + '.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    return

def get_comments(text_id, token, off, j):
    AgeComment = {}
    TownComment = {}
    LengthComments = 0
    line = 'https://api.vk.com/method/wall.getComments?owner_id=-14088108&post_id=' + str(text_id) + '&count=100&v=5.7&access_token=' + token
    data = requesting(line)
    if data['response']['count'] < 100:
        for i in range(0,data['response']['count']):
            LengthComment = data_comments(data, off, j, i, 0)
            LengthComments += LengthComment
            TownComment = TownAge(data, i, TownComment, 'town', LengthComment)
            AgeComment = TownAge(data, i, AgeComment, 'age', LengthComment)
    else:
        for i in range(0,100):
            LengthComment = data_comments(data, off, j, i, 0)
            LengthComments += LengthComment
            TownComment = TownAge(data, i, TownComment, 'town', LengthComment)
            AgeComment = TownAge(data, i, AgeComment, 'age', LengthComment)
        offsets = []
        limit = int(math.ceil(data['response']['count'] / 100))
        for i in  range (1, limit):
            offsets.append (i*100)
        offsets.append('stop')
        for off in range(0, len(offsets) - 1 ):
            line = 'https://api.vk.com/method/wall.getComments?owner_id=-14088108&post_id=' + str(text_id) + '&offset='+ str(offsets[off]) +'&v=5.7&access_token=' + token
            data = requesting(line)
            if offsets[off+1] != 'stop':
                for i in range(0, 100):
                    LengthComment = data_comments(data, off, j, i,  offsets[off])
                    LengthComments += LengthComment
                    TownComment = TownAge(data, i, TownComment, 'town', LengthComment)
                    AgeComment = TownAge(data, i, AgeComment, 'age', LengthComment)
            else:
                for i in range(0,data['response']['count'] - offsets[off] -1):
                    LengthComment = data_comments(data, off, j, i, offsets[off])
                    LengthComments += LengthComment
                    TownComment = TownAge(data, i, TownComment, 'town', LengthComment)
                    AgeComment = TownAge(data, i, AgeComment, 'age', LengthComment)
# будем возвращать массив из трёх элементов : [средння длина коммента к посту, словарь с городами-длиной, словарь с возрастами-длиной]
    return result(LengthComments, data, TownComment,AgeComment)

def result(LengthComments, data, TownComment,AgeComment):
    a = []
    if data['response']['count'] != 0:
         a.append(LengthComments/data['response']['count'])
    else:
         a.append(0)
    a.append(TownComment)
    a.append(AgeComment)
    return a

def data_comments(data, off, j, i, offsets):
    LengthComment = length_text(data['response']['items'][i]['text'])
    write_comment(data['response']['items'][i]['text'], off, j, i, offsets)
    return LengthComment

def write_comment(text, offset, j, i, offsets):
    filepath = os.path.join("." , 'texts',  str(offset + j), str('comment') + str(i + offsets) + '.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    return

def user_town(data, i):
     id = data['response']['items'][i]['from_id']
     line = 'https://api.vk.com/method/users.get?user_ids=' + str(id)+'&fields=home_town&v=5.7&access_token=' + token
     data =requesting(line)
     if data['response'] == []:
         return 'none'
     if 'home_town' in data['response'][0]:
         return data['response'][0]['home_town']
     else:
         return 'none'


def user_age(data, i):
    id = data['response']['items'][i]['from_id']
    line = 'https://api.vk.com/method/users.get?user_ids=' + str(id) + '&fields=bdate&v=5.7&access_token=' + token
    data = requesting(line)
    if data['response'] == []:
        return 'none'
    if 'bdate' in data['response'][0]:
        if len(data['response'][0]['bdate']) > 5:
                today = date.today()
                born = data['response'][0]['bdate'].split('.')
                return today.year - int(born[2]) - ((today.month, today.day) < (int(born[1]), int(born[0])))
        else:
            return 'none'

    else:
        return 'none'

def TownAge (data, i, dict, type, CommentLength):
            if type == 'town':
                item = user_town(data, i)
            else:
                item = user_age(data, i)
            return dictionarize (item, dict, CommentLength )


def dictionarize (item, dict,CommentLength ):
            if item  not in dict:
                dict[item] = CommentLength
            else:
                dict[item] = (dict[item]+ CommentLength)/2
            return dict

def graph_textcomment(TextComment):
    X = []
    Y = []
    for key in TextComment.keys():
        X.append(key)
        Y.append(TextComment[key])
    plt.title('зависимость числа слов в комментарии от числа слов в посте')
    plt.ylabel('слов в комментарии')
    plt.xlabel('слов в посте')
    plt.scatter(X, Y, s = 10)
    plt.savefig('зависимость числа слов в комментарии от числа слов в посте' + '.pdf')
    plt.clf()
    return

def graph_bar(dict, word1, word2):
    X = []
    Y = []
    for key in dict.keys():
        X.append(key)
        Y.append(dict[key])
    plt.title('зависимость числа слов в ' + word1 +' от ' + word2)
    plt.ylabel('слов в ' + word1)
    plt.xlabel(word2[:-1])
    font = {'size': 4}
    plt.rc('font', **font)
    plt.bar(X, Y)
    plt.xticks(rotation=90)
    plt.savefig('зависимость числа слов в ' + word1 +' от ' + word2 + '.pdf')
    plt.clf()
    return


main(token)
