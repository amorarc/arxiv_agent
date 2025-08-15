from arxiv2text import arxiv_to_md, arxiv_to_text
from camel.toolkits import ArxivToolkit
from camel.agents import ChatAgent
from pydantic import BaseModel


# First template for arxiv queries
class ArxivQueryTemplate(BaseModel):
    query: str
    max_num: int 


# Second template for paper template
class ArxivPaperTemplate(BaseModel):
    title: str
    url: str
    abstract: str



# Arxiv agent class
class ArxivAgent(ChatAgent):
    def __init__(self, model):
        system_message = """
        You are an Arxiv query agent.
        """
        self.query_arxiv_message = " You will receive a search query and you will have to extract the information to format it to return a (query : string) and the maximun search limit (max_num : int)."
        self.similarity_message = " You will receive a bunch of papers. Select the one that fits more with teh description given and return its title, url and abstract."
        # Coordinator agent
        super().__init__(
            system_message=system_message,
            model=model,
            output_language='english',
            message_window_size=2,
        )
        self.arxiv_tool = ArxivToolkit()
        self.searched = {}
    
    # Request from a topic and obtain realted arxiv papers 
    def request_papers(self, message : str, verbose : bool = False):
        """
        Handles the process of searching for papers on arXiv based on a user-provided topic or query.

        Args:
            message (str): The topic or search query provided by the user.
            verbose (bool): If True, prints debugging messages.

        Returns:
            List[dict]: A list of search results from arXiv, each containing paper metadata.
        """
        query_created = False
        if verbose:
            print('ARXIV_AGENT: Creating query...')
        # Try to create the corresponding query
        while not query_created:
            parsed = super().step(f"{self.query_arxiv_message}\n\n Query: {message}\n\n Answer: ", ArxivQueryTemplate).msgs[0].parsed
            query_created = type(parsed) == ArxivQueryTemplate
            if verbose and not query_created:
                    print('ARXIV_AGENT: Failed creating query, retrying...')
        if verbose:
            print(f'ARXIV_AGENT: Query created! ({parsed})')
        search =  self.arxiv_tool.search_papers(parsed.query, max_results=max(1, parsed.max_num))

        message = f"Here you have the recent {max(1, parsed.max_num)} papers about '{parsed.query.capitalize()}':\n\n"

        # Accomodate info
        for paper in search:
             message += f'Title : {paper['title']}.\n'
             message += f'Date : {paper['published_date']}.\n'
             message += f'Authors : {", ".join(paper['authors'])}.\n'
             message += f'URL : {paper['pdf_url']}.\n\n'
             if paper['title'] not in self.searched:
                  self.searched[paper['title']] = paper

        return message

    def retrieve_full_paper(self, message : str, verbose : bool = False):
        """
        Handles the process of retrieving the full content of a specific paper selected
        from the previously searched results.

        Args:
            message (str): A description or selection criteria for the desired paper.
            verbose (bool): If True, prints debugging messages.

        Returns:
            str: The full paper content, either in Markdown or plain text format.
        """
        query_created = False
        if verbose:
            print('ARXIV_AGENT: Finding paper...')
        # Try to create the corresponding query
        papers = "\n"
        for paper in self.searched.values():
             papers += f"title: {paper['title']}\n"
             papers += f"url: {paper['pdf_url']}\n"
             papers += f"abstract: {paper['summary']}\n\n"
        while not query_created:
            parsed = super().step(f"{self.similarity_message}\n\nPapers: {papers}\n\nDescription{message}", ArxivPaperTemplate).msgs[0].parsed
            query_created = type(parsed) == ArxivPaperTemplate
            if verbose and not query_created:
                    print('ARXIV_AGENT: Failed founding paper, retrying...')
        if verbose:
            print(f'ARXIV_AGENT: Paper found! ({parsed.title})')
            print(f'ARXIV_AGENT: Obtaining paper in markdown format...')

        try:
            paper_parsed = arxiv_to_md(parsed.url, "cache/")
        except:
            print(f'ARXIV_AGENT: Failed obtaining paper in markdown format. Trying in text format...')
            paper_parsed = arxiv_to_text(parsed.url, "cache")

        return paper_parsed
