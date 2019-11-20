from flask import Flask, render_template
from flask import request, redirect
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
    return render_template('album.html', rows = result)

@app.route('/track')
def track():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `tracks`';
    result = execute_query(db_connection, query).fetchall();
    return render_template('track.html', rows = result)

@app.route('/band_members')
def band_members():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `band members`';
    result = execute_query(db_connection, query).fetchall();
    return render_template('members.html', rows = result)

@app.route('/shows')
def shows():
    db_connection = connect_to_database()
    query = 'SELECT * FROM `shows`';
    result = execute_query(db_connection, query).fetchall();
    return render_template('shows.html', rows = result)

@app.route('/set_list')
def set_list():
    db_connection = connect_to_database()
    query = 'SELECT `set list`.`line up id`, `shows`.`city`, `set list`.`track id`, `tracks`.`track name` FROM `set list` JOIN `shows` ON `set list`.`line up id` = `shows`.`line up id` JOIN `tracks` ON `set list`.`track id` = `tracks`.`track id`';
    result = execute_query(db_connection, query).fetchall();
    return render_template('set_list.html', rows = result)
    
@app.route('/track_contributors')
def track_contributors():
    db_connection = connect_to_database()
    query = 'SELECT `track band member`.`track id`, `tracks`.`track name`, `track band member`.`band member id`, `band members`.`name` FROM `track band member` JOIN `tracks` ON `track band member`.`track id` = `tracks`.`track id` JOIN `band members` ON `track band member`.`band member id` = `band members`.`band member id`';
    result = execute_query(db_connection, query).fetchall();
    return render_template('track_contributors.html', rows = result)

@app.route('/add_album')
def add_album():
    return render_template('add_album.html')

@app.route('/add_album_new', methods = ['POST'])
def add_album_new():
    album_name = request.form['Album_Name']
    release_date = request.form['Release_Date']
    query = 'INSERT INTO `album` (`album name`, `release date`) VALUES (%s, %s)'
    data = (album_name, release_date)
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)
    return render_template('add_album_new.html')


@app.route('/add_track')
def add_track():
    db_connection = connect_to_database()
    query = 'SELECT `album id` FROM `album`';
    result_album = execute_query(db_connection, query).fetchall();
    return render_template('add_track.html', albums = result_album )   
    

@app.route('/add_track_new', methods = ['POST', 'GET'])
def add_track_new():
    db_connection = connect_to_database()
    track_name = request.form['track_name']
    track_length = request.form['track_length']
    album_id = request.form['Album_ID']
    query = 'INSERT INTO `tracks` (`track name`, `track length`, `album id`) VALUES (%s, %s, %s)';
    data = (track_name, track_length, album_id)
    execute_query(db_connection, query, data)
    return render_template('add_track_new.html') 

@app.route('/add_band_members')
def add_band_members():
    return render_template('add_members.html')
    
@app.route('/add_members_new', methods = ['POST', 'GET'])
def add_members_new():
    member_name = request.form['Member_Name']
    instrument = request.form['Instrument']
    birthdate = request.form['Birthdate']
    query = 'INSERT INTO `band members` (`name`, `instrument`,`birthdate`) VALUES (%s, %s, %s)'
    data = (member_name, instrument, birthdate)
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)
    return render_template('add_members_new.html')    

@app.route('/add_shows')
def add_shows():
    return render_template('add_shows.html')   
    
    
@app.route('/add_shows_new', methods = ['POST', 'GET'])
def add_shows_new():
    db_connection = connect_to_database()
    city = request.form['city']
    query = 'INSERT INTO `shows` (`city`) VALUES (%s)';
    data = (city,)
    execute_query(db_connection, query, data)
    return render_template('add_shows_new.html')    

@app.route('/add_set_list')
def add_set_list():
    db_connection = connect_to_database()
    query1 = 'SELECT `line up id` FROM `shows`';
    query1a = 'SELECT `city` FROM `shows`';
    result_lineup = execute_query(db_connection, query1).fetchall();
    result_city = execute_query(db_connection, query1a).fetchall();
    query2 = 'SELECT `track id` FROM `tracks`';
    query2a = 'SELECT `track name` FROM `tracks`';
    result_tracks = execute_query(db_connection, query2).fetchall();
    result_track_name = execute_query(db_connection, query2a).fetchall();
    return render_template('add_set_list.html', lineup = result_lineup, city = result_city, track = result_tracks, track_name = result_track_name)

@app.route('/add_set_list_new', methods = ['POST', 'GET'])
def add_set_list_new():
    db_connection = connect_to_database()
    lineup_id = request.form['lineup_id']
    track_id = request.form['track_id']
    query = 'INSERT INTO `set list` (`line up id`, `track id`) VALUES (%s, %s)';
    data = (lineup_id, track_id)
    execute_query(db_connection, query, data)
    return render_template('add_set_list_new.html')    

@app.route('/add_track_contributors')
def add_track_contributors():
    db_connection = connect_to_database()
    query1 = 'SELECT `band member id` FROM `band members`';
    query1a = 'SELECT `name` FROM `band members`';
    query2 = 'SELECT `track id` FROM `tracks`';
    query2a = 'SELECT `track name` FROM `tracks`';
    result_bm = execute_query(db_connection, query1).fetchall();
    result_bm_names = execute_query(db_connection, query1a).fetchall();
    result_tracks = execute_query(db_connection, query2).fetchall();
    result_track_name = execute_query(db_connection, query2a).fetchall();
    return render_template('add_track_contributors.html', members = result_bm, members_name = result_bm_names, tracks = result_tracks, track_name = result_track_name )   

@app.route('/add_track_contributors_new', methods = ['POST', 'GET'])
def add_track_contributors_new():
    db_connection = connect_to_database()
    track_id = request.form['track_id']
    band_member_id = request.form['Band_Member_ID']
    query = 'INSERT INTO `track band member` (`track id`, `band member id`) VALUES (%s, %s)';
    data = (track_id, band_member_id)
    execute_query(db_connection, query, data)
    return render_template('add_track_contributors_new.html')    
    
@app.route("/search", methods = ['GET', 'POST'])
def search():
    db_connection = connect_to_database()
    track_id = request.form['Search']
    query = 'SELECT `tracks`.`track id`, `tracks`.`track name`, `tracks`.`track length`, `tracks`.`album id`, `band members`.`name`, `shows`.`line up id`, `shows`.`city` FROM `tracks` LEFT JOIN `set list` ON `tracks`.`track id` = `set list`.`track id` LEFT JOIN `shows` ON `set list`.`line up id` = `shows`.`line up id` LEFT JOIN `track band member` ON `tracks`.`track id` = `track band member`.`track id` LEFT JOIN `band members` ON `track band member`.`band member id` = `band members`.`band member id` WHERE `tracks`.`track id` = (%s)'
    data = (track_id,)
    result_search = execute_query(db_connection, query, data).fetchall();
    return render_template('results.html', results = result_search)    
    
@app.route("/delete_album/<int:id>")
def delete_album(id):
    db_connection = connect_to_database()
    query1 = 'DELETE FROM `album` WHERE `album id` = %s'
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query2 = 'SELECT * FROM `album`';
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('album.html', rows = result2)

@app.route("/delete_member/<int:id>")
def delete_member(id):
    db_connection = connect_to_database()
    query1 = 'DELETE FROM `band members` WHERE `band member id` = %s'
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query2 = 'SELECT * FROM `band members`';
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('members.html', rows = result2)
    
@app.route("/delete_show/<int:id>")
def delete_show(id):
    db_connection = connect_to_database()
    query1 = 'DELETE FROM `shows` WHERE `line up id` = %s'
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query2 = 'SELECT * FROM `shows`';
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('shows.html', rows = result2)    
    
@app.route("/delete_track/<int:id>")
def delete_track(id):
    db_connection = connect_to_database()
    query1 = 'DELETE FROM `tracks` WHERE `track id` = %s'
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query2 = 'SELECT * FROM `tracks`';
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('track.html', rows = result2)

@webapp.route('/update_tracks/<int:id>', methods=['POST','GET'])
def update_tracks(id):
    db_connection = connect_to_database()
    if request.method == 'GET':
        track_query = 'SELECT * FROM `tracks` WHERE `track_id` = %s' % (id)
        track_result = execute_query(db_connection, track_query).fetchone()

        if track_result == None:
            return "No such track found!"

        return render_template('track_update.html')

    elif request.method == 'POST':
        print("Update Track!");
        db_connection = connect_to_database()
        track_name = request.form['track_name']
        track_length = request.form['track_length']
        album_id = request.form['Album_ID']
        data = (track_name, track_length, album_id)

        print(request.form);

        query = "UPDATE `tracks` SET `track_name` = %s, `track_length` = %s, `album_id` = %s WHERE `track_id` = %s"
        data = (track_name, track_length, album_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated");

        return redirect('/tracks')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3975)
