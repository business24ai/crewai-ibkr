import os
from crewai import Agent, Task, Crew, Process
from tools.custom_ibkr_tools import CustomTradingTools
from tools.custom_tools import CustomTools

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = "YOUR_KEY_HERE"

# Use a more cost effective model
from langchain.chat_models import ChatOpenAI
llm_gpt35=ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.2)

# Define our portfolio manager
portfolio_manager = Agent(
  role='Portfolio Manager',
  goal='Manage the portfolio and get the portfolio positions',
  backstory="""You manage the portfolio of the customer.
  You can give information about the positions in the portfolio.
  This inforamtion is private so only use the provided tool.""",
  verbose=True,
  allow_delegation=False,
  tools=[CustomTradingTools.get_positions_of_portfolio],
  llm=llm_gpt35,
)


# Define our market manager
market_manager = Agent(
  role='Market Manager',
  goal='Get stock price and market data',
  backstory="""You can get the live and latest price of the stock.
  You should use the provided tool to get the data,
  but each time use only a single ticker symbol.
  """,
  verbose=True,
  allow_delegation=False,
  tools=[CustomTradingTools.fetch_live_last_stock_price],
  llm=llm_gpt35,
)

# Define our financial analyst
financial_analyst = Agent(
  role='Financial Analyst',
  goal='Summerize and analyse financial market information',
  backstory="""Your job is get the information about the current
  positions in the portfolio and check the market data and 
  analyse the financial information regarding the portfolio stocks.
  You should summerize the information in markdown table.""",
  verbose=True,
  allow_delegation=True,
  llm=llm_gpt35,
)

note_taker = Agent(
  role='Note Taker',
  goal='Save content as note and store them as markdown on local device',
  backstory="""You structure and format the given content to markdown
  and create a note to be stored on disk.
  You MUST use the TOOL provided to store the note to Obsidian.
  If the content has a list use a markdown table to organize the text.
  If the content starts or ends with ``` remove the ```.
  Make sure the text is saved on disk.
  When the note is saved successful return "Note is saved.".
  """,
  verbose=True,
  allow_delegation=False,
  tools=[CustomTools.store_note_to_obsidian],
  llm=llm_gpt35,
)


# Create tasks for your agents
task1 = Task(
  description="""Get the positions of the portfolio.""",
  agent=portfolio_manager
)

task2 = Task(
  description="""For each position in the portfolio check the latest price separately.""",
  agent=market_manager
)

task3 = Task(
  description="""Create a report with a markdown table with each row a position in the portfolio and the current price of it.""",
  agent=financial_analyst
)

task4 = Task(
  description="""Save the report as a note in our second brain.""",
  agent=note_taker
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[portfolio_manager, market_manager, financial_analyst, note_taker],
  tasks=[task1, task2, task3, task4],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
