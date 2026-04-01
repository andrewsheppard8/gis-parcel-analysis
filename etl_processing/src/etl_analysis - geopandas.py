import geopandas as gpd
import pandas as pd
import os
import datetime
import logging

os.environ["PROJ_LIB"] = r"C:\Users\andre\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\Library\share\proj"
# --- PATHS ---
parcels_path = r"C:\Users\andre\Desktop\GIT Resources\gis-portfolio\etl_processing\data\raw\Parcels.shp"
output_folder = r"C:\Users\andre\Desktop\GIT Resources\gis-portfolio\etl_processing\data\output"
output_reports=os.path.join(output_folder,"reports")
output_shapefiles=os.path.join(output_folder,"shapefiles")
output_gbd=os.path.join(output_folder,"gdb")
os.makedirs(output_reports, exist_ok=True)
os.makedirs(output_shapefiles, exist_ok=True)
os.makedirs(output_gbd, exist_ok=True)

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# --- EXTRACT ---
parcels = gpd.read_file(parcels_path)

# --- INSPECT SCHEMA ---  
# print(parcels.columns.tolist())
# print(parcels.dtypes)
# Capture and export schema metadata to support ETL validation and downstream data integrity checks
schema_output=os.path.join(output_reports,"schema_report.csv")
parcels.dtypes.to_csv(schema_output)
print("Output schema report for audit")

# # --- TRANSFORM: DATA QUALITY FLAGS ---

# # Total count
total_parcels = len(parcels)

# # Missing geometry flag
missing_geom_mask = parcels['geometry'].isna()

# # Duplicate APN flag (ALL duplicates)
duplicate_mask = parcels.duplicated(subset=['APN'], keep=False) #if keep='first' will only list the duplicates, not the first instance, keep=False prints all duplicates

# Invalid APN (null or empty)
invalid_apn_mask = parcels['APN'].isna() | (parcels['APN'].str.strip() == "")

# Acreage field empty (this is a necessary field to populate)
invalid_acreage_mask = parcels['ACREAGE'] <= 0

# If date updated is older than one year
parcels['DATE_ADDED'] = pd.to_datetime(parcels['DATE_ADDED'], errors='coerce')
stale_days=365
date_threshold=datetime.datetime.now() - datetime.timedelta(days=stale_days)
date_mask=(parcels['DATE_ADDED'] < date_threshold) | (parcels['DATE_ADDED'].isna())
# print(f"Parcels older than 1 year: {date_mask.sum()}")

# Geometry validation
invalid_geom_mask = ~parcels.is_valid #invalid geometry
empty_geom_mask = parcels.geometry.is_empty #no geometry at all

# # Create issues DataFrame
issues_df = parcels[['APN']].copy()
issues_df['MISSING_GEOMETRY'] = missing_geom_mask
issues_df['DUPLICATE_APN'] = duplicate_mask
issues_df['OUT_OF_DATE'] = date_mask
issues_df['INVALID_APN'] = invalid_apn_mask
issues_df['INVALID_ACREAGE'] = invalid_acreage_mask
issues_df['INVALID_GEOMETRY'] = invalid_geom_mask
issues_df['EMPTY_GEOMETRY'] = empty_geom_mask

# # Keep only rows with at least one issue
issues_df = issues_df[
    (issues_df['MISSING_GEOMETRY']) | (issues_df['DUPLICATE_APN']) | (issues_df['OUT_OF_DATE']) | (issues_df['INVALID_APN']) |
    (issues_df['INVALID_ACREAGE']) | (issues_df['INVALID_GEOMETRY']) | (issues_df['EMPTY_GEOMETRY'])
]

# # Add issue count
issues_df['ISSUE_COUNT'] = (
    issues_df['MISSING_GEOMETRY'].astype(int) +
    issues_df['DUPLICATE_APN'].astype(int) +
    issues_df['OUT_OF_DATE'].astype(int) +
    issues_df['INVALID_APN'].astype(int) +
    issues_df['INVALID_ACREAGE'].astype(int) +
    issues_df['INVALID_GEOMETRY'].astype(int) +
    issues_df['EMPTY_GEOMETRY'].astype(int) 
)

# # Sort by worst records first
issues_df = issues_df.sort_values(by='ISSUE_COUNT', ascending=False)

# # --- LOAD: EXPORT DATA QUALITY TABLE ---
issues_output_path = os.path.join(output_reports, "data_quality_issues.csv")
issues_df.to_csv(issues_output_path, index=False)

print(f"Exported data quality issues → {issues_output_path}")

# # --- SUMMARY REPORT ---
missing_geom_count = missing_geom_mask.sum()
# duplicate_count = duplicate_mask.sum()
unique_duplicate_apns = parcels.loc[duplicate_mask, 'APN'].nunique()
ood_count=date_mask.sum()
invalid_apn_count=invalid_apn_mask.sum()
invalid_acreage_count=invalid_acreage_mask.sum()
invalid_geom_count=invalid_geom_mask.sum()
empty_geom_count=empty_geom_mask.sum()


summary_df = pd.DataFrame({
"Metric": [
    "Total Parcels",
    "Missing Geometry",
    "Unique Duplicate APNs",
    "Out of Date Parcel",
    "Invalid APNs",
    "Invalid Acreage",
    "Invalid Geometry",
    "Empty Geometry"
],
"Value": [
    total_parcels,
    missing_geom_count,
    unique_duplicate_apns,
    ood_count,
    invalid_apn_count,
    invalid_acreage_count,
    invalid_geom_count,
    empty_geom_count
]
})

summary_output_path = os.path.join(output_reports, "etl_summary_report.csv")
summary_df.to_csv(summary_output_path, index=False)

print(f"Exported summary report → {summary_output_path}")

# # --- LOG EXPORT ---
log_path = os.path.join(output_reports, "etl_log.txt")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("ETL process started")
logging.info(f"Total parcels: {total_parcels}")
logging.info(f"Missing geometry: {missing_geom_count}")
logging.info(f"Out of date parcels: {ood_count}")
logging.info(f"Invalid APNs: {invalid_apn_count}")
logging.info(f"Invalid Acreages: {invalid_acreage_count}")
logging.info(f"Invalid Geometry: {invalid_geom_count}")
logging.info(f"Empty Geometry: {empty_geom_count}")

# # --- EXPORT A DATASET THAT DOES NOT HAVE ANY OF THE ISSUES INDENTIFIED ---

clean_parcels = parcels[~(
    missing_geom_mask |
    duplicate_mask |
    invalid_apn_mask |
    date_mask |
    invalid_geom_mask |
    empty_geom_mask
)]

clean_output_path = os.path.join(output_shapefiles, "clean_parcels.shp")
clean_parcels.to_file(clean_output_path)
print("Output shapefile with only clean parcels")

# # --- EXPORT A DATASET WITH PARCELS OF ONLY ISSUES INDENTIFIED ---

clean_parcels = parcels[(
    missing_geom_mask |
    duplicate_mask |
    invalid_apn_mask |
    date_mask |
    invalid_geom_mask |
    empty_geom_mask
)]

clean_output_path = os.path.join(output_shapefiles, "dirty_parcels.shp")
clean_parcels.to_file(clean_output_path)
print("Output shapefile with only dirty parcels")