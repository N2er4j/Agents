import os

from crewai import Agent, Task, Process, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.llms import Ollama

# To Load Local models through Ollama
#mistral = Ollama(model="mistral")

# To Load GPT-4
api = os.environ.get("OPENAI_API_KEY")

# To load gemini (this api is for free: https://makersuite.google.com/app/apikey)
api_gemini = os.environ.get("GEMINI_API_KEY")
print(api_gemini)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=api_gemini
    #model="models/gemini/gemini-1.5-pro", verbose=True, temperature=0.1, google_api_key=api_gemini
)
'''
marketer = Agent(
    role="Market Research Analyst",
    goal="Find out how big is the demand for my products and suggest how to reach the widest possible customer base",
    backstory="""You are an expert at understanding the market demand, target audience, and competition. This is crucial for 
		validating whether an idea fulfills a market need and has the potential to attract a wide audience. You are good at coming up
		with ideas on how to appeal to widest possible audience.
		""",
    verbose=True,  # enable more detailed or extensive output
    allow_delegation=True,  # enable collaboration between agent
    #   llm=llm # to load gemini
)

technologist = Agent(
    role="Technology Expert",
    goal="Make assessment on how technologically feasable the company is and what type of technologies the company needs to adopt in order to succeed",
    backstory="""You are a visionary in the realm of technology, with a deep understanding of both current and emerging technological trends. Your 
		expertise lies not just in knowing the technology but in foreseeing how it can be leveraged to solve real-world problems and drive business innovation.
		You have a knack for identifying which technological solutions best fit different business models and needs, ensuring that companies stay ahead of 
		the curve. Your insights are crucial in aligning technology with business strategies, ensuring that the technological adoption not only enhances 
		operational efficiency but also provides a competitive edge in the market.""",
    verbose=True,  # enable more detailed or extensive output
    allow_delegation=True,  # enable collaboration between agent
    #   llm=llm # to load gemini
)

business_consultant = Agent(
    role="Business Development Consultant",
    goal="Evaluate and advise on the business model, scalability, and potential revenue streams to ensure long-term sustainability and profitability",
    backstory="""You are a seasoned professional with expertise in shaping business strategies. Your insight is essential for turning innovative ideas 
		into viable business models. You have a keen understanding of various industries and are adept at identifying and developing potential revenue streams. 
		Your experience in scalability ensures that a business can grow without compromising its values or operational efficiency. Your advice is not just
		about immediate gains but about building a resilient and adaptable business that can thrive in a changing market.""",
    verbose=True,  # enable more detailed or extensive output
    allow_delegation=True,  # enable collaboration between agent
    #   llm=llm # to load gemini
)

task1 = Task(
    description="""Analyze what the market demand for plugs for holes in crocs (shoes) so that this iconic footware looks less like swiss cheese. 
		Write a detailed report with description of what the ideal customer might look like, and how to reach the widest possible audience. The report has to 
		be concise with at least 10 bullet points and it has to address the most important areas when it comes to marketing this type of business.
    """,
    agent=marketer,
    expected_output="""A detailed report with description of what the ideal customer might look like, and how to reach the widest possible audience. The report has to 
		be concise with at least 10 bullet points and it has to address the most important areas when it comes to marketing this type of business.""",
)

task2 = Task(
    description="""Analyze how to produce plugs for crocs (shoes) so that this iconic footware looks less like swiss cheese.. Write a detailed report 
		with description of which technologies the business needs to use in order to make High Quality T shirts. The report has to be concise with 
		at least 10  bullet points and it has to address the most important areas when it comes to manufacturing this type of business. 
    """,
    agent=technologist,
    expected_output="""A detailed report with description of which technologies the business needs  to use in order to make High Quality T shirts.""",

)

task3 = Task(
    description="""Analyze and summarize marketing and technological report and write a detailed business plan with 
		description of how to make a sustainable and profitable "plugs for crocs (shoes) so that this iconic footware looks less like swiss cheese" business. 
		The business plan has to be concise with 
		at least 10  bullet points, 5 goals and it has to contain a time schedule for which goal should be achieved and when.
    """,
    agent=business_consultant,
    expected_output="""A detailed business plan with description of how to make a sustainable and profitable business""",

)
'''
# Agent 1: Language Expert Agent
language_expert = Agent(
    role="Linguistic Specialist",
    goal="Ensure the assessments are linguistically accurate, grammatically correct, and aligned with proficiency levels.",
    backstory="""You are a linguist with extensive experience in teaching English as a Foreign Language (EFL). You are familiar with the Common European Framework of Reference for Languages (CEFR) 
        and have a deep understanding of language acquisition challenges. Your expertise lies in crafting materials that cater to learners at various levels, ensuring accuracy and relevance.
        Additional rules for Tools:
        -----------------
        1. Regarding the Action Input (the input to the action, just a simple python dictionary, enclosed
        in curly braces, using \" to wrap keys and values.)
        
        For example for the following schema:
        ```
        class ExampleToolInput(BaseModel):
          task: str = Field(..., description="The task to delegate")
          context: str = Field(..., description="The context for the task")
          coworker: str = Field(..., description="The role/name of the coworker to delegate to")
        ```
        Then the input should be a JSON object with the user ID:
        - task: The task to delegate
        - context: The context for the task
        - coworker: The role/name of the coworker to delegate to        
        """,
    verbose=True,  # Enable more detailed or extensive output
    allow_delegation=True,  # Enable collaboration between agents
    llm=llm,
)

task1 = Task(
    description="""Create a pool of 50 grammatically correct multiple-choice questions (MCQs) tailored for CEFR levels A1 to C2, 
        covering grammar, vocabulary, and reading comprehension.""",
    agent=language_expert,
    expected_output="""A document containing 50 MCQs categorized by CEFR levels.""",
)

# Agent 2: Pedagogical Strategist Agent
pedagogical_strategist = Agent(
    role="Assessment Design Specialist",
    goal="Design assessments that are pedagogically sound and effectively evaluate language skills (listening, speaking, reading, and writing).",
    backstory="""You are an experienced educator specializing in curriculum and assessment design. You have worked extensively with EFL learners, 
        creating balanced and engaging tests that accurately measure language proficiency. You ensure that assessments are diverse, covering all four key skills and incorporating innovative formats to keep learners engaged.
        Additional rules for Tools:
        -----------------
        1. Regarding the Action Input (the input to the action, just a simple python dictionary, enclosed
        in curly braces, using \" to wrap keys and values.)
        
        For example for the following schema:
        ```
        class ExampleToolInput(BaseModel):
          task: str = Field(..., description="The task to delegate")
          context: str = Field(..., description="The context for the task")
          coworker: str = Field(..., description="The role/name of the coworker to delegate to")
        ```
        Then the input should be a JSON object with the user ID:
        - task: The task to delegate
        - context: The context for the task
        - coworker: The role/name of the coworker to delegate to
        """,
    verbose=True,
    allow_delegation=True,
    llm=llm
)

task2 = Task(
    description="""Develop a comprehensive EFL assessment framework that includes listening, speaking, reading, and writing tasks, ensuring alignment with CEFR levels.""",
    agent=pedagogical_strategist,
    expected_output="""An assessment framework document with examples of tasks for each skill.""",
)

# Agent 3: Cultural Relevance Agent
cultural_relevance_agent = Agent(
    role="Cultural Content Specialist",
    goal="Ensure the assessment content is culturally sensitive, engaging, and globally relevant to diverse learner populations.",
    backstory="""You are a cultural expert with a background in sociolinguistics and international education. Your role is to incorporate culturally diverse content into assessments, 
        ensuring inclusivity and relatability. You understand the nuances of various cultures and ensure that assessments are free from bias and resonate with learners worldwide.
        Additional rules for Tools:
        -----------------
        1. Regarding the Action Input (the input to the action, just a simple python dictionary, enclosed
        in curly braces, using \" to wrap keys and values.)
        
        For example for the following schema:
        ```
        class ExampleToolInput(BaseModel):
          task: str = Field(..., description="The task to delegate")
          context: str = Field(..., description="The context for the task")
          coworker: str = Field(..., description="The role/name of the coworker to delegate to")
        ```
        Then the input should be a JSON object with the user ID:
        - task: The task to delegate
        - context: The context for the task
        - coworker: The role/name of the coworker to delegate to        
        """,
    verbose=True,
    allow_delegation=True,
    llm=llm
)

task3 = Task(
    description="""Review and refine the content of assessments to include culturally diverse themes, avoiding stereotypes and ensuring global relevance.""",
    agent=cultural_relevance_agent,
    expected_output="""A report detailing refinements and suggestions for culturally diverse and inclusive content. Include couple of MCQ question for each type are areas""",
)

crew = Crew(
    agents=[language_expert, pedagogical_strategist, cultural_relevance_agent],
    tasks=[task1, task2, task3],
    verbose=True,
    process=Process.sequential,  # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
)

result = crew.kickoff()

print("######################")
print(result)