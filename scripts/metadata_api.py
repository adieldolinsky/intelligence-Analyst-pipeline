from flask import Flask, request, jsonify
import uuid
import datetime


app = Flask(__name__)

# ==========================================
# Helper Functions (Business Logic)
# ==========================================
def determine_sensitivity(classification, entities_str):
    """Core logic for document sensitivity"""
    if classification in ['article', 'marketing', 'public_notice']:
        return 'public'
    elif 'amount' in entities_str.lower() or '$' in entities_str:
        return 'confidential'
    else:
        return 'internal'

# ==========================================
# API Routes
# ==========================================

# --- GET /health ---
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

# --- GET /categories ---
@app.route('/categories', methods=['GET'])
def categories():
    return jsonify({
        "categories": ["invoice", "report", "contract", "ticket", "article", "other"]
    })


# --- POST /sensitivity ---
@app.route('/sensitivity', methods=['POST'])
def check_sensitivity():
    data = request.json
    # Extract needed variables from the JSON payload
    classification = data.get('classification', 'other')
    entities = str(data.get('entities', {}))
    sensitivity = determine_sensitivity(classification, entities)
    return jsonify({"sensitivity": sensitivity})


# --- POST /enrich ---
@app.route('/enrich', methods=['POST'])
def enrich():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        classification = data.get('classification', 'other')

        # Safe float conversion
        try:
            confidence_score = float(data.get('confidence_score', 0.0))
        except ValueError:
            confidence_score = 0.0

        entities = data.get('entities', {})

        # 1. Map classification to department
        dept_map = {
            'invoice': 'Finance',
            'contract': 'Legal',
            'report': 'Management',
            'ticket': 'IT Support',
            'article': 'Marketing'
        }
        department = dept_map.get(classification, 'General')

        # 2. Assign sensitivity based on entities
        sensitivity = determine_sensitivity(classification, str(entities))

        # 3. Confidence score adjustment
        if not entities.get('people'):
            confidence_score -= 0.1

        # 4. Generate routing tags
        if confidence_score < 0.4:
            routing_tag = 'escalate'
        elif confidence_score < 0.7:
            routing_tag = 'needs-review'
        else:
            routing_tag = 'auto-approved'

        # 5. Build enriched response with UUID and Timestamp
        enriched_data = {
            'document_id': str(uuid.uuid4()),
            'department': department,
            'sensitivity': sensitivity,
            'routing_tag': routing_tag,
            'adjusted_confidence': round(confidence_score, 2),
            'processed_at': datetime.datetime.utcnow().isoformat()
        }

        return jsonify(enriched_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=5000, debug=debug)