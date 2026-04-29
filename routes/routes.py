# routes.py
from flask import Blueprint, request, jsonify, render_template

api_bp = Blueprint('api', __name__, url_prefix='/api')
web_bp = Blueprint('web', __name__, url_prefix='/')

agent = None

def init_agent(agent_instance):
    global agent
    agent = agent_instance


@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify(agent.health_check())


@api_bp.route('/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "Message required"}), 400
        
        result = agent.generate_response(message)
        
        if result['success']:
            return jsonify({"response": result['response']})
        else:
            return jsonify({"error": result['response']}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@web_bp.route('/', methods=['GET', 'POST'])
def home():
    response = None
    last_message = None
    
    if request.method == 'POST':
        last_message = request.form.get('message')
        if last_message:
            result = agent.generate_response(last_message)
            if result['success']:
                response = result['response']
            else:
                response = result['response']
    
    return render_template('index.html', 
                         response=response, 
                         last_message=last_message)