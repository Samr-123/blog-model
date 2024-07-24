# Import necessary libraries
import base64
import datetime
from io import BytesIO
from flask import Flask, redirect, render_template, Response, request, url_for
import plotly
from welly import Well
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import segfast
import pandas as pd
import dlisio
import xarray as xr
import json
import os
import threading
from plotly import express as px
from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import math
import chart_studio.config as plotly_config
import numpy as np
import segyio
import subprocess
import pypyodbc
import time
import matplotlib
#import subprocess
import json
from flask import Flask, render_template, request,jsonify
from segysak.segy import segy_loader
import segyio
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import plotly.express as px
import mysql.connector
import io
import base64
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
    return render_template('Corr.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            query = "SELECT password FROM login WHERE username=%s"
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            connection.close()

            if row:
                stored_password = row[0]
                if stored_password == password:
                    return render_template('home.html')
                else:
                    return render_template('Corr.html',output='Incorrect password')
                    print('Incorrect password')
            else:
                return render_template('Corr.html',output='Username not found')
                print('Username not found')

        except : # type: ignore
            return render_template('Corr.html',output='Could not connect to database')

    return render_template('Corr.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/posts')
def list_posts():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM posts"
    cursor.execute(query)
    posts = cursor.fetchall()
    connection.close()
    return render_template('list_posts.html', posts=posts)

@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    # if request.method == 'POST':
    #     title = request.form['title']
    #     content = request.form['content']
    #     author = request.form['author']
    #     publication_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #     connection = get_db_connection()
    #     cursor = connection.cursor()
    #     query = "INSERT INTO posts (title, content, author, publication_date) VALUES (%s, %s, %s, %s)"
    #     cursor.execute(query, (title, content, author, publication_date))
    #     connection.commit()
    #     connection.close()

        # return redirect(url_for('list_posts'))

    return render_template('new_post.html')

@app.route('/post/addnewpost', methods=['GET', 'POST'])
def addnewpost():
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
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "DELETE FROM posts WHERE id=%s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()

    return redirect(url_for('list_posts'))

@app.route('/post/like/<int:id>', methods=['POST'])
def like_post(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "UPDATE posts SET likes = likes + 1 WHERE id=%s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()

    return redirect(url_for('list_posts'))

if __name__ == '__main__':
    app.run(port=5001)

