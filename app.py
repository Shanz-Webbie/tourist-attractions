from flask import Flask, render_template, request, redirect, url_for
from locations import Locations
from forms import AddLocationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_PROJECT'

visit = Locations()
categories = {"recommended": "Recommended", "tovisit": "Places To Go", "visited": "Visited!!!"}

UP_ACTION = "\u2197"
DEL_ACTION = "X"

@app.route("/<category>", methods=["GET", "POST"])
def locations(category):
    locations = visit.get_list_by_category(category)

    if request.method == "POST":
        for name, action in request.form.items():
            if action == UP_ACTION:
                visit.moveup(name)
            elif action == DEL_ACTION:
                visit.delete(name)

    return render_template("locations.html",
                           category=category,
                           categories=categories,
                           locations=locations,
                           add_location=AddLocationForm())

@app.route("/add_location", methods=["POST"])
def add_location():
    add_form = AddLocationForm()
    if add_form.validate_on_submit():
        name = add_form.name.data
        description = add_form.description.data
        category = add_form.category.data
        visit.add(name, description, category)
        return redirect(url_for("locations", category=category, _external=True, _scheme='https'))

    return redirect(url_for("locations", category="recommended", _external=True, _scheme='https'))

@app.route("/")
def index():
    return redirect(url_for("locations", category="recommended", _external=True, _scheme='https'))


