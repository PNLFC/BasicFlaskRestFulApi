from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class StudentModel(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    amount_due = db.Column(db.Integer, nullable=False)

    #def __repr__(self):
        #return f"Student(name = {first_name,last_name}, dob = {dob.strftime('%m/%d/%Y')}, amount_due={amount_due})"

#db.create_all()


student_put_args = reqparse.RequestParser()
student_put_args.add_argument("first_name", type=str, help="first name is required", required=True)
student_put_args.add_argument("last_name", type=str, help="last name is required", required=True)
student_put_args.add_argument("dob", type=str, help="date of birth is required", required=True)
student_put_args.add_argument("amount_due", type=int, help="amount due is required", required=True)

student_patch_args = reqparse.RequestParser()
student_patch_args.add_argument("first_name", type=str, help="first name is required")
student_patch_args.add_argument("last_name", type=str, help="last name is required")
student_patch_args.add_argument("dob", type=str, help="date of birth is required")
student_patch_args.add_argument("amount_due", type=int, help="amount due is required")

resource_fields = {
    'id' : fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'dob': fields.DateTime,
    'amount_due': fields.Integer
}


class StudentData(Resource):
    @marshal_with(resource_fields)
    def get(self, student_id):
        result = StudentModel.query.filter_by(id=student_id).first()
        print(result,'here')
        if not result:
            abort(404, message="Could not find video with that id")
        return result,201

    @marshal_with(resource_fields)
    def put(self):
        new_id = str(uuid.uuid4()).replace('-','')
        args = student_put_args.parse_args()
        print(new_id)
        result = StudentModel.query.filter_by(id=new_id).first()
        while (result == True):
            new_id = str(uuid.uuid4()).replace('-','')
            print(new_id)
            result = StudentModel.query.filter_by(id=new_id).first()
        y, m, d = args['dob'].split('-')
        dateField = datetime.datetime(int(y), int(m), int(d))
        student = StudentModel(id=new_id, first_name=args['first_name'],
                               last_name=args['last_name'], dob=dateField, amount_due=args['amount_due']
                               )
        db.session.add(student)
        db.session.commit()
        return student, 201
    
    @marshal_with(resource_fields)
    def patch(self, student_id):
        args = student_patch_args.parse_args()
        result = StudentModel.query.filter_by(id=student_id).first()
        if not result:
            abort(404, message="Student doesn't exist, cannot update")
        if args["first_name"]:
            result.first_name = args['first_name']
        if args["last_name"]:
            result.last_name = args['last_name']
        if args["dob"]:
            result.dob = args['dob']
        if args["amount_due"]:
            result.dob = args['amount_due']
        db.session.commit()
        return result, 201
        
    
    def delete(self, student_id):
        result = StudentModel.query.filter_by(id=student_id).first()
        if not result:
            abort(404, message="Student doesn't exist, cannot update")
        db.session.delete(result)
        db.session.commit()
        return '', 204
            

routes = [
    "/student",
    "/student/<string:student_id>"
]

api.add_resource(StudentData, *routes)

if __name__ == '__main__':
    app.run(debug=True)