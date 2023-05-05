from flask import render_template
from flask import Flask, render_template, request
import random
#import pandas as pd
#import matplotlib.pyplot as plt

import mysql.connector
from mysql.connector import connect, cursor


db_connection = connect(user="root", db="quiz_questions", password="11@Woofy")
cursor = db_connection.cursor()
maxQ = 10
maxQ = int(maxQ)
selectString = f"""SELECT * from questions order by rand() limit {maxQ};"""
cursor.execute(selectString)
questions = cursor.fetchall()


from app import app


@app.route('/')
@app.route('/home', methods=["POST", "GET"])

def home():
    return render_template('home.html')

@app.route('/')
@app.route('/quiz', methods=["POST", "GET"])

def quiz():
    return render_template('quiz_q.html', questions=questions, q = 0)

@app.route('/')
@app.route('/submit_user_challenge', methods=["POST", "GET"])

def submit_user_challenge():
    authorL = ['This poem was written by a human: ','This poem was written by a computer: ']
    if request.method == "POST":
        response = request.form["response"]
    author = random.randint(0,1)
    insertString = f"""INSERT INTO questions (Q_TEXT, Q_ART) VALUES ('{authorL[author]}', '{response}')"""
    #print(insertString)
    cursor.execute(insertString)
    db_connection.commit()

    return render_template('user_challenge.html')

@app.route('/')
@app.route('/submit_quiz/<q>', methods=["POST", "GET"])

def submit_quiz(q):
    q = int(q)

    if request.method == 'POST':
        quiz_answer = request.form["q"]


    if quiz_answer == "SA":
        insertAnswers = f"""INSERT INTO answers (Q_ID, A_SA, A_A, A_MA, A_MD, A_D, A_SD) VALUES ({questions[q][0]},1,0,0,0,0,0)"""
    elif quiz_answer == "A":
        insertAnswers = f"""INSERT INTO answers (Q_ID, A_SA, A_A, A_MA, A_MD, A_D, A_SD) VALUES ({questions[q][0]},0,1,0,0,0,0)"""
    elif quiz_answer == "MA":
        insertAnswers = f"""INSERT INTO answers (Q_ID, A_SA, A_A, A_MA, A_MD, A_D, A_SD) VALUES ({questions[q][0]},0,0,1,0,0,0)"""
    elif quiz_answer == "MD":
        insertAnswers = f"""INSERT INTO answers (Q_ID, A_SA, A_A, A_MA, A_MD, A_D, A_SD) VALUES ({questions[q][0]},0,0,0,1,0,0)"""
    elif quiz_answer == "D":
        insertAnswers = f"""INSERT INTO answers (Q_ID, A_SA, A_A, A_MA, A_MD, A_D, A_SD) VALUES ({questions[q][0]},0,0,0,0,1,0)"""
    elif quiz_answer == "SD":
        insertAnswers = f"""INSERT INTO answers (Q_ID, A_SA, A_A, A_MA, A_MD, A_D, A_SD) VALUES ({questions[q][0]},0,0,0,0,0,1)"""


    cursor.execute(insertAnswers)
    db_connection.commit()


    if request.method == 'POST':
        if request.form.get("back") == "V1":
            q = q - 1
        elif request.form.get("next") == "V2":
            q = q + 1



    #db_connection.commit()
    if q == maxQ:
        return render_template('quiz_finished.html')

    return render_template('quiz_q.html', q=q, questions=questions)

@app.route('/')
@app.route('/art_examples')

def art_examples():
    return render_template('art_examples.html', title='Art Examples')

@app.route('/')
@app.route('/user_challenge', methods=["POST", "GET"])

def user_challenge():
    return render_template('user_challenge.html', title='User Challenge')

@app.route('/')
@app.route('/paintings')

def paintings():
    paintings = [
        {
            'title': 'Painting 1',
            'img': 'Picture1.png'
        }
    ]
    return render_template('paintings.html', title='Painting Examples', posts=paintings)


@app.route('/')
@app.route('/poems')

def poems():
    poems = [
        {
            'name': 'Duck',
            'body': 'Windy afternoon; <br>A common, springy duck eats; <br>before the lion'
        },
        {
            'name': 'The Light of a Candle',
            'body': 'The light of a candle; \nis transferred to another candle; \nspring twilight.'
        }
    ]
    return render_template('poems.html', title='Poem Examples',  posts=poems)

@app.route('/')
@app.route('/stats')

def stats():
    '''
    for question in questions:
        cursor.execute(selectString)
        y = cursor.fetchall()

        x = f''Select A_SA = Sum(A_SA) Group By Q_TEXT''
            # the line of code above needs triple quotes

        # histogram of total_bills
        plt.hist(data['total_bill'])

        plt.title("Histogram")

        # Adding the legends
        plt.show()
    '''
    return render_template('stats.html', title='Stats')

@app.route('/')
@app.route('/faq')

def faq():
    return render_template('faq.html')