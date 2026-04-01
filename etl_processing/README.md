# Parcel QA/QC ETL



## Project Title

Parcel QA/QC ETL – Data Validation, Reporting, and Dataset Generation



### Description

This project demonstrates \*\*end-to-end GIS data processing and QA/QC\*\* for parcel datasets. It includes two Python workflows: one using \*\*ArcPy\*\* and one using \*\*GeoPandas\*\*, providing flexible approaches depending on the environment. 



Key steps include:



\- Load and inspect parcel shapefiles

\- Validate geometry and attribute data (APN, acreage, date fields)

\- Flag parcels with data quality issues:

&#x20; - Missing or empty geometry

&#x20; - Duplicate APNs

&#x20; - Invalid or missing APNs

&#x20; - Invalid acreage

&#x20; - Parcels out-of-date based on `DATE\_ADDED`

\- Aggregate issue counts per parcel

\- Export detailed CSV reports and summary metrics

\- Generate \*\*clean\*\* (no issues) and \*\*dirty\*\* (only issues) datasets

\- Optionally export data to a \*\*File Geodatabase\*\* with spatial indexing (ArcPy workflow)

\- Maintain ETL log files for audit and reproducibility



This workflow demonstrates \*\*Python scripting for GIS ETL\*\*, spatial data validation, and automated reporting.



### Technologies \& Libraries

\- Python 3.x – Core scripting language for ETL and GIS processing

\- pandas – Data manipulation, field calculations, and reporting

\- geopandas – Spatial data handling, geometry validation, and shapefile operations

\- arcpy – ArcGIS geodatabase management, feature class operations, and spatial indexing

\- os / glob – File path management and batch file handling

\- datetime – Date calculations for data validation

\- logging – Automated ETL process logging



### Features

###### Data Processing

\- Validates parcel geometries and attributes

\- Flags duplicates, invalid fields, and outdated parcels

\- Aggregates issue counts for each parcel

\- Converts string date fields to proper Date fields for GDB export



###### Outputs

\- CSV: `schema\_report.csv`, `data\_quality\_issues.csv`, `etl\_summary\_report.csv`

\- Shapefiles: `clean\_parcels.shp`, `dirty\_parcels.shp`

\- File Geodatabase (ArcPy workflow): `original\_parcels`, `clean\_parcels`, `dirty\_parcels` with spatial indexes

\- Log file: `etl\_log.txt`



###### CRS Handling

\- Ensures all parcel geometries are valid

\- Compatible with different CRS for analysis and export



### File Structure

project-root/

│

├─ etl\_processing/

&#x20;   ├─ README.md                        # Project overview, usage, and notes

&#x20;   ├─ etl\_analysis - arcpy.py          # Full ETL workflow using ArcPy + GDB

&#x20;   ├─ etl\_analysis - geopandas.py      # Full ETL workflow using GeoPandas + CSV/Shapefiles

&#x20;   │

&#x20;   ├─ data/

&#x20;       ├─ raw/                         # Original shapefiles

&#x20;       │   └─ Parcels.shp

&#x20;       │

&#x20;       └─ output/                      # Generated files

&#x20;           ├─ reports/

&#x20;           │   ├─ schema\_report.csv

&#x20;           │   ├─ data\_quality\_issues.csv

&#x20;           │   ├─ etl\_summary\_report.csv

&#x20;           │   └─ etl\_log.txt

&#x20;           │

&#x20;           ├─ shapefiles/

&#x20;           │   ├─ clean\_parcels.shp

&#x20;           │   └─ dirty\_parcels.shp

&#x20;           │

&#x20;           └─ gdb/

&#x20;               └─ etl\_output.gdb



### Notes/Future Improvements

Make input/output paths and thresholds configurable via a settings file

Add extended validation rules, e.g., zoning, building footprints, or multi-class parcels

Implement unit tests for QA/QC functions and data integrity checks

Optimize performance for large datasets using vectorized operations or batch processing

Add interactive visualizations or dashboards to highlight data quality issues



### Author

Andrew Sheppard – GIS Solution Engineer

GitHub: https://github.com/andrewsheppard8

Email: andrewsheppard8@gmail.com

