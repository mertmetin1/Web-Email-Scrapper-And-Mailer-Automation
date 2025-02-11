# Email Scraper & Job Application Sender

## 📌 Overview
This project is a **fully automated system** that scrapes email addresses from given websites and then sends job application emails to the collected addresses. It is designed for job seekers who want to apply for multiple jobs efficiently.

## ⚙️ Features
- **Web Scraping:** Extracts emails from a list of websites recursively (up to a max depth of 10).
- **Email Validation:** Ensures only valid email formats are collected.
- **Bulk Email Sending:** Automatically sends job application emails to the scraped email addresses.
- **Resume Attachment:** Attaches a CV (PDF) to each sent email.
- **Logging System:** Keeps track of sent and failed emails to prevent duplicate applications.
- **robots.txt Compliance:** Ensures ethical web scraping.

## 🛠️ Technologies Used
- **Python**
- **BeautifulSoup** (for web scraping)
- **requests** (for handling HTTP requests)
- **smtplib & email.mime** (for sending emails)
- **pandas & csv** (for data handling and logging)

## 📂 Project Structure
```
├── email_scraper_sender.py   # Main script for scraping and email sending
├── websites.csv              # List of websites to scrape emails from
├── scraped_emails.csv        # Output file containing collected emails
├── email_log.csv             # Log file for tracking sent emails
├── your_cv.pdf               # Resume to be sent as an attachment
├── README.md                 # Project documentation
```

## 🚀 How to Use
### 1️⃣ Install Dependencies
```sh
pip install requests beautifulsoup4 pandas
```

### 2️⃣ Prepare Input Files
- Add websites to `websites.csv` (one per line).
- Place your CV in the project directory (`cv.pdf`).

### 3️⃣ Run the Script
```sh
python email_scraper_sender.py
```

### 4️⃣ Monitor Logs
- `scraped_emails.csv`: List of collected emails.
- `email_log.csv`: Track successfully sent and failed emails.

## 🔒 Ethical Considerations
- Always check a website’s `robots.txt` before scraping.
- Do not spam; send emails responsibly.
- Modify the script as needed to comply with GDPR and other data regulations.

---


