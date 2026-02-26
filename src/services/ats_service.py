from openai import OpenAI
from src.services.prompts.extraction_prompt import SYSTEM_PROMPT,USER_PROMPT
from constants import GPT_Model
from src.models.ats_models import ATSResult
from src.utilities.openai_llm_utils import OpenAI_Text_Config, OpenAITextGenerator
from src.services.prompts.jd_prompts import JD_SYSTEM_PROMPT,JD_USER_PROMPT
from src.services.prompts.ats_score_prompt import ATS_SCORE_SYSTEM_PROMPT

from dotenv import load_dotenv
load_dotenv()

class ATSservice:
    def __init__(self):
       self.ai_generator = OpenAITextGenerator(
           config=OpenAI_Text_Config(
               model=GPT_Model.GPT_40_MINI.value,
           )
         )

    async def extract_cv_items(self, ocr_text):
        try: 
            response = await self.ai_generator.async_generate_response(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=USER_PROMPT.format(raw_text=ocr_text),
                json_response=True,
                # response_model=ATSResult
            )
            
            return response["response"]

        except Exception as e:
            raise e
        
    async def extract_jd_items(self, jd_text):
        try: 
            response = await self.ai_generator.async_generate_response(
                system_prompt=JD_SYSTEM_PROMPT,
                user_prompt=JD_USER_PROMPT.format(jd_text=jd_text),
                json_response=True                
            )
            
            return response["response"]

        except Exception as e:
            raise e

    async def generate_ats_score(self, cv_data, jd_data):
        try:
            user_prompt = f"""
            CV DATA:
            {cv_data}

            JOB DESCRIPTION DATA:
            {jd_data}
            """

            response = await self.ai_generator.async_generate_response(
                system_prompt=ATS_SCORE_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                json_response=True
                
            )

            return response["response"]

        except Exception as e:
            raise e
       
    def calculate_score(self):
        pass
