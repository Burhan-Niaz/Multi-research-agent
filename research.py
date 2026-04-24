from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# Loading Tavily for Web search

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str)-> str:
    """"Search the web for recent and reliable information on a topic , returns Titles, URLS, snippets."""
    results=tavily.search(query=query,max_results=3)
    
    out=[]
    for r in results['results']:
         out.append(
             f"Title : {r ['title']} \n URL :{r['url']} \n Snippet:{r['content'][:300]}\n"
         )
    return "\n-----------------------------------------------\n".join(out)

ans=web_search.invoke("What are the recent news of Iran America war?")
#print(ans)  


# Loading data from Beautiful Soap by extracting data from web-url scarping

@tool
def scrape_url(url:str)->str:
    """Scrap and return clean text content from a given url for deeper reading."""
    
    try:
        resp=requests.get(url,timeout=8,headers={"User-Agent":"Mozilla/5.0"})
        soup=BeautifulSoup(resp.text,"html.parser")
        for tag in soup (["script","style","nav","footer"]):
            tag.decompose()
            return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL:{str(e)}"    

"""
python research.py
 
 """