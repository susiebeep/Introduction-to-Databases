from flask import Flask, render_template
from flask import request, redirect
from db_connector import connect_to_database, execute_query

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')


## SELECT FUNCTIONALITIES

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
    query = 'SELECT `set list`.`set list id`, `set list`.`line up id`, `shows`.`city`, `set list`.`track id`, `tracks`.`track name` FROM `set list` JOIN `shows` ON `set list`.`line up id` = `shows`.`line up id` JOIN `tracks` ON `set list`.`track id` = `tracks`.`track id`';
    result = execute_query(db_connection, query).fetchall();
    return render_template('set_list.html', rows = result)
    
@app.route('/track_contributors')
def track_contributors():
    db_connection = connect_to_database()
    query = 'SELECT `track band member`.`track band contributor id`, `track band member`.`track id`, `tracks`.`track name`, `track band member`.`band member id`, `band members`.`name` FROM `track band member` JOIN `tracks` ON `track band member`.`track id` = `tracks`.`track id` JOIN `band members` ON `track band member`.`band member id` = `band members`.`band member id`';
    result = execute_query(db_connection, query).fetchall();
    return render_template('track_contributors.html', rows = result)


## INSERT FUNCTIONALITIES

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
   
## SEARCH FUNCTION
   
@app.route("/search", methods = ['GET', 'POST'])
def search():
    db_connection = connect_to_database()
    track_id = request.form['Search']
    query = 'SELECT `tracks`.`track id`, `tracks`.`track name`, `tracks`.`track length`, `tracks`.`album id`, `band members`.`name`, `shows`.`line up id`, `shows`.`city` FROM `tracks` LEFT JOIN `set list` ON `tracks`.`track id` = `set list`.`track id` LEFT JOIN `shows` ON `set list`.`line up id` = `shows`.`line up id` LEFT JOIN `track band member` ON `tracks`.`track id` = `track band member`.`track id` LEFT JOIN `band members` ON `track band member`.`band member id` = `band members`.`band member id` WHERE `tracks`.`track id` = (%s)'
    data = (track_id,)
    result_search = execute_query(db_connection, query, data).fetchall();
    return render_template('results.html', results = result_search)    
 
## DELETE FUNCTIONALITIES
 
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
    query1 = 'DELETE FROM `shows` WHERE `set list id` = %s'
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
    
@app.route("/delete_contributor/<int:id>")
def delete_contributor(id):
    db_connection = connect_to_database()
    query1 = 'DELETE FROM `track band member` WHERE `track band contributor id` = %s'
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query2 = 'SELECT `track band member`.`track band contributor id`, `track band member`.`track id`, `tracks`.`track name`, `track band member`.`band member id`, `band members`.`name` FROM `track band member` JOIN `tracks` ON `track band member`.`track id` = `tracks`.`track id` JOIN `band members` ON `track band member`.`band member id` = `band members`.`band member id`';
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('track_contributors.html', rows = result2)      
    
@app.route("/delete_set_list/<int:id>")
def delete_set_list(id):
    db_connection = connect_to_database()
    query1 = 'DELETE FROM `set list` WHERE `set list id` = %s'
    data = (id,)
    result1 = execute_query(db_connection, query1, data)
    query2 = 'SELECT `set list`.`set list id`, `set list`.`line up id`, `shows`.`city`, `set list`.`track id`, `tracks`.`track name` FROM `set list` JOIN `shows` ON `set list`.`line up id` = `shows`.`line up id` JOIN `tracks` ON `set list`.`track id` = `tracks`.`track id`';
    result2 = execute_query(db_connection, query2).fetchall();
    return render_template('set_list.html', rows = result2)


## UPDATE FUNCTIONALITIES        

@app.route('/update_track/<int:id>', methods=['POST','GET'])
def update_tracks(id):
    db_connection = connect_to_database()
    #album_query = 'SELECT `album id` FROM `album`';
    #result_album = execute_query(db_connection, album_query).fetchall();
    
    if request.method == 'GET':
        track_query = 'SELECT * FROM `tracks` WHERE `track id` = %s' % (id)
        track_result = execute_query(db_connection, track_query).fetchone()

     
        return render_template('track_update.html', track = track_result)

    elif request.method == 'POST':
        db_connection = connect_to_database()
        track_name = request.form['track_name']
        track_length = request.form['track_length']
        album_id = request.form['album_ID']
        data = (track_name, track_length, album_id)

        query = "UPDATE `tracks` SET `track name` = %s, `track length` = %s, `album id` = %s WHERE `track id` = %s"
        result = execute_query(db_connection, query, data)

        return redirect('/tracks')


@app.route('/update_set_list/<int:id>', methods=['POST','GET'])
def update_set_list(id):
    db_connection = connect_to_database()
   
    if request.method == 'GET':
        sl_query = 'SELECT * FROM `set list` WHERE `set list id` = %s' % (id)
        sl_result = execute_query(db_connection, sl_query).fetchone()
        
        print(sl_result)
        
        return render_template('set_list_update.html', setlist = sl_result)

    elif request.method == 'POST':
        db_connection = connect_to_database()
        lineup_id = request.form['lineup_id']
        track_id = request.form['track_id']
        data = (lineup_id, track_id)

        query = "UPDATE `set list` SET `line up id` = %s, `track id` = %s WHERE `set list id` = %s"
        result = execute_query(db_connection, query, data)

        return redirect('/set_list')

@app.route('/update_show/<int:id>', methods=['POST','GET'])
def update_show(id):
    db_connection = connect_to_database()
   
    if request.method == 'GET':
        show_query = 'SELECT * FROM `shows` WHERE `line up id` = %s' % (id)
        shows_result = execute_query(db_connection, show_query).fetchone()
        
        print(shows_result)
        
        return render_template('shows_update.html', shows = shows_result)

    elif request.method == 'POST':
        db_connection = connect_to_database()
        city_name = request.form['city_name']
        data = (city_name,)

        query = "UPDATE `shows` SET `city` = %s WHERE `line up id` = %s"
        result = execute_query(db_connection, query, data)

        return redirect('/shows')    
        
        
@app.route('/update_album/<int:id>', methods=['POST','GET'])
def update_album(id):
    db_connection = connect_to_database()
    
    if request.method == 'GET':
        album_query = 'SELECT * FROM `album` WHERE `album id` = %s' % (id)
        album_result = execute_query(db_connection, album_query).fetchone()

     
        return render_template('album_update.html', album = album_result)

    elif request.method == 'POST':
        db_connection = connect_to_database()
        album_id = request.form['album_id']
        album_name = request.form['album_name']
        release_date = request.form['release_date']
        data = (album_name, release_date, album_id)

        query = "UPDATE `album` SET `album name` = %s, `release date` = %s WHERE `album id` = %s"
        result = execute_query(db_connection, query, data)

        return redirect('/album')        
    
@app.route('/update_member/<int:id>', methods=['POST','GET'])
def update_member(id):
    db_connection = connect_to_database()
    
    if request.method == 'GET':
        member_query = 'SELECT * FROM `band members` WHERE `band member id` = %s' % (id)
        member_result = execute_query(db_connection, member_query).fetchone()

        return render_template('members_update.html', member = member_result)

    elif request.method == 'POST':
        db_connection = connect_to_database()
        member_name = request.form['member_name']
        instrument = request.form['instrument']
        birthdate = request.form['birthdate']
        data = (member_name, instrument, birthdate)

        query = "UPDATE `band members` SET `name` = %s, `instrument` = %s, `birthdate` = %s WHERE `band member id` = %s"
        result = execute_query(db_connection, query, data)

        return redirect('/members')      
    
    @app.route('/update_track/<int:id>')
def update_track():
    db_connection = connect_to_database()
    query = 'SELECT `album id` FROM `album`';
    result_album = execute_query(db_connection, query).fetchall();
    return render_template('add_track.html', albums = result_album )   
    

@app.route('/update_track_new/<int:id>', methods = ['POST', 'GET'])
def update_track_new():
    db_connection = connect_to_database()
    track_name = request.form['track_name']
    track_length = request.form['track_length']
    album_id = request.form['Album_ID']
    query = "UPDATE `tracks` SET `track name` = %s, `track length` = %s, `album id` = %s WHERE `track id` = %s"
    data = (track_name, track_length, album_id)
    execute_query(db_connection, query, data)
    return render_template('update_track_new.html') 
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3975)
