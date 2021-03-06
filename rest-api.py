from flask import Flask
from flask_restful import Api, Resource, reqparse


# Create the flask application and create the api object
app = Flask(__name__)
api = Api(app)

vehicles = [
    {
        "name": "redrover",
        "opcode": 1,
        "time": "2018-10-20 18:53:49",
        "rgb": "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",
        "depth": "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",
        "imu": {
            "speed": 0,
            "px": 0.01210937462747097,
            "py": 0.0002734375011641532,
            "pz": 0.5303027033805847,
            "ow": 0.9993076324462891,
            "ox": 0.03558187559247017,
            "oy": 0.010858267545700073,
            "oz": 0.0005822725361213088
        }
    },
    {
        "name": "cuberover",
        "opcode": 1,
        "time": None,
        "rgb": None,
        "depth": None,
        "imu": None
    }
]


class Vehicle(Resource):

    def get(self, name):
        """
        Will return user if the user is in the list
        :param name:
        :return: tuple with http status code. 200 if user exists, 404 otherwise
        """
        for user in vehicles:
            if name == user["name"]:
                return user, 200
        return "User not found", 404

    def post(self, name):
        """
        Will create a new user
        :param name: the same of the vehicle
        :return: a tuple with the second argument as the http status code
        """
        # Create a parser for the vehicle data
        parser = reqparse.RequestParser()
        parser.add_argument("opcode")
        parser.add_argument("state")
        args = parser.parse_args()

        # Check if user has already been created
        for user in vehicles:
            if name == user["name"]:
                # Return 400 bad request
                return "User with name {} already exists".format(name), 400

        # Add the user to the vehicle list
        user = {
            "name": name,
            "opcode": args["opcode"],
            "state": args["state"]
        }
        vehicles.append(user)
        # Return 201, created
        return user, 201

    def put(self, name):
        """
        Will create a new user or update their info
        :param name: the name of the vehicle
        :return: tuple with the second argument as the http status code
        """
        # Create a parser for the vehicle data
        parser = reqparse.RequestParser()
        parser.add_argument("opcode")
        parser.add_argument("state")
        args = parser.parse_args()

        # Update the user info if it is already in the list
        for user in vehicles:
            if name == user["name"]:
                user["opcode"] = args["opcode"]
                user["status"] = args["status"]
                return user, 200

        # Add the user to the vehicle list
        user = {
            "name": name,
            "opcode": args["opcode"],
            "state": args["state"]
        }
        vehicles.append(user)
        # Return 201, created
        return user, 201

    def delete(self, name):
        """
        Will delete a user from the list of vehicles
        :param name: the name of the vehicle
        :return: tuple with info of the user that was deleted
        """
        global vehicles
        vehicles = [user for user in vehicles if user["name"] != name]
        return "{} is deleted.".format(name), 200


api.add_resource(Vehicle, "/user/<string:name>")
app.run(debug=True)
