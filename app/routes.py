from app import api, app
from app.controller import UserController, TodoController


@app.route('/')
def home():
    return "Hello World"


api.add_resource(UserController.WithoutParams, '/users')
api.add_resource(UserController.WithParams, '/users/<id>')
api.add_resource(UserController.Login, '/login')
api.add_resource(TodoController.TodoWithoutParams, '/todo')
api.add_resource(TodoController.TodoWithParams, '/todo/<id>')
