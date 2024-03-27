
from flask import request, jsonify
from application.security import user_datastore
from flask import current_app as app
from werkzeug.security import check_password_hash
from application.jobs.tasks import create_products_csv
from celery.result import AsyncResult
from flask import send_file

@app.post('/api/login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    print(email, data.get("password"))
    if not email:
        return jsonify({"message": "email not provided"}), 400

    user = user_datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User Not Found"}), 404
    
    if not user.active:
        return jsonify({"message": "User is inactive"}), 400

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
    else:
        return jsonify({"message": "Wrong Password"}), 400


@app.get('/api/load-csv')
def load_csv():
    task = create_products_csv.delay()
    return jsonify({"task-id": task.id})

@app.get('/api/products-csv/<task_id>')
def products_csv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
        # return send_file(filename, as_attachment=True,download_name=str(filename),mimetype="text/csv")
    else:
        return jsonify({"message": "Task Pending"}), 404