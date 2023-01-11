from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL, InputRequired
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from time import strftime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ##CONFIGURE TABLE
with app.app_context():
    class List(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        subject = db.Column(db.String(250), unique=True, nullable=False)
        body = db.Column(db.Text, nullable=False)
        important = db.Column(db.Boolean, nullable=False)


    db.create_all()


class NewThing(FlaskForm):
    subject = StringField("Your to do: ", validators=[DataRequired()])
    body = CKEditorField("Add A Larger Description to your 'to do' Here:", validators=[DataRequired()])
    important = SelectField("Select 'yes' to prioritize", choices=[('', 'No'), (True, 'Yes')], coerce=bool)
    submit = SubmitField("Submit To do")


@app.route('/')
def get_all_posts():
    posts = List.query.all()
    return render_template("index.html", posts=posts)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = List.query.get(post_id)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = NewThing()
    if form.validate_on_submit():
        new_post = List(
            subject=form.subject.data,
            body=form.body.data,
            important=form.important.data,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=form)


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    post = List.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
