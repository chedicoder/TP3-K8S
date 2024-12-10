import logging
import re
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from prometheus_client import Counter, Histogram, Gauge,make_wsgi_app, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import time
import psutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Custom metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', ['method', 'status', 'path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'status', 'path'])
REQUEST_IN_PROGRESS = Gauge('http_requests_in_progress', 'HTTP Requests in progress', ['method', 'path'])

# System metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')

def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)

@app.before_request
def before_request():
    request.start_time = time.time()
    REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).inc()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(method=request.method, status=response.status_code, path=request.path).inc()
    REQUEST_LATENCY.labels(method=request.method, status=response.status_code, path=request.path).observe(request_latency)
    REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).dec()
    return response

@app.route('/metrics')
def metrics():
    update_system_metrics()
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Modify the middleware to return bytes
def metrics_app(environ, start_response):
    update_system_metrics()
    data = generate_latest(REGISTRY)
    status = '200 OK'
    headers = [('Content-Type', CONTENT_TYPE_LATEST), ('Content-Length', str(len(data)))]
    start_response(status, headers)
    return [data]

# Use the modified middleware
app_dispatch = DispatcherMiddleware(app, {
    '/metrics': metrics_app
})

# Logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.msg,
            "time": self.formatTime(record, self.datefmt),
            "logger": record.name,
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcname": record.funcName,
            "request": {
                "method": request.method,
                "url": request.url,
                "remote_addr": request.remote_addr,
                "user_agent": str(request.user_agent)
            }
        }
        if record.args:
            log_record['message'] = log_record['message'] % record.args
        return json.dumps(log_record)

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Default credentials
USERNAME = 'admin'
PASSWORD = 'password'

def is_weak_password(password):
    if len(password) < 8:
        return True
    if not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
        return True
    return False

@app.before_request
def log_request_info():
    logger.info(f"Request received")

@app.after_request
def log_response_info(response):
    logger.info(f"Response sent with status: {response.status_code}")
    return response

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username == USERNAME and password == PASSWORD:
        flash('Login successful!', 'success')
        logger.info('Login successful for user: %s', username)
        if is_weak_password(password):
            logger.warning('weak password used by user: %s', username)
        return redirect(url_for('welcome'))
    else:
        flash('Invalid credentials. Please try again.', 'danger')
        logger.warning('Login failed for user: %s', username)
        return redirect(url_for('second_level_auth'))


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/second_level_auth')
def second_level_auth():
    return render_template('second_level_auth.html')

if __name__ == '__main__':
  app.run()