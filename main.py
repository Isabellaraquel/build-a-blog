from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(480))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        
        title = request.form['title']
        body = request.form['body']
        new_post = Blog(title, body)
        db.session.add(new_post)
        db.session.commit()

    posts = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", 
            posts=list(reversed(posts)))


@app.route('/blog', methods=['GET'])
def blog():
    if request.args:
        post = Blog.query.get(request.args['id'])
        return render_template('post.html',post=post)

    posts = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", posts=list(reversed(posts)))


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        titleEmpty = False
        bodyEmpty = False
        if not request.form['title']:
            titleEmpty = True
        if not request.form['body']:
            bodyEmpty = True
        if titleEmpty or bodyEmpty:
            return render_template('newpost.html',title="Build A Blog",titleError=titleEmpty,bodyError=bodyEmpty)
        else:
            title = request.form['title']
            body = request.form['body']
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            url = f"/blog?id={new_post.id}"
            return redirect(url)
    else:
        return render_template('newpost.html',title="Build A Blog")


@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Blog.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()