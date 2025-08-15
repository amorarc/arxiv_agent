from typing import Literal
from camel.agents import ChatAgent
from pydantic import BaseModel


# Template needed for coordination
class TaskTemplate(BaseModel): 
    agent: Literal['ARXIV_AGENT', 'SCIENTIST_AGENT', 'COORDINATOR_AGENT']
    action : Literal['request_papers', 'retrieve_full_paper', 'write', 'END'] 


# Coordinator agent class
class CoordinatorAgent(ChatAgent):
    def __init__(self, model):
        system_message = """
        You are an Coordinator agent that receives a goal and selects the best agent and action of the next task.
        """
        self.instruction = """
        You will be given some previous tasks. Return the following task needed to be done in order to achieve the goal. You have available agents with functionalities:
        ARXIV_AGENT: If you need to retrieve or search info, use this agent.
        - 'request_papers': searchs on the web to retrieve/find/give papers
        - 'retrieve_full_paper': obtains information about a paper. You must use the action if the message starts with 'Retrieve the full paper of ...'
         
        SCIENTIST_AGENT: If you want to analyse data or make great conlusions, use this agent. Always if it's a question
        - 'write': can answer questions from a paper, analyse a paper, summarize a paper, and operate with it. 

        Example:
        agent: Literal['ARXIV_AGENT', 'SCIENTIST_AGENT']
        action : Literal['request_papers', 'retrieve_full_paper', 'write']  

        Note: When you achieve your goal or you don't have anything to say, return 
        agent: "COORDINATOR_AGENT"
        action : "END"

        Note: the order must only contain information of the task assigned, not of the whole goal
        """
        # Coordinator agent
        super().__init__(
            system_message=system_message,
            model=model,
            output_language='english',
            message_window_size=4,
        )
    
    def coordinate(self, message : str , verbose : bool = False):

        query_created = False
        if verbose:
            print('COORDINATOR_AGENT: Creating task...')


        # Try to create the corresponding task
        while not query_created:
            parsed = super().step(f"{self.instruction}\n\nGoal: {message}\n\n Next task:\n", TaskTemplate).msgs[0].parsed
            query_created = type(parsed) == TaskTemplate
            if verbose and not query_created:
                    print('COORDINATOR_AGENT: Failed creating task, retrying...')
        if verbose:
            print(f'COORDINATOR_AGENT: Task created! ({parsed})')
        return parsed