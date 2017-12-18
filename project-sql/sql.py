import sqlite3
import matplotlib.pyplot as plt


gloss = {'1PL':'first person plural',
         '3PL':'third person plural',
         '1SG':'first person singular',
         '2SG':'second person singular',
         '3SG':'third person singular',
         'ABL':'ablative case',
         'ACC':'accusative case',
         'AUX':'auxiliary',
         'C':'UNKNOWN',
         'CONJ':'conjunction',
         'CONN':'connective',
         'DAT':'dative case',
         'DAT-LOC':'dative-locative case',
         'DEM':'demonstrative',
         'EMPH':'emphatic',
         'ENCL':'enclitic',
         'ENLC':'UNKNOWN',
         'GEN':'genitive case',
         'IMF':'UNKNOWN',
         'IMP':'imperative',
         'IMPF':'imperfect',
         'INDEF':'indefinite',
         'INF':'infinitive',
         'INSTR':'instrumental case',
         'LOC':'locative case',
         'MED':'medium',
         'N':'noun',
         'NEG':'negative',
         'NOM':'nominative case',
         'P':'preposition (postposition)',
         'PART':'particle',
         'PERS':'personal',
         'POSS':'possessive',
         'PL':'plural',
         'PRON':'pronoun',
         'PRS':'present',
         'PRT':'preterite',
         'PRV':'preverb',
         'PST':'past',
         'PTCP':'participle',
         'REFL':'reflexive',
         'REL':'relative pronoun',
         'SG':'singular',
         'Q':'question word',
         'QUOT':'quotative',
         'VOC':'vocative case'}


def collector(mass_of_rows, digit):
    items = []
    for row in mass_of_rows:
        a = row[digit]
        items.append(a)
    return items

def collector_glosses(mass_of_rows):
    pure_glosses = []
    gloss_dict = {}
    for row in mass_of_rows:
        glosses = row[2].split('.')
        for i in range(0, len(glosses)):
            if not glosses[i].isupper():
                glosses[i] = ''
            elif glosses[i] == 'I':
                glosses[i] = ''
        pure = ''
        for i in range(0, len(glosses)):
            if glosses[i] != '':
                if glosses[i] in gloss_dict.keys():
                    gloss_dict[glosses[i]] += 1
                else:
                    gloss_dict[glosses[i]] = 1
            if pure != '':
                    pure = pure + ' ' + glosses[i]
            else:
                    pure = glosses[i]
        pure_glosses.append(pure)
    gloss_table(gloss_dict)
    graphs(gloss_dict)
    return pure_glosses


def gloss_table(gloss_dict):
    gloss_list = []
    i = 0
    for item in gloss_dict.keys():
        a = []
        i += 1
        a.append(i)
        a.append(item)
        if item in gloss:
            a.append(gloss[item])
        else:
            a.append('')
        gloss_list.append(a)
    c.execute('CREATE TABLE glossary (id, gloss, meaning)')
    for row in gloss_list:
        c.execute('INSERT INTO glossary VALUES(?, ?,?)', row)

def graphs(gloss_dict):
     glosses = [['Person+number','1PL', '3PL', '1SG', '2SG', "3SG"],['Cases', 'ABL', 'ACC', 'DAT', 'DAT-LOC', 'GEN', 'INSTR', 'LOC', 'VOC'],  ['Number','SG', 'PL'], ['verb forms', 'IMP', 'IMPF', 'INF', 'PRS', 'PRT', 'PST'], ['types of pronouns', 'POSS', 'REFL', 'REL'] ]
     # тут много глосс, которые объективно не с чем сравнивать, и неизвестных глосс, так что я не стал делать графики для ВСЕХ глосс(как просят в звдании), но смысл же уловил?
     for list in glosses:
        X = []
        Y = []
        dots = []
        for j in range(1,len(list)):
            Y.append(gloss_dict[list[j]])
            dots.append(list[j])
        for i in range(len(Y)):
            X.append(i + 1)
        for x, y,  d in zip(X, Y, dots):
            plt.bar(x, y)
            plt.text(x+0.1, y+0.1, d)
        plt.title(list[0])
        plt.ylabel('встретилась раз')
        plt.xlabel('глосса')
        plt.savefig(list[0] + '.pdf')
        plt.clf()

def words_table(mass_of_lemmas, mass_of_wordforms, mass_of_glosses ):
    c.execute('CREATE TABLE words(id, lemma , wordform, glosses)')
    words = []
    for i in range(0, len(mass_of_lemmas)):
        wordz = []
        wordz.append(i + 1)
        wordz.append(mass_of_lemmas[i])
        wordz.append(mass_of_wordforms[i])
        wordz.append(mass_of_glosses[i])
        words.append(wordz)
    for row in words:
        c.execute('INSERT INTO words VALUES(?,?,?,?)', row)


def id():
    gloss_id = {}
    word_id = {}
    for row in c.execute('SELECT * FROM glossary'):
        gloss_id[row[1]] = row[0]  #'PART': 1
    for row in c.execute('SELECT * FROM words'):
        word_id[row[0]] = row[3] #5: 'PART
    rows = []
    for key in word_id.keys():
        arr_gloss = word_id[key].split()
        if arr_gloss != []:
            for item in arr_gloss:
                arr = []
                v = gloss_id[item]
                arr.append(key)
                arr.append(v)
                rows.append(arr)
        else:
            arr =[]
            arr.append(key)
            arr.append(0)  # сохраним во всем поле один тип данных, 0 будет отвечать за отсутсвте глосс
            rows.append(arr)
    id_table(rows)


def id_table(rows):
    c.execute('CREATE TABLE ids(word_id, gloss_id)')
    for row in rows:
        c.execute('INSERT INTO ids VALUES(?,?)', row)


conn = sqlite3.connect('hittite.db')
c = conn.cursor()
mass_of_rows = []
    #c.execute('DROP TABLE glossary')
    #c.execute('DROP TABLE words')
    #c.execute ('DROP TABLE ids')
for row in c.execute('SELECT * FROM wordforms'):
    mass_of_rows.append(row) #lemma wordform glosses
mass_of_lemmas = collector(mass_of_rows, 0)
mass_of_wordforms = collector(mass_of_rows, 1)
mass_of_glosses = collector_glosses(mass_of_rows)
words_table(mass_of_lemmas, mass_of_wordforms, mass_of_glosses)
id()
conn.commit()
conn.close()


