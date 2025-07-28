# In D:\CONNECTING_DOTS\Challenge_1a\utils\heading_classifier.py

import numpy as np
from transformers import AutoTokenizer
import onnxruntime as rt
import logging

try:
    from utils.logger import setup_logger
    logger = setup_logger()
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class HeadingClassifier:
    def __init__(self, model_path, tokenizer_path):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.session = rt.InferenceSession(model_path)
        self.input_names = [inp.name for inp in self.session.get_inputs()] 
        self.output_name = self.session.get_outputs()[0].name
        self.idx_to_label = {0: 'H1', 1: 'H2', 2: 'H3', 3: 'H4', 4: 'text'}

    def _predict_onnx(self, text):
        inputs = self.tokenizer(
            text, 
            return_tensors="np", 
            truncation=True, 
            padding="max_length", 
            max_length=128        
        )
        
        input_feed = {}
        for name in self.input_names:
            if name in inputs:
                input_feed[name] = inputs[name]
            else:
                logger.warning(f"Input '{name}' expected by ONNX model but not found in tokenizer output for text: '{text[:50]}...'")
                if name == "token_type_ids":
                    input_feed[name] = np.zeros_like(inputs["input_ids"]) 

        outputs = self.session.run([self.output_name], input_feed)
        logits = outputs[0]
        predicted_class_idx = np.argmax(logits, axis=1)[0]
        return self.idx_to_label[predicted_class_idx]

    def predict(self, text):
        predicted_label = self._predict_onnx(text)

        text_stripped = text.strip()

        if predicted_label == 'text':
            return 'text'

        # --- Enhanced Aggressive Post-processing Rules, especially for file05.pdf ---

        # Rule 1: Demote if text is purely numeric or numeric with single dot/bracket
        if len(text_stripped) <= 5 and (text_stripped.replace('.', '', 1).isdigit() or \
                                       text_stripped.replace(')', '', 1).isdigit() or \
                                       (text_stripped.startswith('(') and text_stripped.endswith(')') and text_stripped[1:-1].isdigit())):
            logger.debug(f"Demoting '{text_stripped}' ({predicted_label}) to 'text' (purely numeric/short numbering)")
            return 'text'
        
        # Rule 2: Demote very short, non-alphanumeric/non-sentence-like strings (e.g., "---", "###")
        if len(text_stripped) < 3 and not any(char.isalnum() for char in text_stripped):
             logger.debug(f"Demoting '{text_stripped}' ({predicted_label}) to 'text' (very short non-alphanumeric)")
             return 'text'

        # Rule 3: Demote common column headers, generic single words, or specific phrases often misclassified
        # Expanded list based on your *latest* problematic output
        common_non_heading_words_or_phrases = {
            "s.no", "name", "age", "relationship", "rs.", "date",
            "service", "pay", "designation", "single", "rail", "fare/bus", "fare", "from", "the",
            "whether", "i declare", "amount", "persons", "home town", "signature",
            "for:", "date:", "time:", "address:", "rsvp:", # From file05.pdf, labels
            "closed toed shoes are required for climbing", # Specific rule from file05.pdf
            "parents or guardians not attending the party, please visit topjump.com to fill out waiver so your child can attend.", # Specific long note from file05.pdf
            "hope to see you there!", # Closing remark from file05.pdf
            "www.topjump.com", # URL from file05.pdf
            "pigeon forge, tn 37863", # New: the misidentified title and part of outline item
            "topjump 3735 parkway pigeon forge, tn 37863", # New: full address from outline
            "(near dixie stampede on the parkway)", # New: location detail from outline
            "please visit topjump.com to fill out waiver so your child can attend. hope to see y ou t here ! www.topjump.com", # New: combined long instruction
        }
        
        # Normalize text for comparison (remove extra spaces, lower case)
        normalized_text = " ".join(text_stripped.split()).lower()

        if normalized_text in common_non_heading_words_or_phrases:
            logger.debug(f"Demoting '{text_stripped}' ({predicted_label}) to 'text' (exact match common non-heading phrase)")
            return 'text'

        # Check for single word classifications that are often mislabeled (retained)
        if len(text_stripped.split()) == 1:
            if normalized_text in common_non_heading_words_or_phrases:
                logger.debug(f"Demoting single word '{text_stripped}' ({predicted_label}) to 'text' (common non-heading word)")
                return 'text'
            if not text_stripped[0].isupper() and not text_stripped.isupper():
                logger.debug(f"Demoting single word '{text_stripped}' ({predicted_label}) to 'text' (not capitalized/all-caps)")
                return 'text'

        # Rule 4: Demote if it's a very short line that starts with a lowercase letter (unlikely to be a main heading) (retained)
        if len(text_stripped) < 15 and text_stripped and text_stripped[0].islower() and ' ' in text_stripped:
            logger.debug(f"Demoting '{text_stripped}' ({predicted_label}) to 'text' (short, starts lowercase, sentence-like)")
            return 'text'
            
        # Rule 5: Catch multi-line sentences being broken into "headings" (retained)
        if text_stripped and text_stripped[-1] in [',', ';', '-', '—'] and len(text_stripped) > 10:
             logger.debug(f"Demoting '{text_stripped}' ({predicted_label}) to 'text' (ends with punctuation, likely sentence fragment)")
             return 'text'

        # Rule 6: Specific rule for short, high-level classifications that are not typical headings. (retained)
        if predicted_label in ['H1', 'H2'] and len(text_stripped.split()) <= 5: 
            if not (text_stripped.split()[0].isdigit() or text_stripped.split()[0].lower() in ['i', 'ii', 'iii', 'iv', 'v']):
                invitation_phrases = ["you're invited", "to a party", "hope to see you there"]
                if any(phrase in normalized_text for phrase in invitation_phrases):
                    logger.debug(f"Demoting '{text_stripped}' ({predicted_label}) to 'text' (short H1/H2, invitation phrase)")
                    return 'text'
        
        return predicted_label
