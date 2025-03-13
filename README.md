# Description
Python script to use Mistral OCR to extract the text from a PDF.
For this example a [Monitour Belge PDF](https://www.ejustice.just.fgov.be/tsv_pdf/2025/03/12/25034497.pdf) is being used.

# Running the Script

## Env variable
export MISTRAL_API_KEY={your api key}

## Get requirements
uv sync

## Run OCR
uv run ocr.py

# Results

OCR is good but is far from being perfect, in this example can be noticed that it struggles with some characters, for example:
> Example
> Belgi\xc3\xab instead of België

Quality of the OCR is not being affected by the model being used, actually OCR errors are the same when using mistral-small-latest and mistral-large-latest



## Raw Text
```JSON
{"id":"74076798fa1d4f16b2cd22a88fe2cb7f","object":"chat.completion","created":1741852402,"model":"mistral-small-latest","choices":[{"index":0,"message":{"role":"assistant","tool_calls":null,"content":"Here is the extracted text from the PDF document:\\n\\n---\\n\\nIn de bijlagen bij het Belgisch Staatsblad bekend te maken kopie na neerlegging van de akte ter griffie\\n\\n# Onderwerp akte : Zetelverplaatsing\\n\\nUittreksel uit de notulen van het schriftelijk besluit van de Raad van Bestuur dd. 25 februari 2025:\\n[...]\\nDe raad van bestuur beslist en bevestigt hierbij om de maatschappelijke zetel van de Vennootschap over te brengen van het huidige adres naar het volgende adres: Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgi\xc3\xab zoals reeds doorgevoerd in de Kruispuntbank van Ondernemingen onder de sectie vestigingseenheid. De raad van bestuur bevestigt dat de Vennootschap hiermee gevestigd blijft binnen het Vlaamse Gewest.\\n$[\\\\ldots]$\\nDe leden van de raad van bestuur verlenen volmacht aan mevrouw Tinneke De Boeck, kantoorhoudende te Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgi\xc3\xab alleen handelend en met de mogelijkheid tot indeplaatsstelling, ten einde al het nodige te doen om de beslissingen van de raad van bestuur tegenstelbaar te maken aan derden, zo doende deze (1) te laten publiceren in de Bijlagen bij het Belgisch Staatsblad, en (2) om in het licht daarvan alle nodige administratieve formaliteiten te vervullen en handelingen te stellen die hiervoor vereist of dienstig zouden zijn, waaronder, de Vennootschap te vertegenwoordigen bij de Kruispuntbank van Ondernemingen, een ondernemingsloket naar keuze en de Griffie van de Ondernemingsrechtbank.\\n$[\\\\ldots]$\\n\\nTinneke De Boeck\\nGevolmachtigde/Lasthebber\\n\\n---\\n\\nThis text includes the details of a decision made by the Board of Directors to relocate the company\'s headquarters and the authorization given to Tinneke De Boeck to handle the necessary administrative tasks."},"finish_reason":"stop"}],"usage":{"prompt_tokens":433,"total_tokens":893,"completion_tokens":460}}
```
 Real time: 7.45 seconds
 CPU time: 0.01 seconds

## Json Schema - Mistrall Small

 ```JSON
 {"id":"b40b1eec14fd49e5bc2d338e6fc64a47","object":"chat.completion","created":1741807711,"model":"mistral-small-latest","choices":[{"index":0,"message":{"role":"assistant","tool_calls":null,"content":"```json\\n{\\n  \\"document-id\\": 1932,\\n  \\"document-type\\": \\"Zetelverplaatsing\\",\\n  \\"authorized-person-name\\": \\"Tinneke De Boeck\\",\\n  \\"old-address\\": \\"Not specified\\",\\n  \\"new-address\\": \\"Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgi\xc3\xab\\",\\n  \\"date\\": \\"2025-02-25\\",\\n  \\"short-summary\\": \\"The board of directors has decided to move the company\'s headquarters to Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgium. Tinneke De Boeck is authorized to handle all necessary actions to make the decision enforceable.\\"\\n}\\n```"},"finish_reason":"stop"}],"usage":{"prompt_tokens":625,"total_tokens":783,"completion_tokens":158}}
 ```
 Real time: 5.03 seconds
 CPU time: 0.01 seconds

## Json Schema - MISTRAL 8B
better understanding

```JSON
 {"id":"5864117283234e9daa821ff9f9a7f85c","object":"chat.completion","created":1741807876,"model":"ministral-8b-latest","choices":[{"index":0,"message":{"role":"assistant","tool_calls":null,"content":"```json\\n{\\n  \\"title\\": \\"Annexe Personnes morales\\",\\n  \\"type\\": \\"object\\",\\n  \\"properties\\": {\\n    \\"document-id\\": {\\"type\\": \\"number\\"},\\n    \\"document-type\\": {\\"type\\": \\"string\\"},\\n    \\"authorized-person-name\\": {\\"type\\": \\"string\\"},\\n    \\"old-address\\": {\\"type\\": \\"string\\"},\\n    \\"new-address\\": {\\"type\\": \\"string\\"},\\n    \\"date\\": {\\"type\\": \\"string\\"},\\n    \\"short-summary\\": {\\"type\\": \\"string\\"}\\n  },\\n  \\"required\\": [\\"document-id\\", \\"document-type\\", \\"name\\", \\"reason\\"],\\n  \\"items\\": [\\n    {\\n      \\"document-id\\": 1,\\n      \\"document-type\\": \\"Zetelverplaatsing\\",\\n      \\"authorized-person-name\\": \\"Tinneke De Boeck\\",\\n      \\"old-address\\": \\"Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgi\xc3\xab\\",\\n      \\"new-address\\": \\"Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgi\xc3\xab\\",\\n      \\"date\\": \\"2025-02-25\\",\\n      \\"short-summary\\": \\"De maatschappelijke zetel van de Vennootschap wordt overgebracht naar Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgi\xc3\xab. Tinneke De Boeck wordt gevolmachtigd om de beslissingen te publiceren en alle nodige administratieve formaliteiten te vervullen.\\"\\n    }\\n  ]\\n}\\n```"},"finish_reason":"stop"}],"usage":{"prompt_tokens":625,"total_tokens":946,"completion_tokens":321}}
 ```
 Real time: 5.67 seconds
 CPU time: 0.01 seconds


## Json Schema - Using Mistral large

```JSON
{"id":"2eb7c3693ff045be858fe7aa5ee2492e","object":"chat.completion","created":1741807948,"model":"mistral-large-latest","choices":[{"index":0,"message":{"role":"assistant","tool_calls":null,"content":"```json\\n{\\n  \\"document-id\\": 0,\\n  \\"document-type\\": \\"Zetelverplaatsing\\",\\n  \\"authorized-person-name\\": \\"Tinneke De Boeck\\",\\n  \\"old-address\\": \\"Onbekend\\",\\n  \\"new-address\\": \\"Xenon Building, Hermeslaan 11, 1932 Zaventem, Belgi\xc3\xab\\",\\n  \\"date\\": \\"2025-02-25\\",\\n  \\"short-summary\\": \\"De raad van bestuur heeft besloten om de maatschappelijke zetel van de Vennootschap te verplaatsen naar het nieuwe adres in Zaventem, Belgi\xc3\xab. Mevrouw Tinneke De Boeck is gevolmachtigd om alle nodige stappen te ondernemen om deze beslissing tegenstelbaar te maken aan derden en de administratieve formaliteiten te vervullen.\\"\\n}\\n```"},"finish_reason":"stop"}],"usage":{"prompt_tokens":760,"total_tokens":993,"completion_tokens":233}}
```
 Real time: 7.92 seconds
 CPU time: 0.01 seconds
