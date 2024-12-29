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
    sources: List[str]
    
class InstagramPlan(BaseModel):
    DaysOfTheWeek: List[Weekday]
    theme: str
    
@CrewBase
class PlanningCrew():
	"""Planning Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def planner(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
   			verbose=True,
			llm=agent_llm
		)
  
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
   			tools=[SerperDevTool()], # Example of custom tool, loaded on the beginning of file
   			verbose=True,
			llm=agent_llm
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['planning_task'],
		)
  
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_pydantic=InstagramPlan
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
