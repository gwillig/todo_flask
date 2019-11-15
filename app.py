""" Useful cmd
Description                         | Cmd
to login as the right user for psql | PGUSER=test PGPASSWORD=test psql -h localhost test
Give all right to role              | GRANT ALL PRIVILEGES ON database todoapp to test;
adds temporary git\bit to path      | "c:\Program Files\Git\bin\sh.exe" --login

PGUSER=test PGPASSWORD=test psql -h localhost todoapp
"""

from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

from flask_migrate import Migrate
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://test:test@localhost:15432/test'
db=SQLAlchemy(app)
migrate=Migrate(app,db)

# import psycopg2
# conn = psycopg2.connect('postgresql://test:test@localhost:15432/test')
# cur = conn.cursor()
# cur.execute("Alter TABLE todo ALTER COLUMN done SET default false")
# result = cur.fetchall()
# conn.rollback()


# Create a model
class TodoList(db.Model):
    __tablename__='todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    todo = db.relationship('Todo', backref="list", lazy=True)


class Todo(db.Model):
    __tablename__='todo'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    done = db.Column(db.Boolean,default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True, default=1)
    def __repre__(self):
        return f'<Todo {self.id} {self.name}>'


db.create_all() #If a table with the name Person already exist, not a new table will be created automatically
##Check if initial
if len(TodoList.query.all())==0:
    list1=TodoList(name='unassigned')
    db.session.add(list1)

    task1=Todo(name='Clean my desk',list_id=1)
    task2=Todo(name='Buy Xmas presents',list_id=1)
    db.session.add_all([task1,task2])
    db.session.commit()

@app.route('/list/<list_id>')
def get_list(list_id):
    print(list_id)
    return render_template('index.html',
                           selected_list=TodoList.query.filter_by(id=list_id).first().name,
                           lists=TodoList.query.order_by('id').all(),
                           todos=Todo.query.filter_by(list_id=list_id).order_by('id')
                           )

@app.route('/')
def index():
    '#1.Step:Get all object from the database'

    return render_template('index.html',
                           lists=TodoList.query.order_by('id').all(),
                           todos=Todo.query.order_by('id').all()
                           )

@app.route('/todo/create',methods=['Post'])
def create_item():
    description = request.form.get("description", None)
    selected_list = request.form.get("selected_list", None)
    list_name_id = TodoList.query.filter_by(name=selected_list).first().id
    try:
        new_task=Todo(name=description,list_id=list_name_id)
        db.session.add(new_task)
        db.session.commit()
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    print(description)
    return redirect(url_for(f'get_list',list_id=list_name_id))


@app.route('/todo/change_complete',methods=['Post'])
def change_complete():
    data = request.get_json()
    print(f'''
            Description:{data["description"]}\n done: {data['done']}           '''
          )
    try:
        task = Todo.query.filter_by(name=data['description']).first()
        task.done = data['done']
        db.session.commit()
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todo/delete_item',methods=['delete'])
def delete_item():
    data = request.get_json()
    print(f'''
            Description:{data["description"]} 
          '''
          )
    try:
        Todo.query.filter_by(name=data['description']).delete()
        db.session.commit()
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    return jsonify({'success': True})

if __name__=='__main__':
    app.run(host='0.0.0.0',port='3000',debug=True)