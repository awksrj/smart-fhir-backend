# SMART on FHIR Backend (Demo)

Project: Enhancing the SMART on FHIR Backend for Patient-Controlled Data Sharing

Organization: Data for the Common Good

Author: Olive Do

Program: Google Summer of Code 2026


This repository is a functional demo implementation for a simple SMART on FHIR backend, developed as part of a GSoC 2026 proposal.

The project demonstrates a simple end-to-end workflow:

- Retrieving data from multiple FHIR servers
- Transforming raw FHIR resources into normalized formats
- Serving application-ready data for a dashboard use case

---

## Setup

### 1. Start local HAPI FHIR server

```bash
docker run -p 8080:8080 hapiproject/hapi:latest
```

### 2. Seed the server with sample data

```bash
python seed_hapi.py
```

### 3. Run the backend

```bash
uvicorn main:app --reload
```

---

## Project Structure

```
api/                # API layer (FastAPI endpoints)
fhir_client/        # FHIR integration layer (client + adapters)
data_pipeline/      # Data transformation layer (normalization)
integrations/       # Data serving layer (plugins/use cases)
```

---

## Architecture Overview

```
API → FHIR Client → Data Pipeline → Integrations
```

- **API Layer (**``**)**\
  Entry point of the system. Handles HTTP requests and routes them to services.

- **FHIR Client (**``**)**\
  Responsible for fetching data from FHIR servers. Encapsulates server-specific logic.

- **Data Pipeline (**``**)**\
  Transforms raw FHIR resources into flattened and consistent structures.

- **Integrations (**``**)**\
  Builds application-specific outputs (dashboard data in this case) from normalized data.

---

## API Endpoints

### Retrieve Patients

```
GET /patients?server=hapi
```

### Retrieve Observations

```
GET /observations/{patient_id}?server=hapi
```

### Dashboard Data

```
GET /dashboard/patient_overview?server=hapi
```

---

## Example Workflow

### Step 1: Fetch data from FHIR server

```
GET /observations/123?server=hapi
```

### Step 2: Transform data

- Extract key fields such as `patient_id`, `value`, `unit`, and `date`
- Flatten nested FHIR structures into a consistent format

### Step 3: Serve dashboard data

```
GET /dashboard/patient_overview
```

Example response:

```json
{
  "dashboard": "patient_overview",
  "total_patients": 5,
  "total_observations": 10,
  "dataset": [
    {
      "patient_id": "anon_1234",
      "age": 34,
      "observation_type": "85354-9",
      "value": 120,
      "unit": "mmHg",
      "date": "2024-01-01"
    }
  ]
}
```


## Example Testing Flow

1. Start the backend and FHIR server
2. Call:
   ```
   GET /patients
   ```
3. Pick a `patient_id` from the response
4. Call:
   ```
   GET /observations/{patient_id}
   ```
5. Call:
   ```
   GET /dashboard/patient_overview
   ```
6. Verify:
   - Data is retrieved from the FHIR server
   - Data is transformed correctly
   - Dashboard output is structured and anonymized

---



