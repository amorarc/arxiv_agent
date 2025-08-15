from camel.agents import ChatAgent



class ScientistAgent(ChatAgent):
    def __init__(self, model):
        system_message = """
        You are an Scientist agent that reads many Arxiv papers.
        """
        self.instruction = "Given the following Arxiv paper text, answer the question and always mention the lines where you found the information to answer the order."
        # Coordinator agent
        super().__init__(
            system_message=system_message,
            model=model,
            output_language='english',
            message_window_size=2,
        )
    
    def write(self, question : str, previous_info : str = "", rethink : int = 3, verbose : bool = False):
        """
        Analyzes a given question and generates a solution based on previous information. The method can optionally rethink
        the solution a specified number of times to refine or improve the answer.

        Args:
            question (str): The primary question or task to be answered or addressed by the agent.
            previous_info (str, optional): Previous context or information to consider when generating the solution. Defaults to an empty string.
            rethink (int, optional): The number of times to re-evaluate or refine the initial solution. Defaults to 0 (no rethinking).
            verbose (bool, optional): If True, enables verbose output to track the process. Defaults to False.

        Returns:
            str: The final solution after any number of rethinking iterations.
        """
        if verbose:
            print('SCIENTIST_AGENT: Analysing paper...')
        solution = super().step(f"{self.instruction}\n{previous_info}\n\n Order: {question}").msgs[0].content
        for i in range(rethink):
            if verbose:
                print(f'SCIENTIST_AGENT: Partial solution found! Rethinking it... {i + 1}/{rethink}')
            solution = super().step(f"{self.instruction}\n{previous_info}\n\n Order: {question}\nYour insight is:\n{solution}\n\n Rethink it to answer the order.").msgs[0].content
        if verbose:
            print('SCIENTIST_AGENT: Solution found!')
        return solution

        