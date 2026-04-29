# app.py
from flask import Flask
from common.llm.llama_agent import LlamaAgent
from routes.routes import api_bp, web_bp, init_agent

app = Flask(__name__)
app.secret_key = 'secret'

# Initialize agent
print("Connecting to Llama Stack...")
agent = LlamaAgent(
    base_url="http://localhost:8321/v1",
    api_key="fake",
    model_id="llama3.2:3b-instruct-fp16",  # Use the exact model from your working example
    enable_guardrails=True  # Set to False to disable guardrails
)
init_agent(agent)

# Register blueprints
app.register_blueprint(api_bp)
app.register_blueprint(web_bp)

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("Server running at: http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)