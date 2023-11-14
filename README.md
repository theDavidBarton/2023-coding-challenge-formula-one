# Test Automation Engineer (аіЅіⅿ) coding challenge - Formula One

A python script to parse and crawl Wikipedia for Formula One-related data using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) and [Requests](https://requests.readthedocs.io/en/latest/) libraries.


## Environment

Python version: Python 3.12.0

Tested against:
- Windows 10 ✅
- Ubuntu 20.04 ✅


## Install dependencies

```
pip install -r requirements.txt
```


## Run

Necessary files to run the script:
```
├── main.py
├── generate_stat.sh (for Linux)
├── generate_stat.bat (for Windows)
```

Run on terminal:
```
python main.py
```
It will also call `generate_stat.sh` or `generate_stat.bat` during execution based on the current platform.

Terminal output:
```
# David Barton (theDavidBarton@AOL.com) © 2023
# Test Automation Engineer coding challenge - Formula One

[init script...]
* teams being collected...
* drivers being collected (slower)...
* flag rules being collected...
* images being collected & downloaded (slower)...
* json file being created...
* stats & txt file being created...

#############################################
1. number of drivers in the championship: 20
2. number of engine suppliers: 4
3. number of images: 58
4. number of identified images: 25
5. number of not identified images: 33
6. size of all images: 746.638
7. average size of images: 12.873068965517241
8. highest resolution: 250x256
9. lowest resolution: 42x26
#############################################

"stat.txt created successfully (Windows)"
```

Files & folders created by the script:
```
├── data.json
├── stat.txt
└── flags
    ├── image files
    ├── ...
└── identified
    ├── image files
    ├── ...
└── not_identified
    ├── image files
    ├── ...
```


## GitHub Actions

The script can be also run with workflow dispatch (manual trigger) from GitHub Actions, the YAML is called "run-test". It runs on Ubuntu 20.04 and Microsoft Windows Server 2022 (10.0.20348 which resembles Windows 10 environment). 


## Disclaimer

The data collected by this script is based on the state of Wikipedia as of November 13, 2023. Please note that Wikipedia is edited by an open community, and the collected information may include factual mistakes or inconsistencies. Users are advised to verify information independently for the most accurate and reliable details.


## Resources

- Python Docs: https://docs.python.org/3/
- Requests: https://requests.readthedocs.io/en/latest/
- Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Using urllib.request to write an image (Stack Overflow): https://stackoverflow.com/a/65143739/12412595


## Author

David Barton (theDavidBarton@AOL.com) © 2023
