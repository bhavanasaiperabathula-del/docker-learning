# 🚀 Docker Networking Overview
 
Container networking refers to how containers connect and communicate with:
 

*   Each other
     
*   The Docker host
     
*   External networks
     
*   Other services
     

Docker manages networking using **network drivers, namespaces, virtual bridges, and iptables rules** on the host.
 
---
 

## 🟦 Default Bridge Network
 
When Docker starts, it creates a default bridge network: `docker0`
 
**Characteristics:**
 

*   Containers get private IPs (e.g., `172.17.0.x`)
     
*   Containers can talk to each other using IP addresses
     
*   They cannot talk using container names (DNS not enabled in default bridge)
     
*   Containers can reach the internet (via NAT)
     
*   No isolation — all containers can reach each other
     
*   Containers do not know what kind of network they are attached to; isolation and routing are managed by Docker.
     

---
 

## 🟪 User-Defined Networks
 
You can create your own networks:
 

    docker network create -d bridge my-net

Run a container inside it:
 

    docker run -d --name application --network my-net -p 8080:8080 project-api

**Benefits:**
 

*   Built-in DNS ⇒ containers can resolve each other by name
     
*   Better isolation
     
*   Cleaner, readable container communication
     
*   Logical grouping of containers
     
*   Restrict groups by placing them on different networks
     

**Example:**
 

*   `my-app-network` → group of containers that should talk to each other
     
*   `my-db-network` → isolated group
     

---
 

## 🔐 Connecting Containers to Multiple Networks
 
Scenario: API needs internet + DB access, DB should not have internet.
 
**Steps:**
 

    docker network create public-net
    docker network create --internal private-net

*   `--internal` = no internet access
     

    docker run -d --name api --network public-net my-api
    docker network connect private-net api
    
    docker run -d --name db --network private-net my-db

**Result:**
 

| Container | public-net | private-net |
| --------- | ---------- | ----------- |
| api | ✔ | ✔ |
| db | ❌ | ✔ |

*   API can reach DB
     
*   DB cannot reach internet → perfect isolation
     

---
 

## 🟥 Understanding Docker Network Drivers
 <table><tbody><tr><th >Driver</th><th >Description</th></tr><tr><td >bridge</td><td >Default driver; container gets private IP, NAT for outgoing traffic</td></tr><tr><td >host</td><td >Removes isolation; container shares host network stack</td></tr><tr><td >none</td><td >No networking at all</td></tr><tr><td >overlay</td><td >Multi-host networking for Swarm/Kubernetes</td></tr><tr><td >macvlan</td><td >Containers get real MAC address on LAN</td></tr><tr><td >ipvlan</td><td >Lighter, alternative L2/L3 integration</td></tr></tbody></table>
---
 

## 🔥 How Docker Uses iptables
 
Docker manipulates iptables on the host to handle:
 

*   Port mappings (`-p 8080:80`)
     
*   NAT for outgoing container traffic
     
*   Forwarding rules
     
*   Isolation rules
     

**Tables touched:**
 

*   `nat`
     
*   `filter`
     

---
 

## 🟦 Important iptables Chains Created by Docker
 <table><tbody><tr><th >Chain</th><th >Purpose</th></tr><tr><td >DOCKER</td><td >NAT rules for port forwarding</td></tr><tr><td >DOCKER-USER</td><td >User-defined firewall rules before Docker rules</td></tr><tr><td >DOCKER-ISOLATION-STAGE-1</td><td >Bridge/network isolation</td></tr><tr><td >DOCKER-ISOLATION-STAGE-2</td><td >Bridge/network isolation stage 2</td></tr></tbody></table>
---
 

## ⭐ Packet Flow When Using `-p 8000:8000`
 
**Assume:**
 

*   Host IP: `192.168.1.10`
     
*   Container IP: `172.17.0.2`
     
*   Container listens on port `8000`
     
*   Client sends: `http://192.168.1.10:8000`
     

**Steps:**
 

1.  **Packet arrives at host NIC**
     
2.  **PREROUTING (NAT Table)**
     
    
        iptables -t nat -A PREROUTING -p tcp --dport 8000 -j DNAT --to-destination 172.17.0.2:8000
    
    Destination IP → `172.17.0.2:8000`
     
3.  **DOCKER Chain (NAT Table)** DNAT rules managed by Docker
     
4.  **FORWARD Chain (Filter Table)**
     
    
        iptables -A FORWARD -d 172.17.0.2 -p tcp --dport 8000 -j ACCEPT
    
5.  **Packet enters docker0 bridge** → Host → docker0 → veth pair → container eth0
     
6.  **POSTROUTING (SNAT / MASQUERADE)**
     
    
        iptables -t nat -A POSTROUTING -s 172.17.0.2 -j MASQUERADE
    
    Client sees response as `192.168.1.10`
     

---
 

## 🔷 Summary: Docker’s iptables Usage
 <table><tbody><tr><th >Table</th><th >Purpose</th></tr><tr><td >nat</td><td >DNAT (port forwarding), SNAT (masquerade)</td></tr><tr><td >filter</td><td >Allow forwarding to/from container</td></tr><tr><td >mangle</td><td >Rarely used</td></tr></tbody></table>
---
 

## 🟩 DOCKER-USER Chain (Firewall Rules)
 
Docker guarantees:
 

*   It will never modify this chain
     
*   Your rules always run before Docker's own rules
     

**Examples:**
 

1.  Block all external access:
     
    
        iptables -I DOCKER-USER -i eth0 -j DROP
    
2.  Allow traffic only from specific IP:
     
    
        iptables -I DOCKER-USER -s 10.0.0.100 -j ACCEPT
        iptables -A DOCKER-USER -j DROP
    
3.  Block one container from internet:
     
    
        iptables -I DOCKER-USER -s 172.17.0.5 -o eth0 -j DROP
    
4.  Rate-limit traffic:
     
    
        iptables -I DOCKER-USER -p tcp --dport 80 -m limit --limit 10/s -j ACCEPT
        iptables -A DOCKER-USER -j DROP
    

**Hierarchy:**
 

    FORWARD
       ↓
    DOCKER-USER  ← YOUR RULES RUN HERE
       ↓
    DOCKER-ISOLATION
       ↓
    DOCKER (Docker internal rules)
       ↓
    ACCEPT or DROP

---
 

## 📄 Final Notes
 

*   User-defined networks offer better isolation & DNS.
     
*   `docker0` is the default bridge for basic communication.
     
*   Docker depends heavily on iptables NAT and filter chains.
     
*   `DOCKER-USER` is the best place to write custom firewall rules.
     
*   Port mapping (`-p`) creates DNAT, Forwarding rules, and SNAT.