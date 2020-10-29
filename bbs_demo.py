from flask import Flask, render_template, request, redirect, url_for, session
from models import User, Issue, Comment
from exts import db, valiEmail
from decorators import login_required
import config


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'issues' : Issue.query.order_by(db.desc('create_time')).all()
    }
    return render_template('index.html', **context)


@app.route('/d/<issue_id>')
def d(issue_id):
    res = Issue.query.filter(Issue.id == issue_id).first()
    return render_template('d.html', issue_item = res)


@app.route('/add_comment/', methods=["POST"])
@login_required
def add_comment():
    comment = Comment(comment=request.form.get('comment'))
    issue_id = request.form.get('issue_id')
    user_id = session['user_id']
    user = User.query.filter(User.id==user_id).first()
    issue = Issue.query.filter(Issue.id == issue_id).first()
    comment.author = user
    comment.issue = issue
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('d', issue_id=issue_id))


@app.route('/issue/', methods=['GET', 'POST'])
@login_required
def issue():
    if request.method == 'GET':
        return render_template('issue.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        issue = Issue(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        issue.author = user
        db.session.add(issue)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email==email, User.password==password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.email == email).first()
        if user:
            return u"该邮箱已存在!"
        elif not valiEmail(email):
            return u"请检查邮箱格式I"
        else:
            if password1 == password2:
                user = User(email=email, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def valiLogin():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()
