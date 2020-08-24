from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import os

db_connect = create_engine('sqlite:///captcha.db')
app = Flask(__name__)
api = Api(app)

class Captcha(Resource):

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from captcha;")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        try:
            conn = db_connect.connect()
            token = request.json['token']
            date = request.json['date']

            conn.execute("insert into user values(null, '{0}','{1}')".format(token, date))
            query = conn.execute('select * from user order by id desc limit 1')
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            return jsonify(result)
        except Exception as e:
            print(e)
            return jsonify({"result": False, "error": str(e)})

    def delete(self):
        try:
            conn = db_connect.connect()
            conn.execute("delete from captcha;")
            return jsonify({"result": True})
        except Exception as e:
            print(e)
            return jsonify({"result": False, "error": str(e)})

class CaptchaByDate(Resource):

    def get(self):
        try:
            conn = db_connect.connect()
            date = request.json['date']

            query = conn.execute("select * from captcha where date > '{0}'".format(date))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

            return jsonify(result)
        except Exception as e:
            print(e)
            return jsonify({"result": False, "error": str(e)})


api.add_resource(Captcha, '/captcha')
api.add_resource(CaptchaByDate, '/captcha/<date>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)