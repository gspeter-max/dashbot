#!/usr/bin/env python
from enum import Enum
import warnings
from pydantic import BaseModel
from pydantic import Field
import typing 
from fastapi import FastAPI
from datetime import datetime

from backend.crew import Backend
from backend.src.backend.ArgType import requestArgumentClass, responseArgumentClass

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

    
class apiContextClass( BaseModel ):
    request : requestArgumentClass
    response : responseArgumentClass

class finalArgumentClass( BaseModel ):
    user_promopt: str
    api_context: BaseModel = apiContextClass

class apiDashArgument( BaseModel ):
    userQuery : str 
    headers : typing.Optional[ typing.Dict[str, str ]]  
    requests_body : typing.Optional[ typing.Dict[str, str ]]
    method : str 
    url : str 
    response_body : typing.Optional[typing.Dict[str,str]]
    status_code: int
    time_taken_ms: int

app = FastAPI() 

def _start_crewai(input_for_crewai_agents : typing.Dict[str, str]):
    inputs = {
        'topic': 'ai agent for ApiDash',
        'current_year': str(datetime.now().year),
        'input_for_crewai_agents' : input_for_crewai_agents
    }
    try:
        Backend().crew().kickoff()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    

@app.post('/v1/ask')
def userQuery(query: apiDashArgument): 
    print("✅ --- DATA SUCCESSFULLY RECEIVED FROM FLUTTER! --- ✅")
    
    # Here is the key part: We call our other function and PASS the `query`
    # object to it. The `query` object is "stored" in memory for this to happen.
    query = {
        'topic': 'ai agent for ApiDash',
        'current_year': str(datetime.now().year),
        'input_for_crewai_agents' : query
        }
    
    final_answer = _start_crewai(input_for_crewai_agents = query)
    
    print("✅ --- PREPARING TO SEND RESPONSE BACK TO FLUTTER --- ✅")
    print(f"✅ --- arguemnt recived > {query}")
    
    return {
        "status" : "success",
        "message" : "Data processed successfully by the AI backend.",
        "finalAnswer" : {final_answer}
    }
