# Project Title

Official python library for [Promptlytics](https://www.promptlytics.co/)

## Description

Promptlytics is a prompt analytics tool that helps you find the best prompts for your use case by tracking user feedback and associating it with your prompt templates.

## Installation

```bash
pip install promptlytics
```

## Getting Started

Use an instance of the Promptlytics class to get your prompt templates and track user feedback

```python
from promptlytics import Promptlytics

promptlytics = Promptlytics(YOUR_API_KEY)

# Gets the template selected for use in your dashboard
template = promptlytics.useTemplate(use_selected=True)

# sends user feedback
promptlytics.track(use_selected=True, rating=5, completion="string response from your LLM")
```
