import logging
import sqlite3
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from logging import StreamHandler

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection.execute('INSERT INTO db_connections DEFAULT VALUES')
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.commit()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.commit()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error(f"Article {post_id} not found")
      return render_template('404.html'), 404
    else:
      app.logger.info(f"Article {post['title']} retrieved")
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About us page accessed')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f'Article {title} created')
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Health check successful')
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    connections = connection.execute('SELECT * FROM db_connections').fetchall()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.commit()
    connection.close()
    no_of_db_connections = len(connections)
    no_of_posts = len(posts)
    response = app.response_class(
            response=json.dumps({"db_connection_count": no_of_db_connections, "post_count": no_of_posts}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Metrics request successful')
    return response

# start the application on port 3111
if __name__ == "__main__":
   handlers = [
    StreamHandler(),  # Default stream=sys.stderr
    StreamHandler(stream=sys.stdout)
    ]

   logging.basicConfig(handlers=handlers, level=logging.DEBUG)
   app.run(host='0.0.0.0', port='3111')
