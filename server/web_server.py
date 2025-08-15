from flask import Flask, request, jsonify
from agents.agent_system import AgentSystem

app = Flask(__name__)

# Create agent system
agent_system = AgentSystem('web')

@app.route('/')
def index():
    return open('templates/index.html').read()  

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')
    
    # Process the user's message with agent system
    ai_response = agent_system.send_message(user_message)
    
    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)

