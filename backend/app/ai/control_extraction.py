from app.ai.llm import llm
from app.ai.prompts import CONTROL_EXTRACTION_PROMPT
from app.ai.schemas import ControlExtraction

structured_llm=llm.with_structured_output(
    ControlExtraction
)

def extract_controls(
        text:str,
) -> ControlExtraction:
    chain=(
        CONTROL_EXTRACTION_PROMPT
        | structured_llm
    )
    return chain.invoke(
        {
            "text":text
        }
    )