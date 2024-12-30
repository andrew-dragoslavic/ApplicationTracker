# Job Application Parser

## Overview
The **Job Application Parser** is an automated tool designed to extract and organize critical information from job application emails. Using state-of-the-art Natural Language Processing (NLP) models, the project identifies key details such as job titles, company names, and application statuses from unstructured email content. The results are saved in a structured format for easy analysis and tracking.

---

## Features
- **Email Parsing**: Connects to an email account using IMAP and fetches job-related emails.
- **Information Extraction**: Extracts:
  - Job Title
  - Company Name
  - Application Status (e.g., Accepted, Rejected, Under Review)
- **NLP Model**: Utilizes a pre-trained LLaMA model for text understanding and extraction.
- **Data Organization**:
  - Outputs extracted information into a tabular format.
  - Saves the structured data as an Excel file for easy visualization and storage.
- **Time Filtering**: Retrieves emails from a specified date onward.

---

## How It Works
1. **Fetch Emails**: Connects to the email server and retrieves job application emails using `imaplib`.
2. **Text Extraction**: Processes the body of each email to extract meaningful content.
3. **NLP Processing**: Feeds the email content into an NLP pipeline to extract structured information.
4. **Data Saving**: Saves extracted information in an Excel table format for future reference and analysis.

---

## Prerequisites
- Python 3.9 or later
- Required Python libraries:
  - `transformers`
  - `torch`
  - `pandas`
  - `openpyxl`
  - `imaplib`

---

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/andrew-dragoslavic/ApplicationTracker.git
