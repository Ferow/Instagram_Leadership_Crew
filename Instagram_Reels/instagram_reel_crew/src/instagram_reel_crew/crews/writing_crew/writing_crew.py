from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from typing import List
from crewai_tools import SerperDevTool

import os
from dotenv import load_dotenv
load_dotenv()


agent_llm = LLM(
	base_url=os.getenv("OLLAMA_BASE_URL"), 
	model=os.getenv("OLLAMA_MODEL"),
	api_key = os.getenv("FAKE_KEY")
)

class Weekday(BaseModel):
    DayOfTheWeek: str
    title: str
    summary: str
    sources: List[str]
    posttext: str
    hashtags: str
    imageprompt: str
    
class InstagramPlan(BaseModel):
    DaysOfTheWeek: List[Weekday]
    theme: str
    
@CrewBase
class WritingCrew():
	"""Writing Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def content_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_writer'],
   			verbose=True,
			llm=agent_llm
		)
  
	@agent
	def AI_prompt_engineer(self) -> Agent:
		return Agent(
			config=self.agents_config['AI_prompt_engineer'],
    			verbose=True,
				llm=agent_llm
		)

	@task
	def post_writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['post_writing'],
		)
  
	@task
	def prompt_writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['prompt_writing'],
			output_json=InstagramPlan
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			
		)
