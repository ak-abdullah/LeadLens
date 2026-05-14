from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()
@tool
def search_company_news(company_name: str) -> str:
    """Search for recent news about a company."""
    search = TavilySearch(max_results=3)
    response = search.invoke(f"{company_name} company recent news 2025 2026")
    # New TavilySearch returns dict with 'results' key
    if isinstance(response, dict) and "results" in response:
        return "\n".join([r["content"] for r in response["results"]])
    return str(response)

@tool
def search_tech_stack(company_name: str) -> str:
    """Find the tech stack a company uses from job postings."""
    search = TavilySearch(max_results=3)
    response = search.invoke(
        f"{company_name} job posting backend engineer python AWS OR GCP OR Azure tech stack"
    )
    if isinstance(response, dict) and "results" in response:
        return "\n".join([r["content"] for r in response["results"]])
    return str(response)
    
llm = ChatGroq(model="llama-3.3-70b-versatile")

tools = [search_company_news, search_tech_stack]
agent = create_react_agent(llm, tools)

def run_agent(company_name: str) -> str:
    prompt = f"""
    You are an AI outreach assistant.
    
    Research the company: {company_name}
    
    Steps:
    1. Search for recent news about them
    2. Find their tech stack
    3. Identify one specific pain point or opportunity
    4. Write a short, personalized cold outreach message (max 100 words)
    
    The message should feel human, not AI-generated.
    End with the final message only — no explanations.
    """
    
    result = agent.invoke({"messages": [("user", prompt)]})
    return result["messages"][-1].content

if __name__ == "__main__":
    output = run_agent("Stripe")
    print(output)