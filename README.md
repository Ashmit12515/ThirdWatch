# ThirdWatch

> AI-powered Third-Party Risk Management (TPRM) platform for vendor security assessments, evidence validation, and explainable risk scoring.

## Overview

ThirdWatch is an AI-native Third-Party Risk Management (TPRM) platform that helps security and compliance teams evaluate vendor risk through explainable assessments, evidence collection, and automated control validation.

Unlike traditional questionnaire-based assessments that rely heavily on manual reviews, ThirdWatch combines deterministic risk scoring with evidence-driven validation to produce transparent, auditable vendor risk decisions.

The platform is being developed as a modern GRC solution with support for local Large Language Models (LLMs), document intelligence, and explainable AI.

---

## Features

### Vendor Assessment

- Create vendor security assessments
- Assess vendor criticality
- Evaluate security posture
- Generate explainable risk scores
- Automatically assign vendor risk tiers

### Explainable Risk Scoring

Risk scores are generated using transparent scoring logic based on factors such as:

- Personally Identifiable Information (PII)
- SOC 2 availability
- ISO 27001 certification
- Multi-Factor Authentication (MFA)
- Encryption at Rest
- Incident Response Planning
- Vendor Criticality
- Third-party Exposure

Every assessment includes human-readable reasoning explaining why a vendor received its score.

---

### Evidence Management

- Upload vendor evidence (.txt and PDF)
- Store evidence for audit purposes
- Maintain evidence history
- Associate evidence with vendors

---

### Control Extraction

Extract security controls from uploaded evidence.

Current implementation supports deterministic control detection for:

- SOC 2
- ISO 27001
- MFA
- Encryption at Rest
- Incident Response

---

### Evidence-Based Risk Recalculation

After controls are verified through uploaded evidence, ThirdWatch recalculates vendor risk automatically.

Example workflow:

Vendor Assessment

↓

Upload SOC 2 Report

↓

Extract Security Controls

↓

Validate Controls

↓

Recalculate Vendor Risk

↓

Generate Updated Risk Score

---

### Assessment History

Every assessment is preserved.

Instead of overwriting previous assessments, ThirdWatch stores historical assessments to provide a complete audit trail.

---

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

### Frontend

- React
- TypeScript
- Vite

### Current AI Components

- Rule-based evidence extraction

### Planned AI Stack

- LangChain
- LangGraph
- LM Studio
- Local LLMs
- RAG
- Vector Search

---

## Project Structure

```
backend/
    app/
        api/
        models/
        schemas/
        services/

frontend/
    src/
```

---

## Current Workflow

```
Vendor

↓

Risk Assessment

↓

Evidence Upload

↓

Control Extraction

↓

Evidence Validation

↓

Risk Recalculation

↓

Audit History
```

---

## Roadmap

- [x] Vendor assessment engine
- [x] Explainable risk scoring
- [x] React dashboard
- [x] Evidence upload
- [x] Evidence persistence
- [x] Control extraction
- [x] Evidence-based risk recalculation
- [x] Assessment history

### In Progress

- [ ] LangChain integration
- [ ] Local LLM support (LM Studio)

### Planned

- [ ] AI-powered control extraction
- [ ] PDF document intelligence
- [ ] Table extraction from SOC 2 reports
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] LangGraph workflow orchestration
- [ ] Continuous vendor monitoring
- [ ] Security framework mapping (SOC 2, ISO 27001, NIST)
- [ ] Executive risk dashboard
- [ ] Analyst review workflow

---

## Why ThirdWatch?

Traditional vendor assessments are often:

- Manual
- Time-consuming
- Questionnaire-driven
- Difficult to audit
- Hard to explain

ThirdWatch aims to combine deterministic risk models with AI-assisted evidence analysis to create transparent, explainable, and auditable vendor risk decisions.

---

