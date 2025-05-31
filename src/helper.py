"""
Helper functions for the GenAI Interview Questions Generator.

This module contains utility functions for processing PDF files, 
generating questions and answers using LLMs, and managing the RAG workflow.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv
from src.prompt import *


# Load environment variables and set OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def file_processing(file_path):
   """
   Process a PDF file and prepare it for question generation and answering.
   
   Args:
       file_path (str): Path to the PDF file
       
   Returns:
       tuple: (document_ques_gen, document_answer_gen) - Documents prepared for 
              question generation and answer generation respectively
   """
   # Load data from PDF using PyPDFLoader
   loader = PyPDFLoader(file_path)
   data = loader.load()

   # Concatenate all page content into a single string
   question_gen = ''
   for page in data:
       question_gen += page.page_content
   
   # Create a text splitter for question generation
   # Using larger chunks for question generation
   splitter_ques_gen = TokenTextSplitter(
       model_name='gpt-3.5-turbo',
       chunk_size=10000,
       chunk_overlap=200
   )

   # Split the text into manageable chunks
   chunks_ques_gen = splitter_ques_gen.split_text(question_gen)

   # Convert chunks to Document objects for question generation
   document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

   # Create a text splitter for answer generation
   # Using smaller chunks for answer generation to improve retrieval precision
   splitter_ans_gen = TokenTextSplitter(
       model_name='gpt-3.5-turbo',
       chunk_size=1000,
       chunk_overlap=100
   )

   # Split the documents into smaller chunks for answer generation
   document_answer_gen = splitter_ans_gen.split_documents(
       document_ques_gen
   )

   return document_ques_gen, document_answer_gen


def llm_pipeline(file_path):
   """
   Execute the full LLM pipeline for generating questions and answers.
   
   This function processes a PDF file, generates questions about its content,
   and creates a retrieval system for answering these questions.
   
   Args:
       file_path (str): Path to the PDF file
       
   Returns:
       tuple: (answer_generation_chain, filtered_ques_list) - The QA chain and 
              the list of generated questions
   """
   # Process the file to get documents for question and answer generation
   document_ques_gen, document_answer_gen = file_processing(file_path)

   # Initialize LLM for question generation
   llm_ques_gen_pipeline = ChatOpenAI(
       temperature=0.3,  # Lower temperature for more focused outputs
       model="gpt-3.5-turbo"
   )

   # Create prompt templates for question generation
   PROMPT_QUESTIONS = PromptTemplate(
       template=prompt_template, 
       input_variables=["text"]
   )

   # Create prompt templates for refining questions
   REFINE_PROMPT_QUESTIONS = PromptTemplate(
       input_variables=["existing_answer", "text"],
       template=refine_template,
   )

   # Set up the question generation chain
   ques_gen_chain = load_summarize_chain(
       llm=llm_ques_gen_pipeline, 
       chain_type="refine",  # Use refine to improve questions as more context is provided
       verbose=True,  # Show the process
       question_prompt=PROMPT_QUESTIONS, 
       refine_prompt=REFINE_PROMPT_QUESTIONS
   )

   # Run the question generation chain
   ques = ques_gen_chain.run(document_ques_gen)

   # Create embeddings for semantic search
   embeddings = OpenAIEmbeddings()

   # Create vector store from documents for retrieval
   vector_store = FAISS.from_documents(document_answer_gen, embeddings)

   # Initialize LLM for answer generation with lower temperature for factual answers
   llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")

   # Split and filter the generated questions
   # Keep only lines that end with '?' or '.' to filter out non-questions
   ques_list = ques.split("\n")
   filtered_ques_list = [element for element in ques_list if element.endswith('?') or element.endswith('.')]

   # Set up the answer generation chain
   answer_generation_chain = RetrievalQA.from_chain_type(
       llm=llm_answer_gen, 
       chain_type="stuff",  # "stuff" method puts all retrieved documents into the prompt
       retriever=vector_store.as_retriever()
   )

   return answer_generation_chain, filtered_ques_list