# שימוש בגרסת v1.x ספציפית ויציבה שכוללת את apk
FROM n8nio/n8n:1.40.0

USER root

# התקנת פייתון כרגיל
RUN apk update && apk add --no-cache python3 py3-pip

# יצירת סביבה וירטואלית
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# התקנת הספריות של פייתון
RUN pip install --no-cache-dir PyMuPDF pdfplumber requests python-docx --break-system-packages

USER node