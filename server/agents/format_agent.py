from camel.agents import ChatAgent


class FormatAgent(ChatAgent):
    def __init__(self, model, env):

        text_type = "HTML paragraph" if env == 'web' else 'terminal'
        system_message = f"""
        You are an Agent that rewrites raw text into {text_type} text. You love to make text clear and spaced.
        """
        self.instruction = f"Given the following raw text, make the necessary changes to adapat it to {text_type}. Use bold for highlight important parts. Do not delete information, just transform it. Do not tell me 'Here is the transformed text ...'"
        # Coordinator agent
        super().__init__(
            system_message=system_message,
            model=model,
            output_language='english',
            message_window_size=2,
        )
    
    def format(self, message : str, verbose : bool = False):
        if verbose:
            print('FORMAT_AGENT: formatting message...')
        formatted_text = super().step(f"{self.instruction}\n\n Raw text: {message}\n\n").msgs[0].content.replace("Here is the transformed text:", "").replace("here is the transformed text:", "")
        if verbose:
            print('FORMAT_AGENT: Message formatted!')
        return formatted_text

        