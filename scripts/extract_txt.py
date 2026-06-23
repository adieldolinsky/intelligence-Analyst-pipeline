import sys
import os
import json

def extract_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 extract_txt.py <path_to_txt>", file=sys.stderr)
        sys.exit(1)

    txt_path = sys.argv[1]

    extracted_text = extract_txt(txt_path)
    file_name = os.path.basename(txt_path)
    name_only, extension = os.path.splitext(file_name)
    file_type = extension.replace('.', '').lower()

    output_payload = {
        "file_name": name_only,
        "file_type": file_type,
        "text": extracted_text
    }

    print(json.dumps(output_payload))