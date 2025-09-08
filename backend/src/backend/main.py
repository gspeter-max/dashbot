
import warnings
from pydantic import BaseModel
import typing 
import uvicorn
from fastapi import FastAPI
from datetime import datetime

from backend.crew import Backend
from backend.ArgType import requestArgumentClass, responseArgumentClass

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

    
class apiContextClass( BaseModel ):
    request : requestArgumentClass
    response : responseArgumentClass

class finalArgumentClass( BaseModel ):
    user_prompt: str
    api_context: apiContextClass

app = FastAPI() 

async def _start_crewai(input_for_crewai_agents : typing.Dict[str, str]):
    inputs = {
        'topic': 'ai agent for ApiDash',
        'current_year': str(datetime.now().year),
        'input_for_crewai_agents' : input_for_crewai_agents
    }
    try:
        Backend().crew().kickoff()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


getHistoryData = {} 
current_user_data = {}
i = 0 

@app.get('/v1/getCurrentUserData')
async def getCurrentMemory(self):
    return {
        'status': 'OK',
        'response_data': current_user_data
    }

@app.get('/v1/getHistoryOfUsers')
async def getHistoryOfUsers(self):
    return {
        "status" : "OK",
        "response_data" : getHistoryData
    }

@app.post('/v1/ask')
async def userQuery(query: finalArgumentClass ):
    global current_user_data 
    global getHistoryData 
    print("✅ --- DATA SUCCESSFULLY RECEIVED FROM FLUTTER! --- ✅")
    
    # Here is the key part: We call our other function and PASS the `query`
    # object to it. The `query` object is "stored" in memory for this to happen.
    current_user_data = query 
    global i 
    i += 1 

    getHistoryData[f'requestNumber_{i}'] = query
    if len(getHistoryData.keys()) > 3:
        getHistoryData.pop(getHistoryData.keys()[0]) 

    crewai_input  = {
        'topic': 'ai agent for ApiDash',
        'current_year': str(datetime.now().year),
        'input_for_crewai_agents' : {
            "user_prompt": query.user_prompt,
            "api_context": {
                "requests" : {
                    "method" : query.api_context.request.method,
                    "url": query.api_context.request.url,
                    "headers": query.api_context.request.headers,
                    "params": query.api_context.request.params,
                    "authModel": query.api_context.request.authModel,
                    "isHeaderEnabledList" : query.api_context.request.isHeaderEnabledList,
                    "isParamEnabledList" : query.api_context.request.isParamEnabledList,
                    "bodyContentType" : query.api_context.request.bodyContentType,
                    "body" : query.api_context.request.body,
                    "formData" : query.api_context.request.formData
                },
                "response" : {
                    "statusCode": query.api_context.response.statusCode,
                    "headers": query.api_context.response.headers,
                    "requestHeaders": query.api_context.response.requestHeaders,
                    "body": query.api_context.response.body,
                    "formattedBody": query.api_context.response.formattedBody,
                    "bodyBytes": query.api_context.response.bodyBytes,
                    "time" : query.api_context.response.time,
                    "seeOutput": query.api_context.response.sseOutput
                }
            }
        }
    }

    final_answer = await _start_crewai(input_for_crewai_agents = crewai_input)
    
    print("✅ --- PREPARING TO SEND RESPONSE BACK TO FLUTTER --- ✅")
    print(f"✅ --- arguemnt recived > {query}")
    
    return {
        "status" : "success",
        "message" : "Data processed successfully by the AI backend.",
        "finalAnswer" : {final_answer}
    }
