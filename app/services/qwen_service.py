from openai import OpenAI
from app.core.config import settings
from app.core.logger import logger
from typing import Dict, Any, List

class QwenService:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.QWEN_API_URL,
            api_key="none"
        )
        self.model = settings.QWEN_MODEL_NAME

    async def create_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> str:
        """
        调用通义千问API生成回复
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error calling Qwen API: {str(e)}")
            raise

qwen_service = QwenService() 