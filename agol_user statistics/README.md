# AGOL User Audit Tool (ArcGIS API for Python)



A lightweight auditing tool for inspecting ArcGIS Online (AGOL) user content using the ArcGIS API for Python.



This project demonstrates multiple execution patterns—from simple scripts to automation-ready CLI workflows—while providing useful insights into a user's AGOL content.



## 🔍 What This Tool Does



###### Connects to ArcGIS Online



###### Retrieves all items owned by a user



###### Summarizes:

Total item count

Storage usage (approximate)

Item type breakdown



###### Identifies:

Largest items

Recently modified items

Stale items (not modified in 1+ year)

Items missing descriptions

Exports results to a timestamped .txt report



## 🧩 Execution Patterns



This repo intentionally includes three different approaches to show flexibility and real-world usage:



###### 1\. Hardcoded Script

Credentials stored directly in script

Best for quick testing and learning

Minimal setup



###### 2\. Config-Based Script

Credentials stored in a config.ini file

More secure and reusable

Suitable for repeatable workflows



Example config:



\[AGOL]

portal\_url = https://your-org.maps.arcgis.com

username = your\_username

password = your\_password



###### 3\. CLI (Command Line Interface)

Supports command-line arguments

Ideal for automation (Task Scheduler, pipelines)

Most flexible and scalable approach



Example usage:



python agol\_audit\_cli.py --summary-only





## 📄 Output



###### All scripts generate a timestamped report:



agol\_report\_YYYYMMDD\_HHMMSS.txt



###### Reports include:



Full inventory of items

Summary statistics

Data quality indicators (missing descriptions, stale items)

⚙️ Requirements

Python 3.x

ArcGIS API for Python



Install dependencies:



pip install -r requirements.txt



## 🚀 Why This Project Matters



###### This project demonstrates:



Multiple approaches to authentication and configuration

Scalable scripting patterns (hardcoded → config → CLI)

Practical AGOL content auditing

Automation-ready design



It reflects real-world GIS workflows where scripts evolve from quick utilities into maintainable, reusable tools.



## 🔮 Future Improvements



Organization-wide admin audit (all users)

CSV / Excel export

Credit usage estimation

Dashboard integration

Automated scheduling



## 👤 Author



Andrew Sheppard

GIS Developer | Solutions Engineer | Automation SpecialistGitHub: https://github.com/andrewsheppard8

Email: andrewsheppard8@gmail.com

