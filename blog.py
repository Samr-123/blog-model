# Importing necessary libraries

from flask import Flask, redirect, render_template, Response, request, url_for
import pandas as pd
from flask import Flask, render_template, request,jsonify
import numpy as np
import mysql.connector
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to set a secret key for flashing messages

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='blogs',
        user='root',
        password='root'
    )
    return connection

@app.route('/', methods=['GET', 'POST'])
def index():
    #main landing page would be Index page
    return render_template('Index.html')

@app.route('/login', methods=['POST'])
def login():
    #getting username and password which user entered
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            #creating db connection and matching credentials with authorized user saved in login table
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "SELECT password FROM login WHERE username=%s"
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            connection.close()

            if row:
                stored_password = row[0]
                if stored_password == password:
                    #if credentials are correct redirect to home page else show same page with error message
                    return render_template('home.html')
                else:
                    return render_template('Index.html',output='Incorrect password')
                    
            else:
                return render_template('Index.html',output='Username not found')
                

        except : # type: ignore
            return render_template('Index.html',output='Could not connect to database')

    return render_template('Index.html')

@app.route('/home')
def home():
    #returning home page
    return render_template('home.html')

@app.route('/posts')
def list_posts():
    #if user selects view posts, then get all saved posts from database and view them
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM posts"
    cursor.execute(query)
    posts = cursor.fetchall()
    connection.close()
    return render_template('list_posts.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    #if user selects create new post, redirect to new_post page where user could create posts

    return render_template('new_post.html')

@app.route('/post/addnewpost', methods=['GET', 'POST'])
def addnewpost():
    #getting entered data from user and saving in database 
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        publication_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO posts (title, content, author, publication_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, content, author, publication_date))
        connection.commit()
        connection.close()
       # return None
        return redirect(url_for('list_posts'))
        #return render_template('list_posts.html')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    #get post which user edited and update in database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']

        query = "UPDATE posts SET title=%s, content=%s, author=%s WHERE id=%s"
        cursor.execute(query, (title, content, author, id))
        connection.commit()
        connection.close()

        return redirect(url_for('list_posts'))

    query = "SELECT * FROM posts WHERE id=%s"
    cursor.execute(query, (id,))
    post = cursor.fetchone()
    connection.close()

    return render_template('edit_post.html', post=post)

@app.route('/post/delete/<int:id>', methods=['POST'])
def delete_post(id):
    #delete the post which user selected
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM posts WHERE id=%s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()

    return redirect(url_for('list_posts'))

@app.route('/post/like/<int:id>', methods=['POST'])
def like_post(id):
    #update likes on each posts
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE posts SET likes = likes + 1 WHERE id=%s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()

    return redirect(url_for('list_posts'))

if __name__ == '__main__':
    app.run(port=5001)

