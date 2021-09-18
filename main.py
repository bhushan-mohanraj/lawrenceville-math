from app import create_app


app = create_app()

with app.app_context():
    from app.scripts import *

    create_db()
    create_events()
    create_tests()
