# DBAIOps
This repository now tracks the current **DBAIOps** workspace after the project was refactored from a server-side O&M deployment bundle to a browser-extension-based database knowledge assistant. The active worktree now carries the browser-extension-based DBAIOps assistant while keeping the repository history.

Current DBAIOps focuses on the following capabilities:

- **Intelligent database knowledge Q&A:** retrieve answers for mainstream and domestic database engines.
- **AWR report analysis:** parse Oracle AWR reports and generate structured diagnosis results.
- **Inspection analysis:** review inspection tasks, history records, and issue summaries.
- **SQL optimization assistance:** support targeted optimization workflows and report desensitization.
- **Configurable model access:** connect external knowledge services and third-party model providers.

The structure is as follows:

* [DBAIOps Browser Extension Guide](#dbaiops-browser-extension-guide)
    * [1. Repository Overview](#1-repository-overview)
        * [1.1 Core Capabilities](#11-core-capabilities)
        * [1.2 Repository Layout](#12-repository-layout)
    * [2. Local Loading and Basic Configuration](#2-local-loading-and-basic-configuration)
        * [2.1 Load the Unpacked Extension](#21-load-the-unpacked-extension)
        * [2.2 Registration and Knowledge Service Configuration](#22-registration-and-knowledge-service-configuration)
        * [2.3 Model Provider Configuration](#23-model-provider-configuration)
    * [3. Analysis Features](#3-analysis-features)
        * [3.1 AWR Report Analysis](#31-awr-report-analysis)
        * [3.2 Inspection Analysis](#32-inspection-analysis)
        * [3.3 SQL Optimization and Desensitization](#33-sql-optimization-and-desensitization)
    * [4. Preserved Assets and Operational Notes](#4-preserved-assets-and-operational-notes)

---

# DBAIOps Browser Extension Guide

```
├── DBAIOps_v1.1.1               # Unpacked browser extension source
├── DBAIOps_v1.1.1.zip           # Preserved release archive
├── assets                      # Screenshots, demo video, and documentation media
├── icons                       # Repository-level branding assets
├── README.md                   # English usage guide in DBAIOps style
├── README_ZH.md                # Chinese usage guide in DBAIOps style
└── LICENSE                     # License file from the extension project
```

## 1. Repository Overview

### 1.1 Core Capabilities

| Module | Summary |
|--------|---------|
| Knowledge Q&A | Query database knowledge bases for SQL syntax, troubleshooting, tuning, and best practices |
| AWR Analysis | Upload Oracle AWR HTML reports and generate structured AI-assisted analysis |
| Inspection Analysis | Review database inspection tasks and historical analysis records |
| SQL Optimization | Submit SQL optimization tasks and inspect returned recommendations |
| Service Integration | Configure knowledge-service endpoints, API keys, and model providers |

### 1.2 Repository Layout

**Extension Entry Folder:**
```
/data/wei/program/DBAIOps/DBAIOps_v1.1.1
```

**Key Configuration Files:**
- `DBAIOps_v1.1.1/manifest.json`
- `DBAIOps_v1.1.1/config/registration.json`
- `DBAIOps_v1.1.1/config/knowledge_service.json`

**Default Service Endpoints:**
- Registration service: configured in `DBAIOps_v1.1.1/config/registration.json`
- Knowledge service: configured in `DBAIOps_v1.1.1/config/knowledge_service.json`

---

## 2. Local Loading and Basic Configuration

### 2.1 Load the Unpacked Extension

1. Open the browser extension management page.
2. Enable developer mode.
3. Click **Load unpacked**.
4. Select the directory below:
```bash
/data/wei/program/DBAIOps/DBAIOps_v1.1.1
```
5. Confirm that the extension icon and popup page can be opened normally.

### 2.2 Registration and Knowledge Service Configuration

#### Step 1: User Registration
Open the settings page and fill in user information. The extension uses `config/registration.json` as the default registration-service template and can persist user-specific updates in browser storage.

#### Step 2: Knowledge Service
Enter the knowledge-service configuration page and set the API key and service URL. The default template comes from:
```bash
DBAIOps_v1.1.1/config/knowledge_service.json
```

#### Step 3: Configuration Validation
After saving the configuration, verify that:
- the target knowledge base can be selected;
- the configured service endpoint is reachable;
- the popup page can submit and receive messages.

### 2.3 Model Provider Configuration

DBAIOps currently relies on browser-side configuration for model providers.

Typical workflow:
1. Open **Settings** -> **Models & Service Providers**.
2. Add a provider such as `ollama`, `deepseek`, or another OpenAI-compatible endpoint.
3. Fill in the API base URL and API key if required.
4. Run the built-in test action and save the selected models.

**Local Ollama Example:**
```bash
http://localhost:11434/v1
```

---

## 3. Analysis Features

### 3.1 AWR Report Analysis

DBAIOps provides an Oracle AWR analysis workflow inside the extension UI.

**Supported Input:**
- Oracle single-instance AWR HTML reports
- RAC AWR reports generated through `awrrpt.sql` or `awrrpti.sql`

**Current Notes:**
- AWR comparison reports generated through `awrddrpi.sql` are not the primary target.
- Global reports generated through `awrgrpt.sql` should be validated before production use.

**Typical Steps:**
1. Open the AWR analysis panel.
2. Fill in the issue summary and receiving email if required.
3. Upload the AWR report.
4. Select the report language.
5. Submit the task and inspect the history list after processing.

### 3.2 Inspection Analysis

The extension also preserves the database inspection analysis workflow. It is intended for operational review scenarios where users need a summarized status view, historical task lookup, and issue follow-up.

Common use cases include:
- reviewing periodic inspection tasks;
- checking generated summaries and abnormal findings;
- rerunning historical records when model or service settings change.

### 3.3 SQL Optimization and Desensitization

DBAIOps keeps the SQL optimization and report-desensitization related modules from the extension project.

These modules are intended for:
- submitting SQL statements for optimization assistance;
- reducing exposure of sensitive SQL text in uploaded reports;
- preserving a browser-based workflow for database engineers and DBAs.

---

## 4. Preserved Assets and Operational Notes

**Preserved Assets:**
- `DBAIOps_v1.1.1.zip` is intentionally kept as the packaged release artifact.
- `assets/DBAIOps_AWR_Analysis_Demo.mp4` is intentionally kept as the demo video.
- `assets/DBAIOps_WeChat_Assistant_QR.jpg` and `assets/DBAIOps_Community_QR_Code.png` are intentionally kept as community support QR assets.
- the screenshots under `assets/` are intentionally kept for usage documentation.

**Repository Positioning:**
- The repository history remains under **DBAIOps**.
- The active browser-extension assets remain branded as **DBAIOps**.
- This README is intentionally written in the older DBAIOps documentation style instead of the upstream marketing-style README.

**Operational Note:**
- For local verification, load `DBAIOps_v1.1.1` as an unpacked extension instead of trying to run the old DBAIOps deployment scripts.
- If the browser configuration was modified previously, reset the extension settings before validating a new endpoint.
