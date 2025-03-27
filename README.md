# NetZero Letter Generation System - MVP

A Streamlit-based application for automatically generating formal letters using AI, following NetZero brand guidelines.

## Features

- Generate formal letters in Arabic using AI
- Edit and preview letters before saving
- Save letters to the central database
- Integration with existing NetZero systems

## Setup

1. Install dependencies:
pip install -r requirements.txt
2. Run the application:
streamlit run app.py
## API Endpoints

The application uses the following API endpoints:
- `/generate-letter` - Generate a new letter using AI
- `/save-letter` - Save the letter to the database

## Brand Guidelines

This application follows NetZero's brand guidelines, including:
- Tajwal font for Arabic text
- Official color scheme
- Right-to-left layout for Arabic content
