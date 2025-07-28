# Assuming this is D:\CONNECTING_DOTS\Challenge_1a\utils\pdf_utils.py

import fitz # PyMuPDF
import logging

try:
    from utils.logger import setup_logger
    logger = setup_logger()
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

def extract_text_lines(pdf_path):
    """
    Extracts text lines from a PDF, including their page number and bounding box.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of dictionaries, each containing 'text', 'page_no', and 'bbox'.
              'bbox' is a tuple (x0, y0, x1, y1) representing the bounding box.
    """
    lines_data = []
    try:
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc):
            # page_num is 0-indexed, so add 1 for page_no
            current_page_no = page_num + 1 
            
            # This extracts text blocks. We want lines, so further processing is needed.
            # PyMuPDF's get_text("dict") or get_text("rawdict") are useful for structured extraction.
            # Using get_text("dict") provides blocks, lines, and spans.
            page_dict = page.get_text("dict") # Extract as dictionary
            
            for block in page_dict['blocks']:
                if block['type'] == 0: # Text block
                    for line in block['lines']:
                        full_line_text = " ".join([span['text'].strip() for span in line['spans']]).strip()
                        if full_line_text: # Only add non-empty lines
                            # Get the bounding box for the entire line
                            bbox = (line['bbox'][0], line['bbox'][1], line['bbox'][2], line['bbox'][3])
                            lines_data.append({
                                'text': full_line_text,
                                'page_no': current_page_no,
                                'bbox': bbox # Optional, but good to include if needed later
                            })
        doc.close()
        logger.debug(f"Successfully extracted {len(lines_data)} lines from {pdf_path}")
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
        # Return empty list or re-raise, depending on desired error handling
        return []
    return lines_data

