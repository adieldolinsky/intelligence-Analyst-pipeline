import sys
import os
import json
import fitz

def extract_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        text = ""

        for page in doc:
            text = text + page.get_text()
        return text
    except Exception as e:

        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_pdf.py <path_to_pdf>", file=sys.stderr)
        sys.exit(1)
    pdf_path = sys.argv[1]
    extracted_text = extract_pdf(pdf_path)

    file_name = os.path.basename(pdf_path)
    name_only, extension = os.path.splitext(file_name)
    file_type = extension.replace('.', '').lower()

    output_payload = {
        "file_name": name_only,
        "file_type": file_type,
        "text": extracted_text
    }

    print(json.dumps(output_payload))