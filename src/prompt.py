"""
Prompt templates for question generation and refinement.

This module contains the prompts used for generating interview questions
from technical documentation and refining those questions with additional context.
"""

# Primary prompt template for generating questions
# This prompt instructs the LLM to create relevant test preparation questions
# based on the provided technical content
prompt_template = """
   You are an expert at creating questions based on coding materials and documentation.
   Your goal is to prepare a coder or programmer for their exam and coding tests.
   You do this by asking questions about the text below:

   ------------
   {text}
   ------------

   Create questions that will prepare the coders or programmers for their tests.
   Make sure not to lose any important information.

   QUESTIONS:
   """


# Refinement prompt template used in the chain
# This prompt helps to improve existing questions using additional context
# It allows for iterative refinement as new chunks of text are processed
refine_template = ("""
   You are an expert at creating practice questions based on coding material and documentation.
   Your goal is to help a coder or programmer prepare for a coding test.
   We have received some practice questions to a certain extent: {existing_answer}.
   We have the option to refine the existing questions or add new ones.
   (only if necessary) with some more context below.
   ------------
   {text}
   ------------

   Given the new context, refine the original questions in English.
   If the context is not helpful, please provide the original questions.
   QUESTIONS:
   """
   )