from flask import Flask


from flask_sqlalchemy import SQLAlchemy

import psycopg2
conn = psycopg2.connect('postgresql://myapp:dbpass@localhost:15432/myapp')
cur = conn.cursor()
cur.execute("SELECT * FROM person;")
result = cur.fetchall()
conn.rollback()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://myapp:dbpass@localhost:15432/myapp'
db=SQLAlchemy(app)

# Create a model
class Person(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

db.create_all() #If a table with the name Person already exist, not a new table will be created automatically
p1=Person(name="Tim")
db.session.add(p1)
db.session.commit()

@app.route('/')
def index():
    msg = ''
    for el in Person.query.all():
        person_name = el.name
        msg+='hello '+person_name+ ' is nice to meet you\n'
    return msg




if __name__=='__main__':
    app.run(host='0.0.0.0',port='3000',debug=True)