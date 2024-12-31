from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from vehicle_csv_agent import CSVAgent
import logging


class QueryForm(FlaskForm):
    query = StringField('Enter your query', validators=[DataRequired()])
    submit = SubmitField('Ask')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

# Initialize the CSVAgent
agent = CSVAgent(csv_path="data/v2_clean.csv")

# Set up logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=["GET", "POST"])
def index():
    form = QueryForm()
    response = None
    if form.validate_on_submit():
        user_query = form.query.data
        logging.debug(f"User query: {user_query}")
        response = agent.run(user_query)
        logging.debug(f"Agent response: {response}")

    return render_template("index.html", form=form, response=response)


if __name__ == "__main__":
    app.run(debug=True)
