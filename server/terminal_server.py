from agents.agent_system import AgentSystem

# Create agent system
agent_system = AgentSystem('terminal')

# Start chat
while True:
    my_message=input('User: ')
    reponse = agent_system.send_message(my_message)
    print(f"Agent: {reponse}")
