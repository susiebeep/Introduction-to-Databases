from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/album')
def album():
    return render_template('add_album.html')

@app.route('/track')
def track():
    return render_template('add_track.html')

@app.route('/band_members')
def band_members():
    return render_template('band_members.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3975)