from langchain_openai import ChatOpenAI

from app.config import settings


llm = ChatOpenAI(
    model=settings.lm_studio_model,
    base_url=settings.lm_studio_base_url,
    api_key=settings.lm_studio_api_key,
    temperature=0,
)