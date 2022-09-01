from flask import Flask, Response,  request, render_template, json
import random, requests
import pandas as pd
import numpy as np
import mysql.connector
mydb =  mysql.connector.connect(host="localhost", password="mili@2001", user="root", database="book_records")
mycursor =mydb.cursor()
app = Flask(__name__)

@app.route('/detail',methods=['GET'])
def detail():
    new_data = random_books()
    return render_template('detail.html',y=new_data)

def random_books():
        sql = "SELECT ID, Name, Rating, Review, Tags FROM goodreads"
        mycursor.execute(sql)
        result=mycursor.fetchall()
        d=pd.DataFrame(result)
        d.columns = ['ID', 'Name', 'Rating', 'Review', 'Tags']
        dict=d.to_dict('index')
        new_data = random.choices(dict, k=5)
        return new_data

@app.route('/detail', methods=['POST'])

def search():
    text = request.form['text']
    print(text)
    sql = "SELECT ID, Name, Rating, Review, Tags FROM goodreads where Name='"+text+"' or Tags='"+text+"' or Review='"+text+"'"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    d = pd.DataFrame(result)
    d.columns = ['ID', 'Name', 'Rating', 'Review', 'Tags']
    dict = d.to_dict(orient='records')
    return render_template('detail.html', y=dict)

@app.route('/update')
def update():
    return render_template('update.html')


@app.route('/update', methods=['POST'])
def update_form():
    id = request.form["id"]
    print(id)
    name = request.form["name"]
    print(name)
    rat = request.form["rat"]
    print(rat)
    review = request.form["review"]
    print(review)
    tags = request.form["tags"]
    print(tags)
    mycursor.execute("update goodreads set Name=%s, Rating=%s, Review=%s, Tags=%s where ID=%s",(name, rat, review, tags, id))
    return Response(status=200)

if __name__=="__main__":
    app.run()
mydb.commit()