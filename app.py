""" Useful cmd
Description                         | Cmd
to login as the right user for psql | PGUSER=myapp PGPASSWORD=dbpass psql -h localhost myapp


"""

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://myapp:dbpass@localhost:15432/myapp'
db=SQLAlchemy(app)

# import psycopg2
# conn = psycopg2.connect('postgresql://myapp:dbpass@localhost:15432/myapp')
# cur = conn.cursor()
# cur.execute("Alter TABLE todo ALTER COLUMN done SET default false")
# result = cur.fetchall()
# conn.rollback()


# Create a model
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    done = db.Column(db.Boolean,default=False)

db.create_all() #If a table with the name Person already exist, not a new table will be created automatically
task1=Todo(name="Clean my work desk")
db.session.add(task1)
db.session.commit()

@app.route('/')
def index():
    '#1.Step:Get all object from the database'
    data={}
    for el in Todo.query.all():
        data[el.id]={"description":el.name,"done":el.done}
    return render_template('index.html',)

if __name__=='__main__':
    app.run(host='0.0.0.0',port='3000',debug=True)