import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from flask.wrappers import Response
from werkzeug.exceptions import abort
import logging
import sys

dbconn_COUNTER = 0 

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global dbconn_COUNTER
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    dbconn_COUNTER += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                    (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    global posts
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define status check the endpoint should return the following message
# if HTTP 200 status code then OK healthy
@app.route('/healthz')
def healthz():
    if post is None:
        response = app.response_class(
        response=json.dumps({"result":"ERROR - Unhealthy"}),
            status=404,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
        response=json.dumps({"result":"OK - healthy"}), 
            status=200, 
            mimetype='application/json'
        )

    ## log line
    app.logger.info('Healthz Status request successful')
    return response

# Define Metrics checking on db connection
@app.route('/metrics')
def metrics():
# Get db connection status
    response = app.response_class(
        response=json.dumps({"status":"success","code":0,"data":{"db_connection_count":dbconn_COUNTER,"post_count":len(posts)}}),
            status=200,
            mimetype='application/json'
        )

    ## log line
    app.logger.info('Metrics request successful')
    return response

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      ## log line
      app.logger.info('Article with id = "{0}" does not exist.'.format(post_id))  
      return render_template('404.html'), 404
    else:
      ## log line
      app.logger.info('Article with id = "{0}" retrieved!'.format(post['title']))  
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
     ## log line
     app.logger.info('-Article "2020 CNCF Annual Report" retrieved!')
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
            ## log line
            app.logger.info('-New post title %s created!',title)
            return redirect(url_for('index'))

    return render_template('create.html')

    


# start the application on port 3111
if __name__ == "__main__":
   ## stream logs to app.log file
   logger = logging.getLogger("__name__")
   logger.setLevel(logging.DEBUG)
   # set logger to handle STDOUT and STDERR 
   h1 = logging.StreamHandler(sys.stdout)
   h1.setLevel(logging.DEBUG)
   h2 = logging.StreamHandler(sys.stderr)
   h2.setLevel(logging.ERROR)
   handlers = [h1, h2]
  
   # logging.basicConfig(filename='app.log',level=logging.DEBUG, format=f'%(levelname)s %(name)s [%(asctime)s] : %(message)s')
   logging.basicConfig(format=f'%(levelname)s %(name)s [%(asctime)s] : %(message)s',level=logging.DEBUG, handlers=handlers)
   logging.debug('This will get logged')
    
   app.run(host='0.0.0.0', port='3111')
