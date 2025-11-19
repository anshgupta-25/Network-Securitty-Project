from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

HONEYPOT_INGEST = os.getenv('HONEYPOT_INGEST', 'http://127.0.0.1:8000/ingest/web')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Simulate a vulnerable login endpoint that forwards attempts to the honeypot
    username = request.form.get('username') or request.json.get('username') if request.is_json else None
    password = request.form.get('password') or request.json.get('password') if request.is_json else None
    src_ip = request.remote_addr or '127.0.0.1'

    payload = {
        'type': 'auth',
        'payload': {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'src_ip': src_ip,
            'username': username,
            'password': password,
            'success': False,
            'service': 'web'
        }
    }

    try:
        # forward to honeypot ingest endpoint
        requests.post(HONEYPOT_INGEST, json=payload, timeout=2)
    except Exception:
        # swallow network errors; this is a local simulation
        pass

    # Always return a fake login page response
    return jsonify({'status': 'failed', 'message': 'Invalid credentials'}), 401

@app.route('/submit_cmd', methods=['POST'])
def submit_cmd():
    # Endpoint to simulate an attacker sending commands after compromise
    cmd = request.form.get('command') or (request.json.get('command') if request.is_json else None)
    src_ip = request.remote_addr or '127.0.0.1'
    session_id = request.form.get('session_id') or request.json.get('session_id') if request.is_json else 'web-session-1'

    payload = {
        'type': 'command',
        'payload': {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'session_id': session_id,
            'src_ip': src_ip,
            'command': cmd,
            'response': ''
        }
    }

    try:
        requests.post(HONEYPOT_INGEST, json=payload, timeout=2)
    except Exception:
        pass

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=False)
