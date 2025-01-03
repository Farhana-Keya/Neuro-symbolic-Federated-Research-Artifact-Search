# ORKG Email extraction API

[![pipeline status](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/badges/main/pipeline.svg)](https://gitlab.com/TIBHannover/orkg/nlp/orkg-nlp-api/-/commits/main)

REST API for the ORKG-email extraction python.

This API provides the emails from PDF, DOI, TITLE and ORCID.

## Prerequisites

We require a Python version `3.7` or above and Grobid from `https://orkg.org/grobid`.

Requirement by service:

| Service                    | Requirement(s)    |
|----------------------------|-------------------|
| `/email_extraction_pdf`          | `file: upload a file`, `UploadPdf: True` |
| `/email_extraction_ORCID`        | `ORCID_id: add a ORCID_id` |
| `/email_extraction_using_title`        | `title: add a title`, `UploadPdf: False`|
| `/email_extraction_using_doi`        | `doi: add a doi` , `UploadPdf: False` |

## How to run

### With ``docker-compose``


```commandline

```

### Manually

```commandline

uvicorn main:app --reload

```
For local development you may run the web server using ``uvicorn`` with the ``--reload`` option:

```commandline
uvicorn app.main:app --host 0.0.0.0 --port 4321 --reload
```


### Why Integrate Grobid with Regular expression?

```commandline
Please find all the papers in the "tests/test_file" folder for the test.
```

| Research paper                    | DOI    |Grobid output    |Grobid with Regular expression output    | Expected output|
|----------------------------|-------------------|-------------------|-------------------|-------------------|
| `Open Research Knowledge Graph:A System Walkthrough`   | https://doi.org/10.1007/978-3-030-30760-8_31 | "oelen@l3s.de", "manuel.prinz@tib.eu", "markus.stocker@tib.eu", "auer@tib.eu" | "oelen@l3s.de", "manuel.prinz@tib.eu", "markus.stocker@tib.eu", "auer@tib.eu", "jaradeh@l3s.de" | "oelen@l3s.de", "manuel.prinz@tib.eu", "markus.stocker@tib.eu", "auer@tib.eu", "jaradeh@l3s.de"|   
| `TeKET : a Tree-Based Unsupervised Keyphrase Extraction Technique` | https://doi.org/10.1007/s12559-019-09706-3 | "saifulazad@ump.edu.my" | "saifulazad@ump.edu.my", "mufti.mahmud@ntu.ac.uk", "muftimahmud@gmail.com"| "saifulazad@ump.edu.my", "mufti.mahmud@ntu.ac.uk", "muftimahmud@gmail.com" |  
| `Enriching Scholarly Knowledge with Context`| https://doi.org/10.1007/978-3-031-09917-5_10 | "haris@l3s.de", "markus.stocker@tib.eu", "auer@tib.eu" | "haris@l3s.de", "markus.stocker@tib.eu", "auer@tib.eu" | "haris@l3s.de", "markus.stocker@tib.eu", "auer@tib.eu"  | 
| `Persistent Identification and Interlinking of FAIR Scholarly Knowledge` | NaN | "markus.stocker@tib.eu", "auer@tib.eu" | "markus.stocker@tib.eu", "auer@tib.eu", "haris@l3s.de" | "markus.stocker@tib.eu", "auer@tib.eu", "haris@l3s.de"  | 

## API Documentation
After successfully running the application, check the documentation at `localhost:4321/docs`
or `localhost:4321/redoc` (please adapt your `host:port` in case you configured them).
