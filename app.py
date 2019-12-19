""" Useful cmd
Description                         | Cmd
to login as the right user for psql | PGUSER=test PGPASSWORD=test psql -h localhost todoapp
Give all right to role              | grant all privilages on database todoapp to test

PGUSER=test PGPASSWORD=test psql -h localhost todoapp
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://myapp:dbpass@localhost:15432/myapp'
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://test:test@localhost:15432/todoapp'
db=SQLAlchemy(app)
migrate=Migrate(app,db)

# import psycopg2
# conn = psycopg2.connect('postgresql://myapp:dbpass@localhost:15432/myapp')
# cur = conn.cursor()
# cur.execute("Alter TABLE todo ALTER COLUMN done SET default false")
# result = cur.fetchall()
# conn.rollback()


# Create a model
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),)
    done = db.Column(db.Boolean,default=False)
    def __repre__(self):
        return f'<Todo {self.id} {self.name}>'

db.create_all() #If a table with the name Person already exist, not a new table will be created automatically
# task1=Todo(name='Clean my desk')
# task2=Todo(name='Buy Xmas presents')
# db.session.add_all([task1,task2])

db.session.commit()

@app.route('/')
def index():
    '#1.Step:Get all object from the database'
    data={}
    response_data=[]
    for el in Todo.query.all():
        print(el.id)
        data[el.id]={"description": el.name, "done": el.done}
        response_data.append(data[el.id])
    print(response_data)
    return render_template('index.html',data=response_data)

@app.route('/todo/create',methods=['Post'])
def create_item():
    description = request.form.get("description", None)
    try:
        new_task=Todo(name=description)
        db.session.add(new_task)
        db.session.commit()
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    print(description)
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(host='0.0.0.0',port='3000',debug=True)