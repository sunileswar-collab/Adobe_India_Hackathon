# In D:\CONNECTING_DOTS\Challenge_1a\main.py (No changes needed from previous suggestions)

import argparse
import os
from utils.logger import setup_logger
from utils.heading_classifier import HeadingClassifier
from process_pdfs import process_pdf
from json_schema import load_schema # Assuming load_schema is used from json_schema.py

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Process PDFs to extract titles and outlines.")
    parser.add_argument("--pdf_dir", type=str, required=True, help="Path to the directory containing PDF files.")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to the output directory for processed JSONs.")
    parser.add_argument("--schema", type=str, help="Path to the JSON schema for validation (optional).")
    parser.add_argument("--model_path", type=str, default="minilm_model/minilm_headings.onnx", help="Path to the ONNX model file.")
    parser.add_argument("--tokenizer_path", type=str, default="minilm_tokenizer", help="Path to the tokenizer directory.")
    
    args = parser.parse_args()

    INPUT_DIR = args.pdf_dir
    OUTPUT_DIR = args.output_dir
    SCHEMA_PATH = args.schema
    MODEL_PATH = args.model_path
    TOKENIZER_PATH = args.tokenizer_path

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Initialize classifier
    classifier = HeadingClassifier(MODEL_PATH, TOKENIZER_PATH)
    logger.info("HeadingClassifier initialized.")

    # Load schema if provided
    schema = None
    if SCHEMA_PATH and os.path.exists(SCHEMA_PATH):
        schema = load_schema(SCHEMA_PATH)
        logger.info(f"Schema loaded from {SCHEMA_PATH}")
    elif SCHEMA_PATH:
        logger.warning(f"Schema file not found at {SCHEMA_PATH}, proceeding without schema validation.")

    # Process PDFs
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    if not pdf_files:
        logger.warning(f"No PDF files found in {INPUT_DIR}.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        process_pdf(pdf_path, OUTPUT_DIR, classifier, schema)

    logger.info("PDF processing complete.")

if __name__ == "__main__":
    main()

