from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, DallETool
from langchain_openai import ChatOpenAI

from Write_A_Picture_Book.types import Chapter


@CrewBase
class WritingCrew:
    """Write Book Chapter Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    llm = ChatOpenAI(model="gpt-4o")
    dalle_tool = DallETool() 

    @agent
    def Story_Outline(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["Story_Outline_Agent"],
            tools=[search_tool],
            llm=self.llm,
            memory=True,
        )

    @agent
    def Scene_Description(self) -> Agent:
        return Agent(
            config=self.agents_config["Scene_Description_Agent"],
            llm=self.llm,
            #tools=[dalle_tool],
            memory=True,
        )
    
    @agent
    def Language_Simplification(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["Language_Simplification_Agent"],
            llm=self.llm,
            tools=[search_tool],
            memory=True,
        )

    @task
    def define_story_outline(self) -> Task:
        return Task(
            config=self.tasks_config["define_story_outline"], output_pydantic=Chapter
        )

    @task
    def draft_scene_descriptions(self) -> Task:
        return Task(config=self.tasks_config["draft_scene_descriptions"], )

    @task
    def simplify_language(self) -> Task:
        return Task(config=self.tasks_config["simplify_language"])
    
    @crew
    def crew(self) -> Crew:
        """Creates the Write Book Chapter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
