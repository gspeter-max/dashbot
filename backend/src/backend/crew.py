from crewai import Agent, Crew, Process, Task, LLM 
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import TavilySearchTool
from backend.tools.custom_tool import WriteFileAndCreate, getHistoryOfUserRequests, getCurrentRequestData, TerminalExecution, isValiedForPloting, longThinkingTool

@CrewBase
class Backend():
    """Backend crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def summaryManager(self) -> Agent:
        return Agent(
            config=self.agents_config['summaryManager'], # type: ignore[index]
            verbose=True,
            llm = LLM( model = 'gemini/gemin-2.0-flash'),
            tools = [ getCurrentRequestData(), getHistoryOfUserRequests() ],
            max_rpm= 12,
            cache = True,
            verbose = True, 
            max_iter = 3
        )
    
    @agent
    def explainMaster(self) -> Agent:
        return Agent(
            config=self.agents_config['explainMaster'], # type: ignore[index]
            verbose=True,
            llm = LLM(model = 'gemini/gemini-2.0-flash'),
            tools = [ TavilySearchTool() , TerminalExecution(), getCurrentRequestData(), longThinkingTool() ],
            max_rpm = 12,
            cache = True,
            verbose = True,
            max_iter = 2
        )

    @agent
    def debuggingMaster( self ) -> Agent:
        return Agent(
            config = self.agent_config['debuggingMaster'],
            verbose = True,
            llm = LLM(model = 'gemini/gemini-2.0-flash'),
            tools = [TerminalExecution(), TavilySearchTool(), longThinkingTool(), WriteFileAndCreate() ],
            max_rpm= 12,
            cache = True,
            max_iter = 2
        )
    @agent
    def documentGeneraterMaster( self ) -> Agent:
        return Agent(
            config = self.agent_config['documentGeneraterMaster'],
            verbose = True,
            llm = LLM( model = 'gemini/gemini-2.0-flash'),
            tools = [ WriteFileAndCreate(), TavilySearchTool() , getHistoryOfUserRequests(), getCurrentRequestData() ],
            max_rpm = 14,
            cache = True,
            max_iter = 3 
        )

    def testGeneraterKing( self ) -> Agent:
        return Agent(
            config = self.agent_config['testGeneraterKing'],
            verbose = True,
            llm = LLM(model = 'gemini/gemini-2.0-flash'),
            tools = [ WriteFileAndCreate(), getCurrentRequestData(), TavilySearchTool(), longThinkingTool(), TerminalExecution() ],
            max_rpm = 15,
            cache = True,
            max_iter = 3
        )
    
    def responseVisualizer( self ) -> Agent:
        return Agent(
            config = self.agent_config['responseVisualizer'],
            verbose = True,
            llm = LLM(model = 'gemini/gemini-2.0-flash'),
            tools = [ isValiedForPloting(), ],
            max_rpm = 15,
            cache = True,
            max_iter = 3
        )
    
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Backend crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        manager_llm = LLM( model = 'gemini/gemini-2.0-flash')
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_llm = manager_llm,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
