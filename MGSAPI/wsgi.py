from app.main import create_app, db
from app import blueprint

app = create_app('prod')
app.register_blueprint(blueprint)

app.app_context().push()

