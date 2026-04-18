from flask import Flask, request, jsonify
from flask_cors import CORS
from app import analyze_site

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['GET'])
def analyze():
    """
    Endpoint to analyze a website's privacy and security features.
    """
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL parameter"}), 400

    try:
        # Analyze the website using the analyze_site function
        result = analyze_site(url)

        # Check if the analysis returned an error
        if not isinstance(result, dict):
            return jsonify({"error": "Internal error: analyze_site did not return a dict"}), 500

        if 'error' in result:
            return jsonify({"error": result['error']}), 500

        # Ensure 'score' is present and valid
        score = result.get('score')
        if score is None or not isinstance(score, (int, float)):
            return jsonify({"error": "Analysis did not return a valid score."}), 500

        # Add a safety recommendation based on the score
        result['safety_recommendation'] = get_safety_recommendation(score)

        # Return the analysis results
        return jsonify(result), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"❌ An unexpected error occurred: {str(e)}"}), 500


def get_safety_recommendation(score):
    """
    Provide a safety recommendation based on the privacy score.
    """
    try:
        score = float(score)
    except Exception:
        return "⚠️ Unable to determine safety recommendation (invalid score)."

    if score >= 80:
        return "✅ This website is safe to use."
    elif score >= 50:
        return "⚠️ This website has moderate privacy risks. Be cautious."
    else:
        return "❌ This website is unsafe. Avoid sharing sensitive information."


if __name__ == '__main__':
    # Run the Flask server on port 5000
    app.run(port=5000, debug=True)
