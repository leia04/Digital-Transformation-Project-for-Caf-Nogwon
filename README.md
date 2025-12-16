# Digital Transformation Project for Cafe Nogwon – Data Collection Automation (Crawling)

▶️ Demo Video  
![Image](https://github.com/user-attachments/assets/5a49f0f2-1300-4d6e-80cb-85499cb63a6d)

---

## Abstract
This repository contains the **data collection (crawling) module** developed for the Cafe Greenwon Digital Transformation project.  
It automates the collection of sales and order data from multiple external platforms and outputs structured Excel files for analysis and makes a dashboard.


## Problem
- Sales data was distributed across multiple platforms with different access methods and formats.
- Manual collection was inefficient and error-prone.
- There was no unified, repeatable process for acquiring data.


## Approach
- Implemented **platform-specific crawlers** using Selenium where APIs were unavailable.
- Separated **crawling** and **preprocessing** to improve maintainability.
- Externalized credentials and paths via environment variables.
- Avoided unnecessary abstractions to keep the system transparent and debuggable.


## Key Findings
- Reliable data collection is a prerequisite for effective analysis.
- Isolating platforms reduces the impact of UI changes.
- Simple automation logic is more robust than complex pipelines.


## Project Structure
```plaintext
src/
├── main.py          # Execution entry point
├── config.py        # Environment-based configuration
├── crawlers/        # Platform-specific crawling logic
├── preprocess/      # Platform-specific data preprocessing
└── utils/           # Shared utilities (browser, files, dates, logging)
```

## Code
- `main.py`: Entry point that orchestrates crawling and preprocessing for one or multiple platforms.
- `crawlers/`: Contains platform-specific Selenium crawlers. Each crawler is isolated to minimize the impact of UI or DOM changes.
- `preprocess/`: Handles transformation of raw collected data into structured, analysis-ready Excel files.
- `utils/`: Shared utilities for browser setup, file handling, date conversion, and logging.

## Tools and Libraries
- Python
- Selenium
- pandas, numpy
- BeautifulSoup
- openpyxl, xlrd

## Contribution
- Designed and implemented the crawling architecture.
- Developed automated data collection for multiple external platforms.
- Built preprocessing pipelines to produce structured Excel outputs.
