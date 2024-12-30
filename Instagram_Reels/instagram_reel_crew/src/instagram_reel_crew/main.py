#!/usr/bin/env python
import json
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from crewai import LLM
from .crews.planning_crew.planning_crew import PlanningCrew
from .crews.writing_crew.writing_crew import WritingCrew

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
            post_inputs = week.dict()
            post_inputs["theme"] = plan.theme
            weekdayContent = WritingCrew().crew().kickoff(post_inputs).json
            #print(f"Day of the week - {week.DayOfTheWeek}")
            print(weekdayContent)
            final_content.append(weekdayContent)
        return final_content
    
    @listen(generate_posts)
    def save_final(self, content):
        print("printing final posts")
        output_dir = "output"
       
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        with open(os.path.join(output_dir, "final_content.json"), "w", encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
def kickoff():
    poem_flow = InstagramFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = InstagramFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
