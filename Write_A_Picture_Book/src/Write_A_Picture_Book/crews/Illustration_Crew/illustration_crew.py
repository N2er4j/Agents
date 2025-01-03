from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, DallETool
from langchain_openai import ChatOpenAI

from Write_A_Picture_Book.types import Chapter


@CrewBase
class IllustrationCrew:
    """Illustration Book Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o")
    dalle_tool = DallETool() 

    @agent
    def Scene_Description(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["Scene_Description_Agent"],
            tools=[search_tool],
            llm=self.llm,
            memory=True,
        )

    @agent
    def Illustration(self) -> Agent:
        return Agent(
            config=self.agents_config["Illustration_Agent"],
            llm=self.llm,
            tools=[dalle_tool],
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
    def draft_scene_descriptions(self) -> Task:
        return Task(
            config=self.tasks_config["draft_scene_descriptions"],
        )

    @task
    def create_illustration_concepts(self) -> Task:
        return Task(config=self.tasks_config["create_illustration_concepts"],)

    
    @crew
    def crew(self) -> Crew:
        """Creates the Write Book Chapter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
