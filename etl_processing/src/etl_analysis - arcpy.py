import geopandas as gpd
import pandas as pd
import os
import datetime
import logging
import arcpy

# --- ENVIRONMENT SETUP ---
os.environ["PROJ_LIB"] = r"C:\Users\andre\AppData\Local\ESRI\conda\envs\arcgispro-py3-clone\Library\share\proj"

# --- PATHS ---
parcels_path = r"C:\Users\andre\Desktop\GIT Resources\gis-portfolio\etl_processing\data\raw\Parcels.shp"
output_folder = r"C:\Users\andre\Desktop\GIT Resources\gis-portfolio\etl_processing\data\output"

output_reports = os.path.join(output_folder, "reports")
output_gdb_folder = os.path.join(output_folder, "gdb")
gdb_name = "etl_output.gdb"
gdb_path = os.path.join(output_gdb_folder, gdb_name)

# Ensure folders exist
os.makedirs(output_reports, exist_ok=True)
os.makedirs(output_gdb_folder, exist_ok=True)

# --- LOGGING SETUP ---
log_path = os.path.join(output_reports, "etl_log.txt")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("ETL process started")

# --- EXTRACT ---
parcels = gpd.read_file(parcels_path)
total_parcels = len(parcels)

# --- SCHEMA REPORT ---
schema_output = os.path.join(output_reports, "schema_report.csv")
parcels.dtypes.to_csv(schema_output)
logging.info("Exported schema report")

# --- TRANSFORM: DATA QUALITY FLAGS ---
# Missing geometry
missing_geom_mask = parcels['geometry'].isna()
# Duplicate APN
duplicate_mask = parcels.duplicated(subset=['APN'], keep=False)
# Invalid APN
invalid_apn_mask = parcels['APN'].isna() | (parcels['APN'].str.strip() == "")
# Invalid acreage
invalid_acreage_mask = parcels['ACREAGE'] <= 0
# Out of date
parcels['DATE_ADDED'] = pd.to_datetime(parcels['DATE_ADDED'], errors='coerce')
stale_days = 365
date_threshold = datetime.datetime.now() - datetime.timedelta(days=stale_days)
date_mask = (parcels['DATE_ADDED'] < date_threshold) | (parcels['DATE_ADDED'].isna())
# Geometry validation
invalid_geom_mask = ~parcels.is_valid
empty_geom_mask = parcels.geometry.is_empty

# --- ISSUES DATAFRAME ---
issues_df = parcels[['APN']].copy()
issues_df['MISSING_GEOMETRY'] = missing_geom_mask
issues_df['DUPLICATE_APN'] = duplicate_mask
issues_df['OUT_OF_DATE'] = date_mask
issues_df['INVALID_APN'] = invalid_apn_mask
issues_df['INVALID_ACREAGE'] = invalid_acreage_mask
issues_df['INVALID_GEOMETRY'] = invalid_geom_mask
issues_df['EMPTY_GEOMETRY'] = empty_geom_mask

# Keep only rows with at least one issue
issues_df = issues_df[
    (missing_geom_mask) | (duplicate_mask) | (date_mask) | (invalid_apn_mask) |
    (invalid_acreage_mask) | (invalid_geom_mask) | (empty_geom_mask)
]

# Issue count
issues_df['ISSUE_COUNT'] = (
    issues_df['MISSING_GEOMETRY'].astype(int) +
    issues_df['DUPLICATE_APN'].astype(int) +
    issues_df['OUT_OF_DATE'].astype(int) +
    issues_df['INVALID_APN'].astype(int) +
    issues_df['INVALID_ACREAGE'].astype(int) +
    issues_df['INVALID_GEOMETRY'].astype(int) +
    issues_df['EMPTY_GEOMETRY'].astype(int)
)

issues_df = issues_df.sort_values(by='ISSUE_COUNT', ascending=False)

# --- EXPORT REPORTS ---
issues_output_path = os.path.join(output_reports, "data_quality_issues.csv")
issues_df.to_csv(issues_output_path, index=False)
logging.info(f"Exported data quality issues → {issues_output_path}")

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
        missing_geom_mask.sum(),
        parcels.loc[duplicate_mask, 'APN'].nunique(),
        date_mask.sum(),
        invalid_apn_mask.sum(),
        invalid_acreage_mask.sum(),
        invalid_geom_mask.sum(),
        empty_geom_mask.sum()
    ]
})
summary_output_path = os.path.join(output_reports, "etl_summary_report.csv")
summary_df.to_csv(summary_output_path, index=False)
logging.info(f"Exported summary report → {summary_output_path}")

# --- CREATE CLEAN AND DIRTY DATASETS ---
clean_parcels = parcels[~(
    missing_geom_mask |
    duplicate_mask |
    date_mask |
    invalid_apn_mask |
    invalid_acreage_mask |
    invalid_geom_mask |
    empty_geom_mask
)]

dirty_parcels = parcels[
    missing_geom_mask |
    duplicate_mask |
    date_mask |
    invalid_apn_mask |
    invalid_acreage_mask |
    invalid_geom_mask |
    empty_geom_mask
]

# --- CREATE FILE GEODATABASE ---
if not arcpy.Exists(gdb_path):
    arcpy.CreateFileGDB_management(output_gdb_folder, gdb_name)
    logging.info(f"Created geodatabase → {gdb_path}")

# --- EXPORT TO GDB WITH SPATIAL INDEX ---
# Original parcels
arcpy.conversion.FeatureClassToFeatureClass(parcels_path, gdb_path, "original_parcels")
arcpy.AddSpatialIndex_management(os.path.join(gdb_path, "original_parcels"))
logging.info("Exported original parcels to GDB and added spatial index")

# Clean parcels
temp_clean_shp = os.path.join(output_folder, "temp_clean.shp")
clean_parcels.to_file(temp_clean_shp)
arcpy.conversion.FeatureClassToFeatureClass(temp_clean_shp, gdb_path, "clean_parcels")
arcpy.AddSpatialIndex_management(os.path.join(gdb_path, "clean_parcels"))
os.remove(temp_clean_shp)
logging.info("Exported clean parcels to GDB and added spatial index")

# Dirty parcels
temp_dirty_shp = os.path.join(output_folder, "temp_dirty.shp")
dirty_parcels.to_file(temp_dirty_shp)
arcpy.conversion.FeatureClassToFeatureClass(temp_dirty_shp, gdb_path, "dirty_parcels")
arcpy.AddSpatialIndex_management(os.path.join(gdb_path, "dirty_parcels"))
os.remove(temp_dirty_shp)
logging.info("Exported dirty parcels to GDB and added spatial index")

print("ETL complete. Original, clean, and dirty parcels are in the geodatabase.")