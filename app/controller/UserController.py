from app.model.user import Users
from flask import request
from app import response, db
from flask_restful import Resource
from app.library import jwt


class UsersWithoutParams(Resource):
    @jwt.required
    def get(self):
        try:
            users = Users.query.all()
            data = transform(users)
            return response.ok(data, "")
        except Exception as e:
            print(e)

    @jwt.required
    def post(self):
        try:
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']

            users = Users(name=name, email=email)
            users.setPassword(password)
            db.session.add(users)
            db.session.commit()

            access_token = jwt.encode(users)
            refresh_token = jwt.encode(users, access=False)

            return response.ok({
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 'Successfully create data!')

        except Exception as e:
            return response.badRequest('', e)


class UsersWithParams(Resource):
    @jwt.required
    def get(self, id):
        try:
            users = Users.query.filter_by(id=id).first()
            if not users:
                return response.badRequest([], 'Empty....')

            data = singleTransform(users)
            return response.ok(data, "")
        except Exception as e:
            return response.badRequest('', e)

    @jwt.required
    def put(self, id):
        try:
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']

            user = Users.query.filter_by(id=id).first()
            user.email = email
            user.name = name
            user.setPassword(password)

            db.session.commit()

            return response.ok('', 'Successfully update data!')

        except Exception as e:
            print(e)

    @jwt.required
    def delete(self, id):
        try:
            user = Users.query.filter_by(id=id).first()
            if not user:
                return response.badRequest([], 'Empty....')

            db.session.delete(user)
            db.session.commit()

            return response.ok('', 'Successfully delete data!')
        except Exception as e:
            print(e)


class Login(Resource):
    def get(self):
        try:
            token = jwt.decode()
            return response.ok(token, '')
        except Exception as e:
            print(e)

    def post(self):
        try:
            email = request.json['email']
            password = request.json['password']

            user = Users.query.filter_by(email=email).first()
            if not user:
                return response.badRequest([], 'Empty....')

            if not user.checkPassword(password):
                return response.badRequest([], 'Your credentials is invalid')

            data = singleTransform(user, withTodo=False)
            access_token = jwt.encode(data)
            refresh_token = jwt.encode(data, access=False)

            return response.ok({
                'data': data,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, "")
        except Exception as e:
            return response.badRequest('', e)


def transform(users):
    array = []
    for i in users:
        array.append(singleTransform(i))
    return array


def singleTransform(users, withTodo=True):
    data = {
        'id': users.id,
        'name': users.name,
        'email': users.email,
    }

    if withTodo:
        todos = []
        for i in users.todos:
            todos.append({
                'id': i.id,
                'todo': i.todo,
                'description': i.description,
            })
        data['todos'] = todos

    return data
