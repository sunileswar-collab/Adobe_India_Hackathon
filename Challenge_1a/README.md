# 🧠 Adobe Hackathon 2025 - Challenge 1A  
### 🚀 Round 1A: Understand Your Document  
**Theme:** Connecting the Dots Through Docs  

---

## 📌 Objective

Extract a structured outline from a PDF document, mimicking how a machine would "understand" the content. The outline includes:
- A **document title**
- A hierarchical list of headings: **H1**, **H2**, and **H3**
- **Page number** for each heading

---

## 🛠️ What This Solution Does

✅ Accepts multiple PDF files from the `/app/input` directory  
✅ Extracts:
- Title (best matching prominent H1 or H2)
- Hierarchical headings (H1, H2, H3) with page numbers  
✅ Produces a valid `JSON` output for each PDF  
✅ Works fully **offline**  
✅ Fast: Processes a 50-page PDF in under **10 seconds**  
✅ Dockerized and compatible with **amd64** (x86_64) systems  
✅ Lightweight model (≤200MB) using **ONNX**  

---

