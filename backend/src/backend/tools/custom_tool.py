import google 
from google import genai 
import os 
import subprocess
import requests
from fastapi import FastAPI
import crewai 
from crewai.tools import BaseTool
import typing 
from pydantic import BaseModel, Field


class getCurrentRequestData(BaseTool):
    name: str = "getCurrentRequestData"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need ."
    )
    async def _run(self) -> str:
        try:
            url = 'https://localhost' # keep it pending 
            currentRequestData = requests.get(url = url)

            return f'current user metaData : {currentRequestData}'
        except Exception as e:
            return f'error is occure during execution of `getCurrentRequestData` Tool '

class getHistoryOfUserRequests( BaseTool ):
    name : str = 'getHistoryOfUserRequests'
    description : str = (
        'description ai write that for me '
    )

    async def _run(self):
        try:
            url = 'https://localhost'
            historyRequestData = requests.get(url = url)

            return f'history Request Data : {historyRequestData}'
        except Exception as e:
            return f'error is occure during execution of `getHistoryOfUserRequests` Tool '

class ExecutionInput(BaseModel):
    """Input for the TerminalCodeExecutor tool. Specifies the commands to run."""
    commands: typing.List[str] = Field(..., description="A list of one or more valid shell command strings to execute sequentially. These should typically be the direct output from the PromptToTerminalCommandTool.")

class TerminalExecution(BaseTool):  

    name: str = "TerminalCodeExecutor"
    description: str = (
        "Executes a list of shell commands directly in the system terminal and returns their complete output. "
        "This tool is essential for any task requiring direct system interaction, file manipulation, or data gathering from the OS."                          
    )
    args_schema: typing.Type[BaseModel] = ExecutionInput
   
    async def _run(self, commands: typing.List[str]) -> str:
        OutputList = []
        for cmd in commands:
            try:           
                process_output = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)                                                 
                if process_output.stderr:       
                    OutputList.append(f"Command '{cmd}' resulted in an ERROR: {process_output.stderr.strip()}")                                               
                else:
                    OutputList.append(process_output.stdout.strip())                                                                                          
            except Exception as e:                  
                OutputList.append(f"CRITICAL FAILURE executing command '{cmd}': {e}")                                                                         
        return str(OutputList)

class WriteFileAndCreateInput(BaseModel):
    """Input for the WriteFileAndCreateTool. Defines the file's name, format, and content."""
    content: str = Field(..., description="The string content to be written into the file.")
    file_name: str = Field(..., description="The base name of the file, without the extension. E.g., 'research_notes'.")
    file_format: str = Field(..., description="The file extension, without the dot. E.g., 'md', 'txt', 'json'.")

class WriteFileAndCreate(BaseTool):
    name: str = "WriteFileAndCreateTool"
    description: str = "Creates a new file with a specified name and format, and writes string content into it. Essential for saving research, notes, or structured data for later use by other agents."

    args_schema: typing.Type[BaseTool] = WriteFileAndCreateInput

    async def _run(self, content: str, file_name: str, file_format: str):
        if isinstance(content, bytes):
            file_read_format = 'wb'
        else:
            file_read_format = 'w'

        try:
            with open(f'./{file_name}.{file_format}', file_read_format) as f:
                f.write(content)
            return f'{file_name}.{file_format} is created and content writing is complete and save at ./{file_name}.{file_format}'

        except Exception as e:
            return f'{file_name}.{file_format} file creation is failed with error : {e}'


class longThinkingToolInput( BaseModel ):
    content : str = Field(..., description = 'problem for this long thinking ')

class longThinkingTool( BaseTool ):
    name : str = 'longThinkingTool'
    description : str = 'description about ...'

    args_schema = typing.Type[BaseModel] = longThinkingToolInput()
    async def _run( self, content : str ):
        client = genai.Client( api_key = os.environ.get('GOOGLE_API_KEY', None ))
        generate_content_config = google.genai.types.GeneateContentConfig(
            thinkingConfig = google.genai.types.ThinkingConfig(
                includeThoughts = True,
                thinkingBudget = 20000
            )
        )
        response = client.models.generate_content(
            model = 'gemini-2.0-flash',
            contents = f'find the solution of that thinking too deep and find what the problem is : {content} ? ', 
            config = generate_content_config 
        )

        # return thinking and the result do this when you have without quota api key 

class isValiedForPlotingInput( BaseModel ):
    JsonContent : str = Field(..., description = 'description about that ')

class isValiedForPloting: 
    name : str = 'isValiedForPloting'
    description : str = ''
    
    args_schema = typing.Type[BaseModel] = isValiedForPlotingInput
    async def _run( JsonContent : typing.Union[ str, typing.Dict[str,str]]):
        client = genai.Client( api_key = os.environ.get('GOOGLE_API_KEY', None ))
        generate_content_config = google.genai.types.GeneateContentConfig(
            thinkingConfig = google.genai.types.ThinkingConfig(
                includeThoughts = True,
                thinkingBudget = 20000
            )
        )
        response = client.models.generate_content(
            model = 'gemini-2.0-flash',
            contents = f'only and only give me this json data is ok for ploting  : {JsonContent} ? ',
            config = generate_content_config
        )

        # return response.text 
