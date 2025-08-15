from typing import Literal
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from agents.arxiv_agent import ArxivAgent
from agents.coord_agent import CoordinatorAgent
from agents.scientist_agent import ScientistAgent
from agents.format_agent import FormatAgent



class AgentSystem:

    def __init__(self, env : Literal['terminal', 'web']):

        # Set environment for the chat
        self.env = env

        # Load model
        self.model = ModelFactory.create(
            model_platform=ModelPlatformType.OLLAMA,
            model_type="llama3.2",
            #url="http://localhost:11434/v1", # Ana aquí puedes poner la url del modelo!!
            model_config_dict={"temperature": 0.4, "max_tokens" : 999_999_999},
        )

        # Agent system needs a coordinator
        self.coordinator_agent = CoordinatorAgent(self.model)
        # Agent system needs a searcher
        self.arxiv_agent = ArxivAgent(self.model)
        # Agent system needs a scientist
        self.scientist_agent = ScientistAgent(self.model)

        # Agent system needs a formatter
        self.formatter_agent = FormatAgent(self.model, self.env)

        # Dictionary for mapping agents
        self.agent_dict = {'ARXIV_AGENT' : self.arxiv_agent, 'SCIENTIST_AGENT' : self.scientist_agent, 'COORDINATOR_AGENT' : self.coordinator_agent}
        # Dictionary for mapping actions
        self.action_dict = {'request_papers' : self.arxiv_agent.request_papers, 
                      'retrieve_full_paper' : self.arxiv_agent.retrieve_full_paper,
                      'write' : self.scientist_agent.write,
                      'end' : 'Bye!'
                      }

        # Verbose of the agents
        self.verbose = env == 'web'

    # Set verbose
    def set_verbose(self, decision : bool):
        self.verbose = decision
    
    # Set language
    def set_language(self, language : str):
        self.formatter_agent.set_output_language(language)
    
    # Reset all agents
    def reset_system(self):
        self.coordinator_agent.reset()
        self.arxiv_agent.reset()
        self.scientist_agent.reset()
    
    def postprocess_message(self, message : str):
        return message.replace('\n', '<br>').replace('\t', '&emsp;&emsp;')

    # Send message to the system
    def send_message(self, message : str):
        # Manage commands
        if message[0] == '/':
            answer = self.manage_command(message)
        else:
            answer = self.manage_message(message)
        if self.env == 'web':
            formatted_answer = self.formatter_agent.format(self.postprocess_message(answer))
        else:
            formatted_answer = self.formatter_agent.format(answer)
        
        return formatted_answer
    
    # Manage commands
    def manage_command(self, command : str):
        if command == '/help':
            return "SYSTEM: available commands are \n/reset\n/verbose\n/set_spanish\n/set_english"
        elif command == '/reset':
            self.reset_system()
            return "SYSTEM: all agents have been reseted."
        elif command == '/verbose':
            if self.env == 'terminal':
                self.set_verbose(not self.verbose)
                return f"SYSTEM: {"verbose is activated" if self.verbose else "verbose is deactivated"}." 
            else:
                return "SYSTEM: verbose cannot be activated in terminal env. Switch to web." 
        elif command == '/set_spanish':
            self.set_language('spanish')
            return "SYSTEM: language changed to spanish." 
        elif command == '/set_english':
            self.set_language('english')
            return "SYSTEM: language changed to english." 
        else:
            return f"SYSTEM: command '{command}' not found." 
    
    # Manage message received by user
    def manage_message(self, message : str):
        coordinator_reponse = self.coordinator_agent.coordinate(message, self.verbose)
        needed_agent = coordinator_reponse.agent
        action = coordinator_reponse.action

        # Correct agent has teh message to process
        if action == 'write':
            return self.scientist_agent.write(message, self.paper_info, verbose=self.verbose)
        elif action == 'request_papers':
            return  self.arxiv_agent.request_papers(message, self.verbose)
        elif action == 'retrieve_full_paper':
            self.paper_info = self.arxiv_agent.retrieve_full_paper(message, self.verbose)
            return self.paper_info + "\nNow you can ask me about this paper!"
        else:
            return "Sorry, can you rephrase what you want me to do it? I don't understand you."

