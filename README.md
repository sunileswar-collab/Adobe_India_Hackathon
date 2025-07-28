# 📘 Challenge 1B: Persona-Driven Document Intelligence

This project is part of Adobe's **"Connecting the Dots" Hackathon 2025** – Challenge 1B. It implements an offline, CPU-only document intelligence system that extracts and ranks the most relevant sections from a set of PDFs based on a given **persona** and **job-to-be-done**.

---

## 🚀 Objective

Build a generic document analyzer that:
- Accepts a **persona** and **task goal**
- Processes a collection of **3–10 PDFs**
- Extracts **most relevant sections** and refines them
- Outputs a **ranked structured JSON**
- Runs **offline** on **CPU** in ≤60 seconds
- Uses model(s) ≤ **1GB**

---

## 📁 Directory Structure

challenge_1b_ml/
├── app/
│ ├── run_analysis.py # Main logic to process documents
│ ├── server.py # Optional server interface
│ └── models/
│ └── flan-t5-base/ # Offline model (FLAN-T5)
├── Collection/
│ ├── challenge1b_input.json # Input: persona + documents + task
│ ├── challenge1b_output.json # Output: ranked analysis
│ └── PDFs/ # Folder containing 3–10 input PDFs
├── Dockerfile
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 📥 Input Format – `challenge1b_input.json`

```json
{
  "persona": "Undergraduate Chemistry Student",
  "job_to_be_done": "Identify key concepts and mechanisms for exam preparation on reaction kinetics",
  "documents": [
    "Collection/PDFs/Chapter1.pdf",
    "Collection/PDFs/Chapter2.pdf"
  ]
}
📤 Output Format – challenge1b_output.json
json
Copy
Edit
{
  "metadata": {
    "persona": "Undergraduate Chemistry Student",
    "job_to_be_done": "Identify key concepts and mechanisms for exam preparation on reaction kinetics",
    "input_documents": [...],
    "processing_time": "2025-07-28T16:30:00"
  },
  "extracted_sections": [
    {
      "document": "Chapter1.pdf",
      "page_no": 3,
      "section_title": "Reaction Kinetics Basics",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "Chapter1.pdf",
      "page_no": 3,
      "section_title": "Reaction Kinetics Basics",
      "refined_text": "Reaction kinetics involves the study of rates and mechanisms..."
    }
  ]
}
🧠 Model Used
Model: google/flan-t5-base

Size: ~944 MB

Location: app/models/flan-t5-base/

Usage: Refines extracted section text and ranks relevance.

📦 Note: Due to GitHub file size limits (>100MB), the model file is not included in the repo.

Before building the Docker image, please ensure:

bash
Copy
Edit
app/models/flan-t5-base/pytorch_model.bin
is placed manually.

🐳 Docker Instructions
✅ Build Image (Linux AMD64)
bash
Copy
Edit
docker build -t persona-analyzer --platform linux/amd64 .
✅ Run Inference (Offline CPU Mode)
powershell
Copy
Edit
docker run --rm -v ${PWD}/Collection:/app/Collection --network none persona-analyzer
📌 Constraints Met
✅ Runs fully offline (no internet required)

✅ CPU-only inference

✅ < 1GB total model size

✅ ≤ 60 seconds for 3–10 documents

✅ Structured output in correct JSON format

📦 Deliverables
✅ challenge1b_output.json

✅ approach_explanation.md

✅ Dockerized source code
