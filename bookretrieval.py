import json
import os
from flask import Flask, render_template, session, redirect, url_for, request # tools that will make it easier to build on things
import numpy as np
import pandas as pd
import sqlite3


app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'


conn = sqlite3.connect('books.sqlite')
query = "SELECT * FROM Books;"

df_books = pd.read_sql_query(query,conn)


import pandas as pd
import datetime
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import string
import numpy as np
import operator
import math
from num2words import num2words

nltk.download('punkt')
nltk.download('stopwords')
df_books['PublishedDate']= df_books['PublishedDate'].astype(str).str[0:4].apply(lambda x:datetime.datetime.strptime(x,"%Y").year)

def processed(description):
    stop_words = set(stopwords.words('english'))

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(description)

    filtered = []

    for w in word_tokens:
        if w.isnumeric():
            filtered.append(num2words(w))
            pass
        elif w not in stop_words and w not in string.punctuation and w.isalpha(): #remove stop words, punctuation, apostraphes
            filtered.append(w.lower())

    return filtered


desc_list = []
for description in df_books['Description']:
    desc_list.append(processed(description))

df_books['Processed_Text'] = desc_list

title_list = []
for description in df_books['Title']:
    title_list.append(processed(description))

df_books['Processed_Title'] = title_list

book_list = df_books.to_dict(orient='records')
book_list

id_book = {}
inverted = {}
idf = {}

book_num = len(book_list)
for book in book_list:
    key = book['ISBN']

    id_book[key] = book
    term_list = book['Processed_Text'] + book['Processed_Title']

    for t in term_list:
        if t in inverted:
            if key not in inverted[t]:
                inverted[t][key] = 1
            else:
                inverted[t][key] += 1
        else:
            inverted[t] = {key: 1}

for t in inverted:
    idf[t] = math.log10(book_num / len(inverted[t]))

def search(query, inverted, id_book):
    term_list = []
    query = query.split()
    for word in query:
        term_list.append(word)

    tf_idf = {}
    for term in term_list:
        if term in inverted:
            for book_id, frequency in inverted[term].items():
                if book_id in tf_idf:
                    tf_idf[book_id] += (1 + math.log10(frequency)) * idf[term]
                else:
                    tf_idf[book_id] = (1 + math.log10(frequency)) * idf[term]

        sorted_doc = sorted(tf_idf.items(), key=operator.itemgetter(1), reverse=True)
    results = []
    for book_id, score in sorted_doc:
      temp = id_book[book_id]
      temp["ti_idf"] = score
      results.append(temp)
    # results = [id_book[book_id] for book_id, score in sorted_doc]
    return results

#results = search('beautiful', inverted, id_book)


@app.route('/book')
def box():
    return render_template('search_box.html')


@app.route('/book', methods=['GET','POST'])
def index():
    text = request.form['text']
    results = search(text, inverted, id_book)
    return render_template('simple.html',all_books=results)

app.run()
