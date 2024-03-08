"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


db = SQLAlchemy()


DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"



# Models below

class Cupcake(db.Model):
    """model for cupcakes"""

    __tablename__ = "cupcakes"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True)
    
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)
    
    def to_dict(self):
        """Serialize cupcake to a dict of cupcake info"""
        
        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }
    
    
def connect_db(app):
    """Connect to db"""
    db.app = app
    db.init_app(app)

    with app.app_context():
        inspector = inspect(db.engine)  # Create an inspector for the database engine
        # Check if the 'cupcakes' table exists in the database
        if not inspector.has_table("cupcakes"):
            db.create_all()  # If the 'cupcakes' table doesn't exist, create all tables