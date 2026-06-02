# AutoApply AI

AI-powered job application assistant that helps candidates tailor resumes, generate cover letters, track applications, and manage their job search workflow in one place.

![Dashboard](assets/dashboard.png)

---

## Overview

AutoApply AI streamlines the job application process by combining resume optimization, cover letter generation, and application tracking into a single platform.

Instead of manually rewriting documents for every role, users can upload an existing resume, provide a target company and position, and generate tailored application materials in seconds.

---

## Features

### Resume Tailoring

* Upload PDF, DOC, DOCX, or TXT resumes
* Extract and analyze resume content
* Generate role-specific resume versions
* Export professional PDF and DOCX formats

### Cover Letter Generation

* AI-generated personalized cover letters
* Company and role specific customization
* Professional business format
* Download-ready PDF and DOCX exports

### Application Tracker

* Track submitted applications
* Update application status
* Manage interview progress
* Monitor offers and outcomes

### Dashboard Analytics

* Total applications overview
* Interview tracking
* Offer statistics
* Recent application activity

### Modern UI

* Responsive design
* Light and dark theme support
* Clean dashboard experience
* Optimized workflow navigation

---

## Screenshots

### Dashboard

![Dashboard](assets/dashboard.png)

### Resume Generator

![Resume Generator](assets/apply-page.png)

### Application Tracker

![Tracker](assets/tracker.png)

---

## Demo

![Demo](assets/demo.gif)

Or watch the full demo:

https://your-demo-link-here

---

## Technology Stack

### Frontend

* Reflex
* Python
* Radix UI Components

### Backend

* Python
* Reflex State Management

### Document Processing

* PyPDF2
* python-docx
* ReportLab

### AI Integration

* OpenAI API

---

## Project Structure

```text
autoapply_ai/
│
├── pages/
│   ├── dashboard.py
│   ├── tracker.py
│   ├── assets.py
│
├── components/
│   ├── layout.py
│   ├── bottom_nav.py
│
├── services/
│   ├── export.py
│   ├── pdf_generator.py
│
├── state.py
├── styles.py
└── rxconfig.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/hananzamri/autoapply.git
cd autoapply
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create environment variables:

```bash
cp .env.example .env
```

Configure:

```env
OPENAI_API_KEY=your_api_key
```

Run the application:

```bash
reflex run
```

Application will be available at:

```text
http://localhost:3000
```

---

## Roadmap

### Current

* Resume tailoring
* Cover letter generation
* PDF export
* DOCX export
* Application tracker

### Upcoming

* ATS compatibility scoring
* Keyword gap analysis
* Job board integration
* LinkedIn integration
* Interview preparation assistant
* Multi-resume management
* Analytics dashboard

---


Nur Hanan Mohammad Zamri

Artificial Intelligence & Data Science

Sejong University

LinkedIn: https://linkedin.com/in/nurhanan

---

## License

This project is licensed under the MIT License.
