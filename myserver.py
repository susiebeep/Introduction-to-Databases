from flask import Flask, render_template
from flask import request
from db_connector.db_connector import connect_to_database, execute_query

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/album')
def album():
    return render_template('album.html')

@app.route('/track')
def track():
    return render_template('track.html')

@app.route('/band_members')
def band_members():
    return render_template('members.html')

@app.route('/shows')
def shows():
    return render_template('shows.html')

@app.route('/set_list')
def set_list():
    return render_template('set_list.html')

@app.route('/add_album', methods = ['POST', 'GET'])
def add_album():
    Album_Name = request.form['Album_Name']
    Release_Date = request.form['Release_Date']
    query = 'INSERT INTO `album` (`album name`, `release date`) VALUES (:Album_Name, :Release_Date)'
    data = (Album_Name, Release_Date)
    db_connection = connect_to_database()
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

@app.route('/track_contributors')
def track_contributors():
    return render_template('track_contributors.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3975)