#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import sys
import os
from cli_browser_agent import activate_browser_agent, call_gemini, search_pdf
from google import genai
from together import Together
import weave

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize Weave
weave.init('metis')

# Set up API clients
def initialize_clients():
    api_key = os.getenv("GEMINI_API_KEY")
    together_api_key = os.getenv("TOGETHER_API_KEY")
    
    if not api_key or not together_api_key:
        raise ValueError("Please set GEMINI_API_KEY and TOGETHER_API_KEY environment variables")
    
    google_client = genai.Client(api_key=api_key)
    together_client = Together(api_key=together_api_key)
    
    return google_client, together_client

try:
    GOOGLE_CLIENT, TOGETHER_CLIENT = initialize_clients()
except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    try:
        data = request.get_json()
        user_task = data.get('query', '').strip()
        
        if not user_task:
            return jsonify({'response': 'Please provide a task', 'steps': ''}), 400
        
        search_result = search_pdf(user_task, "pdf_instructions_correct2")
        file_path = search_result['pdf_name'] + ".pdf" if search_result else None
        
        with weave.attributes({'user_intent': user_task, 'doc_file': file_path}):
            response = call_gemini(GOOGLE_CLIENT, user_task, file_path)
        
        if response.function_calls:
            steps = response.function_calls[0].args.get('steps', '')
            agent_response = activate_browser_agent(TOGETHER_CLIENT, steps, user_task)
            return jsonify({
                'response': agent_response['result'],
                'steps': agent_response['steps']
            })
        else:
            return jsonify({
                'response': response.text,
                'steps': ''
            })
            
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}', 'steps': ''}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
