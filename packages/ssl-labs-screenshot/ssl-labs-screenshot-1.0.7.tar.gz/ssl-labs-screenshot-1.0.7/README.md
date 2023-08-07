SSL Labs Screenshot is a Python script that captures a trimmed screenshot of the SSL Labs report for a given domain.

## Requirements
- Python 3.x
- Chrome browser (version 89 or later)
- ChromeDriver

## Installation
1. Install SSL Labs Screenshot using pip:
   ```
   pip install ssl-labs-screenshot
   ```
3. Download the latest version of ChromeDriver from the following link: https://sites.google.com/chromium.org/driver/downloads
4. Extract the contents of the downloaded ZIP file to a directory on your system.
5. Either move the ChromeDriver executable to a directory already in your system's `PATH` environment variable or add the path to the directory where you extracted the ChromeDriver executable to the `PATH` variable.

## Usage
Run the script with the following command:
```
ssl-labs-screenshot domain.com
```
Replace domain.com with the domain you want to test. The script will open a headless Chrome browser and load the SSL Labs report for the domain. It will capture a temporary screenshot of the report and save it as a PNG file in the same directory as the script, with the name domain_report_tmp.png. The script will delete the temporary screenshot after the trimmed image is created with the name domain_report.png

## Limitations
The script only captures the first server's report for domains with multiple servers.