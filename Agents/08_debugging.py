from phi.agent import Agent

import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

agent = Agent(markdown=True, debug_mode=True)
agent.print_response("Share a 2 sentence horror story")