#https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# use webserver conda virtual env where it is installed flask
import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

###############################################################################################################
def insertVaribleIntoTable(idb ,published ,author,title,first_sentence):
    try:
        sqliteConnection = sqlite3.connect('books.db')
        cur = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO books
                          (id ,published ,author,title,first_sentence) 
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (idb ,published ,author,title,first_sentence)
        cur.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cur.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

#insertVaribleIntoTable(2, 'Joe', 'joe@pynative.com', '2019-05-19', 9000)
#insertVaribleIntoTable(3, 'Ben', 'ben@pynative.com', '2019-02-23', 9500)


#codice del post method https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
@app.route('/api/v1/resources/add', methods=['POST'])
def add_into_db():
    
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory 
    cur = conn.cursor()
    #query= "INSERT INTO books (id ,published ,author,title,first_sentence) VALUES( '"+str(request.json['id'])+"', "+str(request.json['published'])+", '"+str(request.json['author'])+"', '"+str(request.json['title'])+"', '"+str(request.json['first_sentence'])+"') ;"
    query= "INSERT INTO books (id ,published ,author,title,first_sentence) VALUES( 'we', 1234, 'me', 'tit', 'yoyo') ;"
    result = cur.execute(query)
    conn.commit
    return jsonify(query)

@app.route('/api/v1/resources/readd', methods=['POST'])
def insdb():
    insertVaribleIntoTable(2, 124, 'me', 'tit', '9000')
    insertVaribleIntoTable('due', 124, 'me', 'tit', '9000')
    return jsonify('finished')

@app.route('/api/query/1', methods=['GET'])
def show():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    structure = cur.execute("SELECT sql FROM sqlite_master WHERE name = 'books';").fetchall()

    return jsonify(structure)



app.run()
