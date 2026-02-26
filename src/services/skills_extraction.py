# from src.utilities.skills_prompt import build_skills_prompt
# from src.utilities.openai_llm_utils import async_generate_response
# def extract_skills(raw_text):

#     # 1️⃣ Build prompt
#     prompt = build_skills_prompt(raw_text)

#     # 2️⃣ Call LLM
#     # response = async_generate_response(
#         user_prompt=prompt,   # ✅ use prompt here
#         system_prompt="Extract only technical skills in JSON format."
#     )

#     # 3️⃣ Return cleaned response
#     return response["response"]