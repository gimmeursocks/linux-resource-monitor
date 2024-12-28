# Linux System Resource Monitor

## DEPI R2 - Marathon 1
**Software Development Track - DevOps Profile**

A simple containerized application that monitors and reports Linux system resources in real-time.

## 👥 Team Members
- Hamid Walid (@gimmeursocks)
- Hafez Adel (@hafez599)

## 🚀 Features
- Real-time monitoring of:
  - CPU usage and cores
  - Memory utilization
  - Disk space
- RESTful API endpoints
- Docker containerization
- Simple deployment process

## 🛠 Technology Stack
- Python 3.9
- Flask Web Framework
- Docker
- psutil library

## 🔧 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/gimmeursocks/linux-resource-monitor.git resource-monitor
cd resource-monitor
```

2. Deploy the application:
```bash
chmod +x deploy.sh
./deploy.sh
```

3. Access the metrics:
```bash
curl http://localhost:5000/metrics
```

## 📋 API Endpoints

### Health Check
```
GET /health
Response: {
    "checks": {
        "cpu": {
            "load": int,
            "status": str
        },
        "disk": {
            "free_space_gb": int,
            "status": str
        },
        "memory": {
            "available_gb": int,
            "status": str
        }
    },
    "status": str,
    "timestamp": date
}
```

### System Metrics
```
GET /metrics
Response: {
    "cpu": {
        "usage_percent": float,
        "cores": int
    },
    "memory": {
        "total": int,
        "available": int,
        "used": int,
        "percent": float
    },
    "disk": {
        "total": int,
        "used": int,
        "free": int,
        "percent": float
    }
}
```

## 📁 Project Structure
```
resource-monitor/
├── app.py              # Main application
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── deploy.sh          # Deployment script
└── README.md          # This file
```

---
*Created as part of DEPI R2 - Marathon 1, Software Development Track (DevOps Profile)*