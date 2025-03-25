import psutil
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plyer import notification

# Function to send email notification
def send_email_notification(subject, body):
    sender_email = "your_email@gmail.com"  # Replace with your email
    receiver_email = "recipient_email@gmail.com"  # Replace with recipient's email
    password = "your_email_password"  # Replace with your email password

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Setup the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS (encryption)
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: Unable to send email. {e}")

# Function to send desktop notification
def send_desktop_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification will be displayed for 10 seconds
    )

# Function to check CPU usage and diagnose issues
def monitor_cpu_usage():
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Current CPU Usage: {cpu_usage}%")
    
    # If CPU usage is greater than 90%, it could indicate an issue
    if cpu_usage > 90:
        print("High CPU usage detected!")
        
        # Find processes using the most CPU
        processes = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) for p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent'])]
        processes.sort(key=lambda x: x[2], reverse=True)  # Sort processes by CPU usage
        
        # Log the process with the highest CPU usage
        print(f"Process using most CPU: PID {processes[0][0]}, Name: {processes[0][1]}, CPU: {processes[0][2]}%")
        
        # If a specific process is causing issues
        if processes[0][2] > 90:
            send_desktop_notification("High CPU Usage Detected", f"Process {processes[0][1]} is consuming {processes[0][2]}% of CPU.")
            send_email_notification("High CPU Usage Alert", f"Process {processes[0][1]} with PID {processes[0][0]} is consuming {processes[0][2]}% of CPU.")
            
            # Automated Action: Terminate the high CPU usage process
            try:
                print("Terminating the high CPU usage process...")
                psutil.Process(processes[0][0]).terminate()  # Terminate the process
                print(f"Terminated process {processes[0][1]}.")
                time.sleep(2)  # Wait for the process to be terminated
            except Exception as e:
                print(f"Error terminating process: {e}")
            
            # Optional: Restart the application if needed (e.g., for a web server)
            # os.system("command_to_restart_application")  # Example for restarting an app
            
            # Automated Action: Reboot the system if CPU usage remains high
            print("Rebooting system due to high CPU usage...")
            os.system("shutdown /r /t 1")  # Reboot on Windows
            # Uncomment below for Linux/Unix systems:
            # os.system("sudo reboot")
            
    else:
        print("CPU usage is normal.")
        
# Run the monitoring function periodically
while True:
    monitor_cpu_usage()
    time.sleep(5)  # Check every 5 seconds
