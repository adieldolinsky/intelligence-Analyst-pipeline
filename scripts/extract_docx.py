import  sys
import os
import json
from docx import Document

def extract_docx(file_path):
    try:
        doc = Document(file_path)
        text= "\n".join([para.text for para in doc.paragraphs])
        return text

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_docx.py <path_to_docx>", file=sys.stderr)
        sys.exit(1)

    docx_path = sys.argv[1]
    extracted_text = extract_docx(docx_path)

    file_name = os.path.basename(docx_path)
    name_only, extension = os.path.splitext(file_name)
    file_type = extension.replace('.', '').lower()

    output_payload = {
        "file_name": name_only,
        "file_type": file_type,
        "text": extracted_text
    }

    print(json.dumps(output_payload))