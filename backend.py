from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import time
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging for monitoring
logging.basicConfig(filename='monitoring.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    return "System Resource Monitor Backend is Running!"

@app.route('/metrics')
def get_metrics():
    time.sleep(1)  # Ensure accurate CPU measurement
    data = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    
    # Logging metrics
    logging.info(f"CPU: {data['cpu_usage']}%, Memory: {data['memory_usage']}%, Disk: {data['disk_usage']}%")
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
