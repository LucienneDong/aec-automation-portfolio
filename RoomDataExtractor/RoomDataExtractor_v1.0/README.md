\# Room Data Extractor v1.0



Automated room schedule extraction and data pipeline for BIM/AEC portfolio



---



\## Workflow Diagram



```mermaid

<diagram here>
flowchart LR

	A\[Revit Healthcare Project Model] --> B(Dynamo Extract Room Data)

	B --> C\[room\_data\_raw\_dynamo\_export\_sample.csv]

	C --> D(Python Data Validation \& Cleaning)

	D --> E\[room\_schedule\_cleaned\_sample\_v2.0.csv]

	D --> F\[room\_schedule\_issue\_repo\_sample\_v1.1.1.csv]



### png Diagram:

!\[Room Data Extractor Workflow](./assets/workflow\_diagram.png)


---





\## Folder Contents



\### Includes: 



&nbsp;- \*\*Dynamo extraction script\*\*

&nbsp;- \*\*Python cleanup pipeline\*\*

&nbsp;- Sample datasets for reproducibility



---



\## Sample Data



\*\*Input Samples:\*\*

./data/raw/room\_data\_raw\_dynamo\_export\_sample.csv

./data/raw/room\_data\_raw\_revit\_export\_sample.csv



\*\*Clean Output:\*\*

./data/clean/room\_data\_cleaned\_sample\_v1.0.csv



---



\## How to Run



```bash

python ./scripts/room\_extractor\_v1.0.py



---



\## Portfolio Notes



Built by Lucienne (Huichao) Dong - Architectural Designer transitioning into AEC data and emerging tech workflows.





Room Data Extractor v1.0 workflow supports both schedule-based and Dynamo-based extraction, depending on project needs.



Workflow for 2 options of room data extract/clean/validation

1. Revit Room Schedule -- export .csv file -- python clean \& validation -- excel review -- manually fix in revit
2. Revit Dynamo room extraction -- export .csv file -- python clean \& validation -- excel review -- dynamo write back into revit



option 1 works well under circumstances:

* one-off extraction
* stable schedule
* small teams working on the model



option 2 works better under circumstances:

* multiple data clean needed for different project/phases
* auto-detect: not placed rooms/phase mismatches
* avoid repetitive filter setup \& data cleaning process
* automatically write back cleaned up data



\## Why Dynamo Was(and Was Not) Used



For v1.0, room data was exported via native Revit schedules for reliability and ease of review. Dynamo-based extraction is included as an alternative automated pipeline for larger or repeated workflows.



For room data clean script, v1.0 focuses on cleanup data showing "Not Placed"

