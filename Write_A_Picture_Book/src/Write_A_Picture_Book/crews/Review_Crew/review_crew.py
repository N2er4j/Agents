from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, DallETool
from langchain_openai import ChatOpenAI

from Write_A_Picture_Book.types import Chapter


@CrewBase
class ReviewCrew:
    """Write Book Chapter Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o")
    dalle_tool = DallETool() 

    @agent
    def Educational_Alignment(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["Educational_Alignment_Agent"],
            tools=[search_tool],
            llm=self.llm,
            memory=True,
        )

    @agent
    def Final_Review(self) -> Agent:
        return Agent(
            config=self.agents_config["Final_Review_Agent"],
            llm=self.llm,
            #tools=[dalle_tool],
            memory=True,
        )
    
    '''
    @agent
    def image_tool(self) -> Agent:
        return Agent(
            config=self.agents_config["photographer"],
            llm=self.llm,
            tools=[DallETool()],
            memory=True,
        )
    '''

    @task
    def align_with_educational_goals(self) -> Task:
        return Task(
            config=self.tasks_config["align_with_educational_goals"],
        )

    @task
    def review_and_finalize(self) -> Task:
        return Task(config=self.tasks_config["review_and_finalize"],)

    '''
    @task
    def create_image(self) -> Task:
        return Task(config=self.tasks_config["create_image"])
    '''
    
    @crew
    def crew(self) -> Crew:
        """Creates the Write Book Chapter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
