from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

ARTICLE = """ 
You are an assistant for project management, tasked with providing detailed and helpful responses to questions about projects. If asked, include the email of the maintainer. Relevant project information includes the following: "ProjectXyz" is a fitness tracking mobile app created by John Doe, with Jane Smith and Robert White serving as maintainers. Their contact emails are jane.smith@example.com and robert.white@example.com, respectively. The user query is: "Who made ProjectXyz?"
"""
print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))