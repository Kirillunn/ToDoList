from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey
from forms import ListForm, TaskForm, DeleteListForm

# Create app
app = Flask(__name__)

# Create key for CSFR
app.config['SECRET_KEY'] = '1728395Lka!'

# Create database
class Base(DeclarativeBase):
    pass

# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskopia.db"

# Create the extension
db = SQLAlchemy(model_class=Base)

# Initialize the app with the extension
db.init_app(app)

# Create List Table
class List(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    tasks = relationship("Task", back_populates="list")


# Create Task Table
class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    list_id: Mapped[int] = mapped_column(Integer, ForeignKey("list.id"))
    list = relationship("List", back_populates="tasks")

# Create all tables
with app.app_context():
    db.create_all()

# Show all lists on the sidebar
def show_lists():
    result = db.session.execute(db.select(List))
    all_lists = result.scalars()
    return all_lists


@app.route("/", methods=["GET", "POST"])
def home():
    # Add new list to the db
    form = ListForm()
    if form.validate_on_submit():
        new_list = List(
            title=form.title.data,
            date=form.date.data,
        )
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('home'))

    all_lists = show_lists()

    return render_template("index.html", form=form, all_lists=all_lists)

# Show a particular list
@app.route("/list/<int:list_id>", methods=['GET', 'POST'])
def list(list_id):
    all_lists = show_lists()

    # Add a task  to the list
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            description = form.description.data,
            list_id = list_id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("list", list_id=list_id))

    # Show all tasks of the list
    result = db.session.execute(db.select(Task).where(Task.list_id == list_id))
    all_tasks = result.scalars()

    return render_template("list.html", all_lists=all_lists,
                           list_id=list_id, form=form, all_tasks=all_tasks)


if __name__ == "__main__":
    app.run(debug=True)
