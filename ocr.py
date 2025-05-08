import os
import requests
import json
import time
def main():
    t1 = time.perf_counter(), time.process_time()
    schema={"title":"Annexe Personnes morales","type":"object","properties":{"document-id":{"type":"number"},"document-type":{"type":"string"},"authorized-person-name":{"type":"string"},"old-address":{"type":"string"},"new-address":{"type":"string"},"date":{"type":"string"},"short-summary":{"type":"string"}},"required":["document-id","document-type","name","reason"]}
    message={
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": "extract all the text of the PDF document."
                },
                {
                    "type": "document_url",
                    "document_url": "https://www.ejustice.just.fgov.be/tsv_pdf/2025/03/12/25034497.pdf"
                }
                ]
            }
            ],
            "document_image_limit": 8,
            "document_page_limit": 1
            }
    MISTRAL_API_KEY= os.environ['MISTRAL_API_KEY']
    response = requests.post(
    "https://api.mistral.ai/v1/chat/completions",
    headers={"Content-Type": "application/json",
             "Authorization": f"Bearer {MISTRAL_API_KEY}"},
    data=json.dumps(message)
    )
    print(response.content)
    t2 = time.perf_counter(), time.process_time()

    print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
    print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
    print()


if __name__ == "__main__":
    main()
