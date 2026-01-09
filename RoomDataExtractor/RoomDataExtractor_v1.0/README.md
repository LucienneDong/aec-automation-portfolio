# Room Data Extractor v1.0



Automated room schedule extraction and data pipeline for BIM/AEC portfolio



---



## Workflow Diagram

### PNG Version

![Room Data Extractor Workflow](./assets/workflow_diagram.png)

### Mermaid Version

```mermaid
flowchart LR

	A[Revit Healthcare Project Model] --> B(Dynamo Extract Room Data)
	B --> C[room_data_raw_dynamo_export_sample.csv]
	C --> D(Python Data Validation & Cleaning)
	D --> E[room_schedule_cleaned_sample_v2.0.csv]
	D --> F[room_schedule_issue_repo_sample_v1.1.1.csv]
```


---


## Folder Contents


### Includes: 

 - **Dynamo extraction script**
 - **Python cleanup pipeline**
 - **Sample datasets for reproducibility**


---


## Sample Data


**Input Samples:**

./data/raw/room_data_raw_dynamo_export_sample.csv

./data/raw/room_data_raw_revit_export_sample.csv



**Clean Output:**

./data/clean/room_data_cleaned_sample_v1.0.csv



---



## How to Run



```bash

python ./scripts/room_extractor_v1.0.py

```


---


## Portfolio Notes



Built by Lucienne (Huichao) Dong - Architectural Designer transitioning into AEC data and emerging tech workflows.

