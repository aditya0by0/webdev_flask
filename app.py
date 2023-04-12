from flask import Flask, render_template, jsonify, request

from SQLReadWrite import SQLReadWrite
app = Flask(__name__)

@app.route("/")
def hello_world():
	jobs = SQLReadWrite.get_data('job')
	return render_template('home.html', jobs=jobs, company_name = 'ABCD')

@app.route("/api/jobs")
def list_jobs():
	jobs = SQLReadWrite.get_data('job')
	return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
	jobs = SQLReadWrite.get_data('job', field='id', operator='=', value=id)
	# return jsonify(jobs)
	if not jobs :  
		return "Not Found", 404
		
	return render_template('jobPage.html', job=jobs[0], company_name='ABCD')

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
	data = request.form
	job = SQLReadWrite.get_data('job', field='id', operator='=', value=id)
	SQLReadWrite.store_app_to_db(id, application=data)
	return render_template('app_submitted.html', application=data, job=job[0])




if __name__ == "__main__":
	app.run(host='0.0.0.0', debug = True)
