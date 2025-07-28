from transformers import AutoTokenizer

# Download the pretrained tokenizer from the HuggingFace model hub
tokenizer = AutoTokenizer.from_pretrained("microsoft/MiniLM-L6-v2")

# Save all necessary tokenizer files into the folder "minilm_tokenizer"
tokenizer.save_pretrained("minilm_tokenizer")

print("Tokenizer files saved to ./minilm_tokenizer/")
