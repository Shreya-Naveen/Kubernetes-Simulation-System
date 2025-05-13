# Kubernetes-Simulation-System
A lightweight simulation-based distributed system that mimics core Kubernetes cluster management functionalities. Developed as part of the **Cloud Computing Course**, this project provides a platform for understanding key distributed computing concepts such as scheduling, health monitoring, and fault tolerance.

---

## 📌 Project Objectives

- Simulate a distributed cluster with Docker containers as nodes.
- Implement a central API Server to manage the cluster.
- Enable pod scheduling using resource-based strategies.
- Monitor node health via heartbeats and recover from failures.
- Provide CLI or Web-based interface for user interactions.

---

## 🧰 Features

### ✅ Node Management
- Add nodes with a specified number of CPU cores.
- Register and launch Docker containers to simulate nodes.
- Track node status and resource availability.

### 🧠 Pod Scheduling
- Deploy pods with specific CPU requirements.
- Schedule using First-Fit, Best-Fit, or Worst-Fit algorithms.
- Maintain deployment info for failure recovery.

### ❤️ Health Monitoring
- Nodes send periodic heartbeat signals to API Server.
- Detect node failures on missed heartbeats.
- Automatically reschedule pods from failed nodes.

---
## ⚙️ Tech Stack

| Component        | Technology              |
|------------------|--------------------------|
| API Server        | Flask          |
| Node Simulation   | Docker                   |
| Scheduling Logic  | First-Fit / Best-Fit / Worst-Fit |
| Interface         | CLI            |

---

## 🚀 How to Use

### Prerequisites
- Docker installed
- Python 3.x or Node.js (based on API server)
