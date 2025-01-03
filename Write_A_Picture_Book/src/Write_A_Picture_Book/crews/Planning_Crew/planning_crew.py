from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import os

from Write_A_Picture_Book.types import BookOutline

google_api_key = os.environ.get("GOOGLE_API_KEY")
print(google_api_key)
gemini_llm = LLM(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-1.5-flash",
)

@CrewBase
class PlanningCrew:
    """Book Outline Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = gemini_llm
    @agent
    def Story_Outline(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["Story_Outline_Agent"],
            tools=[search_tool],
            llm=self.llm,
            memory=True,
            verbose=True,
        )

    @agent
    def Character_Design(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["Character_Design_Agent"],
            tools=[search_tool],
            llm=self.llm,
            memory=True,
            verbose=True,
        )

    @task
    def define_story_outline(self) -> Task:
        return Task(
            config=self.tasks_config["define_story_outline"],
        )

    @task
    def design_characters(self) -> Task:
        return Task(
            config=self.tasks_config["design_characters"], output_pydantic=BookOutline
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Book Outline Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            delegation=False,
            process=Process.sequential,
            verbose=True,
        )
