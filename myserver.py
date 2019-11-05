from flask import Flask, render_template
from flask import request
from db_connector import connect_to_database, execute_query

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/album')
def album():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `album`';
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('album.html', rows = result)

@app.route('/track')
def track():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `tracks`';
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('track.html', rows = result)

@app.route('/band_members')
def band_members():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `band members`';
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('members.html', rows = result)

@app.route('/shows')
def shows():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `shows`';
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('shows.html', rows = result)

@app.route('/set_list')
def set_list():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `set list`';
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('set_list.html', rows = result)
    
@app.route('/track_contributors')
def track_contributors():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `track contributor`';
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('track_contributors.html', rows = result)
    

@app.route('/add_album', methods = ['POST', 'GET'])
def add_album():
    db_connection = connect_to_database()
    album_name = request.form['Album Name']
    release_date = request.form['Release Date']
    query = 'INSERT INTO `album` (`album name`, `release date`) VALUES (%s, %D)'
    data = (album_name, release_date)
    execute_query(db_connection, query, data)
    return("Album added!");
    #return render_template('add_album.html')

@app.route('/add_track')
def add_track():
    return render_template('add_track.html')

@app.route('/add_band_members')
def add_band_members():
    return render_template('add_members.html')

@app.route('/add_shows')
def add_shows():
    return render_template('add_shows.html')

@app.route('/add_set_list')
def add_set_list():
    return render_template('add_set_list.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3975)