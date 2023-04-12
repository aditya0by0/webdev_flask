from sqlalchemy import create_engine, text
import os 

class SQLReadWrite:
	
	username = os.environ.get('MYSQL_USERNAME')
	password = os.environ.get('MYSQL_PASSWORD')
	host =  os.environ.get('MYSQL_HOST', default='localhost')
	database = os.environ.get("MYSQL_DB")
	
	engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

	@staticmethod
	def get_data(table_name,**kwargs):
		
		result_dict=[]
		string = "select * from " + table_name

		if kwargs :
			string += ' where'
			for key in ['field', 'operator', 'value']:
				if key not in kwargs: 
					raise 'All parameters not supplied'
				string += ' ' + kwargs[key]
				 

		with SQLReadWrite.engine.connect() as conn:
			result = conn.execute(text(string))
		
		return [dict(row) for row in result.all()]
	
	@staticmethod
	def store_app_to_db(job_id,application):

		query = text("""INSERT INTO applications (job_id, full_name,  email, linkedin_url,
					 education, work_experience, resume_url) VALUES (:job_id, :full_name, :email,
					 :linkedin_url, :education, :work_experience, :resume_url)""")
		
		with SQLReadWrite.engine.connect() as conn:
			result = conn.execute(query,
								  job_id=job_id,
								  full_name=application['full_name'],
								  email=application['email'],
								  linkedin_url=application['linkedin_url'],
								  education=application['education'],
								  work_experience=application['work_ex'],
								  resume_url=application['resume_url'])

