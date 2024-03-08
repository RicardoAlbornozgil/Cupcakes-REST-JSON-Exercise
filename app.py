"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "The very secret key"

connect_db(app)

# Routes
@app.route('/')
def root():
    """Render homepage"""
    return render_template("index.html")


@app.route('/api/cupcakes')
def list_cupcakes():
    """
        Return all cupcakes in the db.
            Returns JSON: 
            {cupcakes: [{id, flavor, rating, image}, ...]}
    """
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)



@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about new cupcake.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """

    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    # POST requests should return HTTP status of 201 CREATED
    return (jsonify(cupcake=cupcake.to_dict()), 201)



@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """
        Return data on specific cupcake
            Returns JSON like:
            {cupcake: [{id, flavor, rating, size, image}]}
    """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())



@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """
        Update cupcake from data in request
            Returns JSON like:
            {cupcake: [{id, flavor, rating, size, image}]}
    """

    # Get Request data
    data = request.json
    # Get cupcake data
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def remove_cupcake(cupcake_id):
    """
        Delelete cupcake and return confirmation message
            Returns JSON of {message: 'Deleted}    
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")


if __name__ == '__main__':
    app.run(debug=True)




    ## **Further Study**

# - Add tests to make sure that the GET/PATCH/DELETE routes return a 404 when the cupcake cannot be found.

# - Add functionality for searching for cupcakes where you can type in a search term, submit to the backend and see a newly filtered list of cupcakes.
    
#     **HINT:** Make sure a search term is passed to the backend and that you are using a ***LIKE*** or ***ILIKE*** SQL query to search.
    
# - Refactor your front-end code to be object-oriented using class methods to ***fetchAllCupcakes*** 
#    and ***createCupcakes*** and instance methods for updating and deleting cupcakes as well as searching for cupcakes.

# - Refactor your HTML page to render a form created by WTForms.

# - Enhance your search functionality so that you do not need to wait to submit to filter by flavors.
    
# - Add functionality on the front-end to update a cupcake.
    
# - **Are you still here??** Then add another table for ingredients. When you add or edit a cupcake, you can 
#    identify what ingredients you need for that cupcake. You should also have a page where you can add or edit ingredients.