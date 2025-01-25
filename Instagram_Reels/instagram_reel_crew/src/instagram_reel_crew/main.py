#!/usr/bin/env python
import datetime
import json
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from crewai import LLM
from .crews.planning_crew.planning_crew import PlanningCrew
from .crews.writing_crew.writing_crew import WritingCrew
import agentops
import os

#from langtrace_python_sdk import langtrace
from dotenv import load_dotenv
load_dotenv()
agentops.init(api_key = os.getenv("AGENTOPS_API_KEY"),skip_auto_end_session=True)
#langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"),
#                api_host = os.getenv("LANGTRACE_API_HOST"))
input_variables = {
            "number_of_posts": 3,
            "mood": "inspiring"
        }

class InstagramFlow(Flow):
    @start()
    def generate_research_topics(self):
        return PlanningCrew().crew().kickoff(inputs=input_variables).pydantic

    @listen(generate_research_topics)
    def generate_posts(self, plan):
       
        final_content = {
            "posts": []
        }
        for post in plan.Posts:
            post_inputs = post.dict()
            post_inputs = {**input_variables, **post_inputs}
            content = WritingCrew().crew().kickoff(inputs=post_inputs).json
            final_content["posts"].append(content)
            
        return json.dumps(final_content, ensure_ascii=False, indent=4)
    
    @listen(generate_posts)
    def save_final(self, content):
        print("printing final posts")
        output_dir = "output"
        print(content)
      
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        import random
        output_file = f"{datetime.date.today().isoformat()}-{input_variables['number_of_posts']}-{input_variables['mood']}-{random.randint(0,999):03d}.json"
        with open(os.path.join(output_dir, output_file), "w") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
def kickoff():
    poem_flow = InstagramFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = InstagramFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
