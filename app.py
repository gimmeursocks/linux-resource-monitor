import psutil
import time
from flask import Flask, jsonify

app = Flask(__name__)

def bytes_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3), 2)

# To make output more readable as GB
def readable_output(mem):
    strmem = str(mem)
    return f"{strmem} ({bytes_to_gb(mem)} GB)"

def get_system_metrics():
    metrics = {
        "cpu": {
            "usage_percent": str(psutil.cpu_percent(interval=1))+"%",
            "cores": psutil.cpu_count()
        },
        "memory": {
            "total": readable_output(psutil.virtual_memory().total),
            "available": readable_output(psutil.virtual_memory().available),
            "used": readable_output(psutil.virtual_memory().used),
            "percent": str(psutil.virtual_memory().percent)+"%"
        },
        "disk": {
            "total": readable_output(psutil.disk_usage('/').total),
            "used": readable_output(psutil.disk_usage('/').used),
            "free": readable_output(psutil.disk_usage('/').free),
            "percent": str(psutil.disk_usage('/').percent)+"%"
        }
    }
    return metrics

# Checks cpu, memory, and disk usage above certain thresholds
def check_system_health():
    try:
        health_metrics = {
            "status": "healthy",
            "checks": {
                "cpu": {
                    "status": "healthy",
                    "load": psutil.cpu_percent(interval=1)
                },
                "memory": {
                    "status": "healthy",
                    "available_gb": round(bytes_to_gb(psutil.virtual_memory().available))
                },
                "disk": {
                    "status": "healthy",
                    "free_space_gb": round(bytes_to_gb(psutil.disk_usage('/').free))
                }
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # If CPU is above 90%
        if health_metrics["checks"]["cpu"]["load"] > 90:
            health_metrics["checks"]["cpu"]["status"] = "warning"
            health_metrics["status"] = "degraded"

        # If memory less than 10% or 1GB available
        if (psutil.virtual_memory().percent > 90 or 
            health_metrics["checks"]["memory"]["available_gb"] < 1):
            health_metrics["checks"]["memory"]["status"] = "warning"
            health_metrics["status"] = "degraded"

        # If disk less than 10% or 1GB free
        if (psutil.disk_usage('/').percent > 90 or 
            health_metrics["checks"]["disk"]["free_space_gb"] < 1):
            health_metrics["checks"]["disk"]["status"] = "warning"
            health_metrics["status"] = "degraded"

        health_metrics["checks"]["cpu"]["load"] = str(health_metrics["checks"]["cpu"]["load"])+"%"
        health_metrics["checks"]["memory"]["available_gb"] = str(health_metrics["checks"]["memory"]["available_gb"])+" GB"
        health_metrics["checks"]["disk"]["free_space_gb"] = str(health_metrics["checks"]["disk"]["free_space_gb"])+" GB"

        return health_metrics

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

@app.route('/health')
def health_check():
    return jsonify(check_system_health())

@app.route('/metrics')
def metrics():
    return jsonify(get_system_metrics())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)