"""
FastAPI application for the GenAI Interview Questions Generator.

This module provides a web interface for uploading PDF documents,
processing them to generate interview questions and answers,
and returning the results to the user.
"""

from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import uvicorn
import os
import aiofiles
import json
import csv
from src.helper import llm_pipeline


# Initialize FastAPI application
app = FastAPI(
   title="GenAI Interview Questions Generator",
   description="Generate interview questions and answers from PDF documents",
   version="1.0.0"
)

# Mount static files directory for serving CSS, JS, and other static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
   """
   Serve the main page of the application.
   
   Args:
       request (Request): The incoming request object
       
   Returns:
       TemplateResponse: Rendered HTML template for the index page
   """
   return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_pdf(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
   """
   Handle PDF file uploads.
   
   This endpoint receives a PDF file, saves it to the static/docs directory,
   and returns a success message with the file path.
   
   Args:
       request (Request): The incoming request object
       pdf_file (bytes): The uploaded PDF file content
       filename (str): Name of the uploaded file
       
   Returns:
       Response: JSON response indicating success and the saved file path
   """
   # Create the docs directory if it doesn't exist
   base_folder = 'static/docs/'
   if not os.path.isdir(base_folder):
       os.mkdir(base_folder)
   
   # Save the uploaded PDF file
   pdf_filename = os.path.join(base_folder, filename)
   async with aiofiles.open(pdf_filename, 'wb') as f:
       await f.write(pdf_file)

   # Return success response with the file path
   response_data = jsonable_encoder(json.dumps({"msg": 'success', "pdf_filename": pdf_filename}))
   res = Response(response_data)
   return res


def get_csv(file_path):
   """
   Generate questions and answers from a PDF file and save them to a CSV file.
   
   Args:
       file_path (str): Path to the PDF file
       
   Returns:
       str: Path to the generated CSV file
   """
   # Generate questions and answers using the LLM pipeline
   answer_generation_chain, ques_list = llm_pipeline(file_path)
   
   # Create the output directory if it doesn't exist
   base_folder = 'static/output/'
   if not os.path.isdir(base_folder):
       os.mkdir(base_folder)
   
   # Define the output CSV file path
   output_file = base_folder + "QA.csv"
   
   # Write questions and answers to the CSV file
   with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
       csv_writer = csv.writer(csvfile)
       csv_writer.writerow(["Question", "Answer"])  # Writing the header row

       # Process each question and generate an answer
       for question in ques_list:
           print("Question: ", question)
           answer = answer_generation_chain.run(question)
           print("Answer: ", answer)
           print("--------------------------------------------------\n\n")

           # Save question and answer to the CSV file
           csv_writer.writerow([question, answer])
   
   return output_file


@app.post("/analyze")
async def analyze_pdf(request: Request, pdf_filename: str = Form(...)):
   """
   Process a PDF file to generate interview questions and answers.
   
   This endpoint takes the path of a previously uploaded PDF file,
   processes it to generate questions and answers, and returns
   the path to the resulting CSV file.
   
   Args:
       request (Request): The incoming request object
       pdf_filename (str): Path to the PDF file to analyze
       
   Returns:
       Response: JSON response with the path to the output CSV file
   """
   # Generate CSV file with questions and answers
   output_file = get_csv(pdf_filename)
   
   # Return the path to the CSV file
   response_data = jsonable_encoder(json.dumps({"output_file": output_file}))
   res = Response(response_data)
   return res


# Run the application if executed directly
if __name__ == "__main__":
   uvicorn.run("app:app", host='0.0.0.0', port=8080, reload=True)