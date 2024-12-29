#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from crewai import LLM
from .crews.planning_crew.planning_crew import PlanningCrew

import os
from langtrace_python_sdk import langtrace
from dotenv import load_dotenv
load_dotenv()

langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"),
                api_host = os.getenv("LANGTRACE_API_HOST"))
input_variables = {
            "number_weeks": 2,
        }

class InstagramFlow(Flow):
    @start()
    def generate_research_topics(self):
        return PlanningCrew().crew().kickoff().pydantic

    @listen(generate_research_topics)
    def generate_posts(self, plan):
        print(f"Generating content, the theme of week is {plan.theme}")
        final_content = []
        for week in plan.DaysOfTheWeek:
            print(week)
           
def kickoff():
    poem_flow = InstagramFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = InstagramFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
