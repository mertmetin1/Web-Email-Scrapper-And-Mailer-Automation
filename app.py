import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from urllib.parse import urljoin, urlparse
import os

def is_allowed_by_robots(url):
    robots_url = urljoin(url, "/robots.txt")
    try:
        response = requests.get(robots_url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            return "Disallow" not in response.text
    except:
        pass
    return True

def get_emails_from_url(url, visited_urls, emails, depth, max_depth=10):
    if url in visited_urls or depth > max_depth:
        return
    
    visited_urls.add(url)
    print(f"Scanning: {url} (Depth: {depth})")
    
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        found_emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.text))
        emails.update(found_emails)
        
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            parsed_url = urlparse(next_url)
            if parsed_url.netloc == urlparse(url).netloc:
                get_emails_from_url(next_url, visited_urls, emails, depth + 1, max_depth)
    except Exception as e:
        print(f"Hata oluştu: {e}")

def scrape_emails_from_websites(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        websites = [row[0] for row in reader if row]
    
    all_results = []
    
    for website in websites:
        if not is_allowed_by_robots(website):
            print(f"Skipping {website} due to robots.txt restrictions.")
            continue
        
        emails = set()
        visited_urls = set()
        get_emails_from_url(website, visited_urls, emails, depth=0, max_depth=10)
        all_results.extend(emails)
        time.sleep(2)
    
    with open("scraped_emails.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Email"])
        for email in all_results:
            writer.writerow([email])
    
    print("E-postalar 'scraped_emails.csv' dosyasına kaydedildi.")

def send_email(sender_email, sender_password, receiver_email, pdf_file):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = 'Job Application'

        email_body = """
        Dear Hiring Manager,

        I hope this email finds you well. Please find my CV attached for review. 
        I am eager to join your esteemed organization.

        Best regards,
        Your Name
        """
        msg.attach(MIMEText(email_body, 'plain'))

        attachment = open(pdf_file, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={pdf_file}")
        msg.attach(part)

        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {str(e)}")
        return False

def send_emails_from_scraped_list(sender_email, sender_password, pdf_file):
    emails_df = pd.read_csv("scraped_emails.csv")
    emails = emails_df["Email"].tolist()
    
    for email in emails:
        time.sleep(1)
        success = send_email(sender_email, sender_password, email, pdf_file)
        print(f"{email}: {'Mail Gönderildi' if success else 'Gönderme Hatası'}")

if __name__ == "__main__":
    sender_email = 'email'  # Gmail adresiniz
    sender_password = 'pass'  # Gmail şifreniz
    pdf_file = 'CV.pdf'  # E-postaya ekleyeceğiniz PDF dosyası
    scrape_emails_from_websites('websites.csv')
    send_emails_from_scraped_list(sender_email, sender_password, pdf_file)
