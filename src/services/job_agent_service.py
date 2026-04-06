from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from src.services.job_agent_tools import search_jobs
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=1000,
    
)

@tool

def job_tool(input_text: str) -> str:
    """
    ALWAYS use this tool to find job recommendations.
    Input will contain skills and experience.
    Extract them and return job results.
    DO NOT answer directly.
    """

    try:
        text = input_text.lower()

        # 🔹 Extract skills
        skills = ""
        if "skills:" in text:
            skills = text.split("skills:")[1].split("experience:")[0].strip()

        # 🔹 Extract experience
        experience = ""
        if "experience:" in text:
            experience = text.split("experience:")[1].strip()

        # 🔹 Handle weak experience like "internship"
        if not any(char.isdigit() for char in experience):
            if "intern" in experience:
                experience = "0-1 years"
            elif "project" in experience:
                experience = "0-1 years"
            else:
                experience = "1-2 years"  # fallback

        # 🔹 Final validation
        if not skills:
            return "❌ Skills missing"

        return search_jobs(skills, experience)

    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_job_recommendations(skills: list, experience: list) -> str:
    agent = create_agent(model, tools=[job_tool])
    
    query = f"""
        You MUST use the job_tool to find job recommendations.

        User details:
        Skills: {', '.join(skills)}
        Experience: {', '.join(experience)}

        Do NOT answer on your own.
        Do NOT ask for more information.
        Just call the tool and return the result.
        """
    
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })

    return response["messages"][-1].content