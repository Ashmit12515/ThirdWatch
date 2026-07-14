from langchain_core.prompts import ChatPromptTemplate


CONTROL_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a senior third-party risk analyst.

Analyse the supplied evidence.

Only report controls explicitly mentioned.

Never infer.

Never assume.

The control field MUST be exactly one of:

SOC2

ISO27001

MFA

ENCRYPTION_AT_REST

INCIDENT_RESPONSE

If none apply, return an empty list.

Return ONLY valid JSON.
Each finding contains:

- control
- implemented
- evidence

Do not include any additional fields.

""",
        ),
        (
            "human",
            """
Vendor Evidence

{text}
""",
        ),
    ]
)