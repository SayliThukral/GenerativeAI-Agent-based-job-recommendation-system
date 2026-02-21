from openai import OpenAI
from src.services.prompts.extraction_prompt import SYSTEM_PROMPT,USER_PROMPT
from constants import GPT_Model
from src.models.ats_models import ATSResult
from src.utilities.openai_llm_utils import OpenAI_Text_Config, OpenAITextGenerator

from dotenv import load_dotenv
load_dotenv()

class ATSservice:
    def __init__(self):
       self.ai_generator = OpenAITextGenerator(
           config=OpenAI_Text_Config(
               model=GPT_Model.GPT_40_MINI.value,
           )
         )

    async def extract_subheadings(self, ocr_text):
        try: 
            response = await self.ai_generator.async_generate_response(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=USER_PROMPT.format(raw_text=ocr_text),
                # response_model=ATSResult
            )
            
            return response["response"]

        except Exception as e:
            raise e
        
       
    def calculate_score(self):
        pass
