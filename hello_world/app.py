import json
import boto3
from flask_lambda import FlaskLambda
from flask import request
from botocore.exceptions import ClientError

# import requests
# session = boto3.Session(profile_name = '579879500798_mstar-operator')

app = FlaskLambda(__name__)

ddb = boto3.resource('dynamodb')
table = ddb.Table('student-new-git')

# def lambda_handler(event, context):
#     students_data = table.scan()['Items']
#     return json_response(students_data)

@app.route('/students', methods=['GET', 'POST'])
def put_or_list_student():
    try:
        if request.method == 'GET':
            students_data = table.scan()['Items']
            return json_response(students_data)
        else:
            # res = request.get_json()
            # print("logging fata*************"+ res)
            # table.put_item(res)
            table.put_item(Item=request.form.to_dict())
            return json_response({'message': 'student entry updated'})
    except ClientError as err:
        print(err)

# Works well with sam local start-api and sam deploy (run lambda in aws console) and sam local invoke
def json_response(data, response_code = 200):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data),
    }

# {"body":"[{\"student_name\": \"Vicky\", \"student_id\": \"200\"}, {\"student_name\": \"Rocky\", \"student_id\": \"100\"}]","headers":{"Content-Type":"application/json"},"statusCode":200}

# Works well with sam local start-api
# def json_response(data, response_code = 200):
#     return json.dumps(data), response_code, {'Content-Type': 'application/json'}

# [{"student_name": "Vicky", "student_id": "200"}, {"student_name": "Rocky", "student_id": "100"}]