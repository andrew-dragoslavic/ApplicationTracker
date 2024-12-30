import email
import imaplib
import torch
from transformers import pipeline
import json
import re
import pandas as pd
import openpyxl

# Initialize the text-generation pipeline
model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# System role to define the task
system_prompt = (
    '''You will be given a text input that contains information about a job application.Your task is to extract only the following details:
    1.    Job Title (e.g., Software Engineer, Data Scientist, etc.)
    2.Company Name(e.g., Google, Microsoft, etc.)
    3.Application Status(Accepted, Rejected, or Under Review).
    Respond in JSON format with keys for ‘JobTitle’, ‘CompanyName’, and ‘ApplicationStatus. Do not add any additional commentary, examples, or unrelated content. Only provide the extracted details. DO NOT GENERATE YOUR EXAMPLE EMAILS EMAILS AND ANALYZE THEM. Once the extracted information from the original email is output stop generating information.''')

# Combine the system prompt and the email content
# Generate output

username = 'andrew.dragoslavic@gmail.com'
password = 'veol sbwu wgat mjyw' #App Password

imap_server = 'imap.gmail.com' # Connects to gmail

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, password)
imap.select('INBOX')

result, data = imap.search(None, 'SUBJECT "application" NOT FROM "jobs-noreply@linkedin.com" SINCE "01-Dec-2024"') #Get all items with keyword application
data = data[0].split() #Create a list of them
data = [(d.decode('utf-8')) for d in data] #Conver list from byte string to integers
data.reverse()

# Function to extract JSON from output
def extract_json_from_output(output):
    try:
        # Locate the JSON portion using regex
        json_match = re.search(r"{.*}", output, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)  # Extract matched JSON string
            return json.loads(json_str)    # Parse the JSON string into a Python dict
        else:
            raise ValueError("No JSON found in the output.")
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None
    except ValueError as e:
        print(e)
        return None

columns = ['JobTitle', 'CompanyName', 'ApplicationStatus']
data_table = pd.DataFrame(columns=["JobTitle", "CompanyName", "ApplicationStatus"])

for d in data:
    r, subject = imap.fetch(d, '(RFC822)')
    raw_email = subject[0][1]
    msg = email.message_from_bytes(raw_email)

    subject = msg['subject']

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            if 'attachment' not in content_disposition:
                if content_type == 'text/plain':
                    body = part.get_payload(decode=True).decode()
                    # print(f"Plain text: {body}")
                    break
                elif content_type == 'text/html':
                    body = part.get_payload(decode=True).decode()
                    # print(f"HTML text: {body}")
                    break
    else:
        body = msg.get_payload(decode=True).decode()
        # print("Body:", body)

    input_text = f"{system_prompt}\n\nEmail Content:\n{subject}\n{body}\n\nExtracted Information:"

    outputs = pipe(
        input_text,
        max_new_tokens=128,
    )

    # Print the extracted information
    model_output = (outputs[0]["generated_text"])

    # Extracted JSON
    extracted_json = extract_json_from_output(model_output)

    # Output result
    if extracted_json:
        print("Extracted JSON:", extracted_json)
    else:
        print("Failed to extract JSON.")

    if extracted_json:
        new_row = pd.DataFrame([extracted_json])
        data_table = pd.concat([data_table, new_row], ignore_index=True)

print(data_table)

data_table.to_excel("job_applications.xlsx", index=False)

print("Data saved as Excel in your directory.")