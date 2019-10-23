#import mysql.connector
#mydb = mysql.connector.connect(
	#host='classmysql.engr.oregonstate.edu',
	#user='cs340_hibberts',
	#passwd='****',
	#database='cs340_hibberts')

#mycursor = mydb.cursor()

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3975)
