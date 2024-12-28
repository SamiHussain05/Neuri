from openai import AzureOpenAI
import pdfplumber
import aspose.words as aw
import requests
import matplotlib.pyplot as plt
import base64
import subprocess

ENDPOINT = ""
API_KEY = ""

# ENDPOINT2 = ""
# API_KEY2 = ""

API_VERSION = "2024-08-01-preview"
MODEL_NAME = "gpt-4-2"

# API_VERSION2 = "2024-08-01-preview"
# MODEL_NAME2 = "dall-e-3"

# client2 = AzureOpenAI(
#     azure_endpoint=ENDPOINT2,
#     api_key=API_KEY2,
#     api_version=API_VERSION2,
# )


client = AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION,
)




# def generate_and_save_image(prompt, image_name):
#     url = ENDPOINT2
#     headers = {
#         "Content-Type": "application/json",
#         "api-key": API_KEY2,
#     }
#     data = {
#         "prompt": prompt,
#         "n": 1,  # Generate 1 image
#         "size": "1024x1024"  # Image size
#     }
    # try:
    #     response = requests.post(url, headers=headers, json=data)
    #     response.raise_for_status()
    #     response_json = response.json()

    #     # Handle different response structures
    #     if 'data' in response_json and len(response_json['data']) > 0:
    #         # Check for a URL key in the response
    #         if 'url' in response_json['data'][0]:
    #             # Handle image URL
    #             image_url = response_json['data'][0]['url']
    #             image_response = requests.get(image_url)
    #             with open(image_name, "wb") as img_file:
    #                 img_file.write(image_response.content)
    #             print(f"Image saved as {image_name}")
    #         else:
    #             print(f"Unexpected data structure: {response_json['data'][0]}")
    #     else:
    #         print(f"Unexpected response structure: {response_json}")
    # except requests.exceptions.HTTPError as http_err:
    #     print(f"HTTP error occurred: {http_err}")
    # except Exception as e:
    #     print(f"An error occurred while generating the image: {e}")
   

def extract_information(pdf_path):
    concatenated_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                concatenated_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"An error occurred: {e}")
    return concatenated_text


text = ""
pdf_path = "volumesofrev.pdf"

text = extract_information(pdf_path)

chunk_size = 1000
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

summaries = []
for chunk in chunks:
    MESSAGES = [
        {"role": "system", "content": "your job is to always write the word python before and after any code you write"},
        {"role": "user", "content": f"generate python code for matplotlib to visualise the equations in the pdf here, remember to put a '#' before every line that you write that is not code:\n\n{chunk}"}
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=MESSAGES,
        )
        content = response.choices[0].message.content
        summaries.append(content)
    except Exception as e:
        print(f"An error occurred while summarizing: {e}")



# Combine Summaries
final_summary = " ".join(summaries)

# prompt = f"can you show the equation explained here, without any people or objects or anything complex, just the equation discussed here in the absolute simplest way please with nothing extra:\n\n{final_summary}"
# image_name = f"image_chunk_{1}.png"
# generate_and_save_image(prompt, image_name)

# create document object
doc = aw.Document()

# create a document builder object
builder = aw.DocumentBuilder(doc)

# add text to the document
builder.write(final_summary)

# save document
doc.save("summary.docx")


final_summary = final_summary.replace('`', '').replace('python', '')

print(final_summary)


with open("visualisation.py", "w") as file:
    file.write(final_summary)

subprocess.run(["python", "visualisation.py"])