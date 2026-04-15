# Multi-Switch Flow Table Analyzer

## Project Description
This project analyzes flow tables of multiple OpenFlow switches in a Software Defined Networking (SDN) environment.  
The Ryu controller dynamically retrieves flow statistics from switches created using Mininet and identifies active and unused flow rules.

---

## Objectives
- Analyze flow tables of multiple OpenFlow switches
- Identify active and unused flow rules
- Monitor packet and byte counts dynamically
- Demonstrate SDN principles using Ryu and Mininet

---

## Tools & Technologies
- Ryu SDN Controller (Docker-based)
- Mininet Network Emulator
- OpenFlow 1.3
- Python

---

## System Architecture
Mininet emulates OpenFlow switches which connect to a Docker-based Ryu controller via OpenFlow protocol.

---

## How to Run the Project

### Step 1: Start Ryu Controller (Docker)
```bash
docker run -it --rm -v $(pwd):/app -p 6633:6633 osrg/ryu
Inside the Docker container, run the following commands:
cd /app
export PYTHONPATH=/app
ryu-manager flow_analyzer ...
```

### Step 2: Run Mininet (New Terminal)
Open a new terminal on the host system and run:
```bash
sudo mn --topo=linear,3 \
--controller=remote,ip=127.0.0.1,port=6633 \
--switch=ovsk,protocols=OpenFlow13
```

### Step 3: Generate Traffic
Inside the Mininet CLI: 
```bash
h1 ping h3
```
Output : 
The Ryu controller displays:
--Flow table entries for each switch
--Packet and byte counters
--Rule classification as ACTIVE or UNUSED

The output updates dynamically as traffic flows through the network.
