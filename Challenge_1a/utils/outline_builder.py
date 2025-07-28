# In D:\CONNECTING_DOTS\Challenge_1a\utils\outline_builder.py

import logging
try:
    from utils.logger import setup_logger
    logger = setup_logger()
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

def build_outline(lines_with_preds):
    outline = []
    
    current_heading = None
    
    for i, line in enumerate(lines_with_preds):
        level = line.get('heading_level')
        text = line.get('text', '').strip()
        
        # --- CRITICAL CHANGE HERE ---
        # Ensure page_no is an integer. Default to 1 if missing or invalid, 
        # but ideally, this indicates an issue with extract_text_lines.
        page_no = line.get('page_no')
        if page_no is None:
            # Log a warning to debug why page_no is missing from lines_with_preds
            logger.warning(f"Line {i} ('{text[:50]}...') is missing 'page_no'. Defaulting to 1.")
            page_no = 1 # Provide a default valid integer
        elif not isinstance(page_no, int) or page_no < 1:
            logger.warning(f"Line {i} ('{text[:50]}...') has invalid 'page_no' ({page_no}). Converting to int or defaulting to 1.")
            try:
                page_no = int(page_no)
                if page_no < 1:
                    page_no = 1
            except (ValueError, TypeError):
                page_no = 1 # Fallback if conversion fails

        # --- (rest of your existing filtering logic in outline_builder.py) ---
        # Rule 1: Only include actual heading levels (H1-H4)
        if level not in ['H1', 'H2', 'H3', 'H4']:
            continue # Skip if not a recognized heading level

        # Rule 2: Exclude specific patterns that are often misclassified as headings but are not desired in outline
        if len(text) <= 3 and text.replace('.', '', 1).isdigit(): # "1.", "2.", "3."
            continue
        if len(text.split()) <= 1 and not text.isupper() and not text.istitle(): # Single non-capitalized words
            continue
        common_non_headings = ["S.No", "Name", "Age", "Relationship", "Rs.", "Date", "Service", "PAY", "Single", "rail", "fare/bus", "fare", "from", "the"]
        if text in common_non_headings:
            continue

        # Rule 3: Check for blank or almost blank "headings"
        if not text or len(text) < 2: # Exclude very short or empty strings
            continue

        # Rule 4: If an H1 or H2 is just a single word that doesn't look like a real heading
        blacklist_words = ["Service", "PAY", "Single", "rail", "fare/bus", "fare", "from", "the", "S.No", "Name", "Age", "Relationship", "Rs.", "Date"]
        if level in ['H1', 'H2'] and text in blacklist_words:
            continue
        # --- (End of filtering logic) ---

        # If it passes all filters, proceed to build/merge heading
        
        # Check for multi-line headings (your merging logic)
        if current_heading and \
           current_heading['level'] == level and \
           current_heading['page_no'] == page_no and \
           (len(current_heading['text'].split()) < 10 or current_heading['text'].endswith(('.', '-', ':', ';', ','))):
            
            if len(text) > 2:
                current_heading['text'] += " " + text
            logger.debug(f"Merged line into previous heading: {current_heading['text']}")
        else:
            if current_heading:
                outline.append(current_heading)
            
            # This is where the new heading is created
            current_heading = {
                "level": level,
                "text": text,
                "page_no": page_no # Ensure the now-validated page_no is used here
            }
            logger.debug(f"Started new heading: {current_heading}")

    if current_heading:
        outline.append(current_heading)

    # Post-processing the final outline (your existing logic)
    final_outline = []
    i = 0
    while i < len(outline):
        item = outline[i]
        merged = False
        if i + 1 < len(outline):
            next_item = outline[i+1]
            # Ensure page_no is valid before comparison in post-processing merge
            # This should already be handled by the pre-check above, but good to be safe.
            if item['level'] == next_item['level'] and \
               item['page_no'] == next_item['page_no'] and \
               (item['text'].endswith(('.', '-', ':', ';', ',')) or len(next_item['text'].split()) < 5):
                
                item['text'] += " " + next_item['text']
                logger.debug(f"Post-processing merge: {item['text']}")
                merged = True
                i += 1 
        
        final_outline.append(item)
        i += 1

    return final_outline
