# app.py
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# View to get an earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    
    if earthquake:
        return make_response(
            jsonify({
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year
            }), 200
        )
    else:
        return make_response(
            jsonify({"message": f"Earthquake {id} not found."}), 404
        )

# Task #4: View to get earthquakes matching a minimum magnitude value
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Prepare the result data
    result = {
        "count": len(earthquakes),
        "quakes": [{
            "id": eq.id,
            "location": eq.location,
            "magnitude": eq.magnitude,
            "year": eq.year
        } for eq in earthquakes]
    }

    return make_response(jsonify(result), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
