import os
os.environ["HF_HOME"] = "D:\\HuggingFaceCache"

from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

ARTICLE = """ 
New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
"""
print(summarizer(ARTICLE, max_length=50, min_length=30, do_sample=False))