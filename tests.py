import unittest

from app import app
from models import db, Cupcake

# # Use test database and don't clutter tests with SQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
# app.config['SQLALCHEMY_ECHO'] = False

# # Make Flask errors be real errors, rather than HTML pages with error info
# app.config['TESTING'] = True

with app.app_context():    
    db.drop_all()
    db.create_all()


CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(unittest.TestCase):
    """Tests for views of API."""

    @classmethod
    def setUpClass(cls):
        """Create test database and set up Flask app."""

        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Drop test database tables."""

        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Create a new session before each test."""

        self.app = app.test_client()
        with app.app_context():
            self.session = db.session
            self.cupcake = Cupcake(flavor="TestFlavor", size="TestSize", rating=5, image="http://test.com/cupcake.jpg")
            self.session.add(self.cupcake)
            self.session.commit()

    def tearDown(self):
        """Rollback changes and delete any cupcakes added during the test."""
        with app.app_context():
            # Rollback any changes made during the test
            self.session.rollback()
            
            # Delete any cupcakes added during the test
            self.session.query(Cupcake).delete()
            self.session.commit()

            # Close the session
            self.session.close()

    def test_list_cupcakes(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get("/api/cupcakes")

                self.assertEqual(resp.status_code, 200)
                data = resp.json
                # Debug statement to print the number of cupcakes retrieved
                print("Number of cupcakes retrieved:", len(data['cupcakes']))

                self.assertIsInstance(data['cupcakes'], list)
                self.assertEqual(len(data['cupcakes']), 1)

    def test_get_cupcake(self):
        with app.app_context():
            with app.test_client() as client:
                cupcake = Cupcake.query.filter_by(flavor="TestFlavor", size="TestSize").first()
                url = f"/api/cupcakes/{cupcake.id}"
                resp = client.get(url)

                self.assertEqual(resp.status_code, 200)
                data = resp.json
                self.assertEqual(data, {
                    "cupcake": {
                        "id": cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                })


    def test_get_cupcake_missing(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/99999"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 404)


    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)


    def test_update_cupcake(self):
        with app.app_context():
            with app.test_client() as client:
                cupcake = Cupcake.query.filter_by(flavor="TestFlavor", size="TestSize").first()
                url = f"/api/cupcakes/{cupcake.id}"
                resp = client.patch(url, json=CUPCAKE_DATA_2)

                self.assertEqual(resp.status_code, 200)

                data = resp.json
                self.assertEqual(data, {
                    "cupcake": {
                        "id": cupcake.id,
                        "flavor": "TestFlavor2",
                        "size": "TestSize2",
                        "rating": 10,
                        "image": "http://test.com/cupcake2.jpg"
                    }
                })

    def test_update_cupcake_missing(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/99999"
            resp = client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        with app.app_context():
            with app.test_client() as client:
                initial_count = Cupcake.query.count()
                cupcake = Cupcake.query.filter_by(flavor="TestFlavor", size="TestSize").first()
                url = f"/api/cupcakes/{cupcake.id}"
                resp = client.delete(url)
                self.assertEqual(resp.status_code, 200)
                data = resp.json
                self.assertEqual(data, {"message": "Deleted"})
                self.assertEqual(Cupcake.query.count(), initial_count - 1)

    def test_delete_cupcake_missing(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/99999"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    unittest.main()