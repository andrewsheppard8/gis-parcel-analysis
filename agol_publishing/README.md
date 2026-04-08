# AGOL Feature Service Publisher



## Project Title

Publish Feature Class to ArcGIS Online – GIS Data Management



### Description

This Python script automates publishing a feature class from an ArcGIS Pro project to ArcGIS Online as a hosted feature layer.



It handles tasks that are typically manual and time-consuming, including clearing layers, deleting existing services, generating a timestamped service name, creating a Web Layer Sharing Draft, staging the service, and uploading to ArcGIS Online.



This version of the tool is interactive, designed to run within ArcGIS Pro. A fully headless version for automated batch publishing is planned for future development.



### Features

Clears existing layers from a map before publishing.

Deletes any existing AGOL services or service definitions with the same name.

Creates timestamped service names to avoid conflicts.

Generates Web Layer Sharing Drafts and stages them automatically.

Uploads services to ArcGIS Online with logging and error handling.

Logs progress and errors to a timestamped log file in the scratch folder.



### Usage

Edit the run block at the bottom of the script with your project paths and service details





### Notes/Future Improvements

Fully headless mode for automated batch publishing.

Configurable portal URL or hosting server.

Optionally store logs in a permanent folder outside scratch.

Robust retry logic for AGOL API operations.

Notifications via email or Teams when publishing completes.



### Author

Andrew Sheppard – GIS Developer

Email: andrewsheppard8@gmail.com

