from flask import Flask, request, jsonify, make_response
from rq import Queue
from rq.job import Job
import worker

class API():

    app = Flask('multi_process')

    def __init__(self):
        pass

    # 1. API Endpoint that will receive the work requests
    # 2. Passes the work to a worker
    # 3. Returns a job id
    # For every -mi INTERVAL start a new InterpolatedValues Job for the day prior?
    @staticmethod
    @app.route('/esbi/stg1/api_runner', methods=['GET'])
    def api_runner():
            results = {}
            # Want to set the following args:
        # start time
            # end time
            # tag
            # server_name
            arguments = ["hello", "world"]
        # Set up a connection using configuration in worker.conn
            q = Queue(connection=worker.conn)
            # Start the job:
            # a. func: Function to call
            # b. args: arguments to pass to fucntion
            # c. result_ttl: seconds for the job to live
            # d. Timeout: in seconds
            job = q.enqueue_call(func=worker.pull_interpolated, args=arguments, result_ttl=5000, timeout=3600)
            results['job_id'] = job.get_id() # Receive the job_id
            return jsonify({'result': results}) # Return the job_id to the client


    @staticmethod
    @app.route('/esbi/stg1/job_status/<job_key>', methods=['GET'])
    def get_results(job_key):
        results = {}
        job = Job.fetch(job_key, connection=worker.conn)

        if job.is_finished:
            return "SUCCESS(200): {JobResult}".format(JobResult=job.result)
        else:
            return "ERROR(202): No Job Result"

    # Error Handler
    @staticmethod
    @app.route('/esbi/stg1/job_status/<job_key>', methods=['GET'])
    def get_results(job_key):
        results = {}
        job = Job.fetch(job_key, connection=worker.conn)

        if job.is_finished:
            return "SUCCESS(200): {JobResult}".format(JobResult=job.result)
        else:
            return "ERROR(202): No Job Result"

    # Error Handler
    @staticmethod
    @app.errorhandler(404)
    def api_timeout(error):
        return make_response(jsonify({'ERROR': 'API Call Timeout'}), 404)

    # Run the flask server:
    def run(self, debug=True, port=5005):
        self.app.run(host="0.0.0.0", port=port, debug=debug, threaded=True)


es_api = API()
es_api.run(True)
