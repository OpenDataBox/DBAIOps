# DBAIOps
This is the code repository of **DBAIOps**, a novel database operation and maintenance (O&M) system that integrates expert experience to achieve practical anomaly detection, diagnosis, and recovery. Specifically, it conducts database O&M based on the following techniques:

- **(1) O&M Maintenance Graph:** a graph-based experience model to represent various possible diagnosis paths within O&M experience;
- **(2) Correlation-Aware Anomaly Model:** capture implicit correlations across metrics and real-world anomalies and initialize knowledge graph exploration during online diagnosis;
- **(3) O&M Path Exploration:** a two-stage graph evolution mechanism that adaptively explores possible diagnosis paths for the input anomaly;
- **(4) Reasoning LLM Based Diagnosis:** prompt reasoning LLM to reason over these diagnosis paths and generate diagnosis reports with specific recovery solutions.

Evaluation over four mainstream database systems demonstrates that DBAIOps outperforms state-of-the-art baselines, **47.85%** higher in diagnosis accuracy and report interpretability. The structure is as follows:

* [DBAIOps Platform Deployment Guide](#dbaiops-platform-deployment-guide)

    * [1. System Preparation](#1-system-preparation)
        * [1.1 Hardware Requirements](#11-hardware-requirements)
        * [1.2 Firewall Port Configuration](#12-firewall-port-configuration)
        * [1.3 Upload Installation Media](#13-upload-installation-media)
        
    * [2. Single-Node Installation](#2-single-node-installation)
        * [2.1 Configure YUM](#21-configure-yum)
        
        * [2.2 Installation](#22-installation)
        
        * [2.3 Service Management Commands](#23-service-management-commands)
        
        * [2.4 Accessing DBAIOps Platform](#24-accessing-dbaiops-platform)        
        

* [Case Study of Oracle Diagnosis Report](#case-study-of-oracle-diagnosis-report)

Note that the full content about the case study of the diagnosis reports can be found at the [Appedinx_Diagnosis_Report](https://anonymous.4open.science/r/DBAIOps-80F8/Appedinx_Diagnosis_Report.pdf).

---

# DBAIOps Platform Deployment Guide

```
├── bin                         # DBAIOps installation and deployment scripts
├── webserver                   # Frontend webserver configuration
├── fstaskpkg                   # Task platform configurations
├── knowl                       # Knowledge graph base scripts
├── colscript                   # Python3 collection scripts (health & cib metrics)
├── pgconf                      # PostgreSQL initialization config for DSmart metadata
└── phantomjsconf               # Frontend webserver JS plugin configurations
```

## 1. System Preparation

### 1.1 Hardware Requirements

#### Minimum Configuration (for <20 database instances)
| Purpose | Hardware Specs | Supported OS | IP Address | Qty | Notes |
|---------|---------------|--------------|------------|-----|-------|
| Database, Task Platform, Web Server | 16C/32GB/600GB | RedHat 7.2+ (YUM configured)<br>CentOS 7.2+ (YUM configured)<br>SUSE 12 SP4 (zypper configured)<br>Kylin V10 SP1/SP2/SP3 | 1 | 1 | No restrictions |

#### Recommended Configuration (for >60 database instances)
| Purpose | Hardware Specs | Supported OS | IP Address | Qty | Notes |
|---------|---------------|--------------|------------|-----|-------|
| Database Server | 16C/64GB/1TB | RedHat 7.2+<br>CentOS 7.2+<br>SUSE 12 SP4 | 3 | 1 | Physical server required |
| Web Server & Task Platform | 16C/64GB/300GB | RedHat 7.2+<br>CentOS 7.2+<br>SUSE 12 SP4 | 3 | 3 | No restrictions |

**Notes:**
- DBAIOps database server can be installed in any directory (only disk space required);
- Distributed installation requires root SSH passwordless login between DBAIOps servers during setup (can be disabled post-installation). Single-node installation doesn't require this.

### 1.2 Firewall Port Configuration

**Between Ops machine and DBAIOps servers:**
- Required ports: 22, 18081, 18090, 28080

**Between DBAIOps servers and monitored databases:**
- Oracle: 11521, 1521
- MySQL: 3306
- PostgreSQL: 5432
- DM8: 5236

### 1.3 Upload Installation Media
Upload installation package to DBAIOps server

---

## 2. Single-Node Installation

### 2.1 Configure YUM
Configure YUM repo:
```
mount /dev/sr0 /mnt
vi /etc/yum.repos.d/local.repo
```

Install dependencies:
```
cd /usr/software/bin
./DBAIOps-system-package.sh -install
```

### 2.2 Installation

#### Step 1: Execute Installation
```bash
cd /usr/software/bin
./DBAIOps.sh -install
```

#### Step 2: Select Deployment Type
Select deployment type [Default is single-node]:
- Single-node deployment
- Distributed deployment (requires manual role.cfg configuration)

#### Step 3: OS Selection

Choose OS type [Select according to your OS]:
- RedHat
- CentOS

#### Step 4: Installation Progress
- Installation typically takes 1-1.5 hours depending on system performance
- RPM packages will be automatically installed

#### Step 5: Post-Installation
After successful installation, restart DBAIOps services:
```bash
/usr/software/bin/DBAIOps.sh -restart
```

### 2.3 Service Management Commands

| Command | Description |
|---------|-------------|
| `./DBAIOps.sh -start` | Start all DBAIOps services |
| `./DBAIOps.sh -stop` | Stop all DBAIOps services |
| `./DBAIOps.sh -status` | Check service status |
| `./DBAIOps.sh -restart` | Restart all services |

### 2.4 Accessing DBAIOps Platform

**Web Interface:**
```
http://<SERVER_IP>:18081/DBAIOps
```

**Default Credentials:**
```
Username: admin
Password: admin@123
```

**Security Notice:**
- Change the default password immediately after first login;
- Recommended to use a strong password following your organization's security policy;
- For production environments, consider implementing additional security measures (IP restrictions, 2FA, etc.).

# Case Study of Oracle Diagnosis Report

**Anomaly:** *LOG SYNCHRONIZATION DELAY*, which detects slowdowns caused by log-writing operations. When a transaction commits or rolls back, forcing a session to wait for the log writer to flush redo logs, the system can degrade significantly if I/O capacity is insufficient. 

**Abnormal Metrics List:**

| Metric ID | Metric Name                             | Min     | Max     | Avg    |
|-----------|-----------------------------------------|---------|---------|--------|
| 2184301   | log file sync average wait time        | 1.08 ms | 15.2 ms | 6.0 ms |
| 2184305   | log file parallel write average wait time | 0.78 ms | 7.09 ms | 3.0 ms |
| 000014    | Mem unavailable                         | 72.82   | 73.07   | 73.0   |

**Root Cause:**

**(1) Insufficient I/O Performance of REDO Log Storage:**  
- Evidence Chains:  
  - Metric 2184301 (*log file sync*): max = 15.2 ms, avg = 6.0 ms (abnormal)  
  - Metric 2184305 (*log file parallel write*): max = 7.09 ms, avg = 3.0 ms (abnormal)  
- Anomaly Analysis:  
  - According to the formula: log_file_sync / log_file_parallel_write = 6.0 / 3.0 = 2  
  - Ratio in range (1.5, 2] ⇒ Storage I/O performance is a primary factor  

**(2) Intermittent I/O Pressure Spikes During Log Writing:**  
- Evidence Chains:  
  - At 06:00, log file sync spiked to 15.2 ms (vs. hourly avg 4.54 ms)  
  - log file parallel write peaked at 7.09 ms (high for mechanical disks)  
  - OS I/O latency = 0.47 ms (normal)  
- Anomaly Analysis:  
  - Storage likely under transient load  

---

### 💬 DBA Feedback
> ✅ The predefined hypothesis of the experiment is that the bottleneck lies in I/O storage.  
> ✅ Both root causes align with this hypothesis (**first evaluation criterion** satisfied)  
>   
> ✅ Evidence chains are logically consistent with Oracle/OS theory (**second criterion**)  
>   
> ✅ All data comes from actual experiments with **no hallucinations** (**third criterion**)  
>   
> 🎯 **Final Accuracy Assessment: 100%**
