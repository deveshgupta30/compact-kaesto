import argparse
import smtplib, ssl
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr



def send_email(args):

    message = MIMEMultipart()

    current_date_formatted = datetime.now().strftime("%d/%m/%Y")
    subject = f"{args.subject} - {current_date_formatted}" if args.subject else f"Report - {current_date_formatted}"
    message["Subject"] = subject

    message["From"] = formataddr(
        (str(Header(args.header, "utf-8")), args.source)
    )

    message["To"] = args.dest

    try:
        with open(args.attach, "r") as f:
            text = f.read()
        message.attach(MIMEText(text, "html"))
    except FileNotFoundError:
        print("Warning: html not found. Sending email without body.")

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(args.source, args.password)
            server.sendmail(args.source, args.dest, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def main():
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--attach", dest='attach', 
                        help="Attachment file", default=None)
    parser.add_argument("--subject", dest='subject', 
                        help="Email subject", default=None)
    parser.add_argument("--source", dest='source', 
                        help="Sender email", required=True)
    parser.add_argument("--dest", dest='dest', 
                        help="Destination email", required=True)
    parser.add_argument("--password", dest='password', 
                        help="Email password", required=True)
    parser.add_argument("--header", dest='header', 
                        help="Email header text", required=True)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Send email
    send_email(args)

if __name__ == "__main__":
    main()