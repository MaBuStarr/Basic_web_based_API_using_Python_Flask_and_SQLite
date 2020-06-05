# this code came from this tutorial: https://nordicapis.com/how-to-create-an-api-from-a-dataset-using-python-and-flask/
# These are sample browder URLS to query the database
# http://127.0.0.1:5000/api/v1/resources/books/all
# http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis
# http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1993
# http://127.0.0.1:5000/api/v1/resources/books?published=2010
import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}

    for idx, col in enumerate(cursor.description):
        print('row', row)
        print('what is this?', idx, col)
        d[col[0]] = row[idx]
        print('d[col[0]]', d[col[0]])
        print('d', d)
    return d

@app.route('/', methods=['GET'])
def home():
    return '''Distant Reading Archive: A prototype API for distant reading of science fiction novels.'''

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db') # connects to the database using the sqlite3.connect command. The variable in the () loads the .db file and the resulting data is connected to the ‘conn’ variable.
    conn.row_factory = dict_factory # The conn.row_factory command tells the connection function to use the dict_factory variable we defined, which converts the data retrieved from the database as dictionaries rather than lists
    cur = conn.cursor() # cur object is an object that moves through the database and collects all the data
    all_books = cur.execute('SELECT * FROM books;').fetchall() # the cur.execute method retrieves all pertinent data, *, from the books table in the database.

    return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(e):
    return "404. The resource could not be found.", 404 #  for when errors occur, returning 404 errors when a query isn’t included in the database.

@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter(): # lets the end-user filter by id, published, and author.
    query_parameters = request.args # defining the query parameters:
    # print('these are the request.args')
    # print(query_parameters)

    id = query_parameters.get('id') # chains the supported queries to the appropriate variable.
    print('id:', id)
    published = query_parameters.get('published') # chains the supported queries to the appropriate variable.
    print('published:', published)
    author = query_parameters.get('author') # chains the supported queries to the appropriate variable.
    print('author:', author)

    query = "SELECT * FROM books WHERE" # the function translates Python code into a format SQL can understand.
    to_filter = []
    print('to_filter before: ', to_filter)

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author): # If the user hasn’t used any of these queries, they’ll be redirected to a 404 page.
        return page_not_found(404)

    print('to_filter after: ', to_filter)
    print("query before:", query)
    query = query[:-4] + ';'
    print("query after:", query)

    # Then the results are paired with appropriate variables, same as before.
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results) # Finally, those results are returned in JSON format

if __name__ == "__main__":
    app.run()