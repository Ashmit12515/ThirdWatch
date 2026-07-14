from app.ai.control_extraction import extract_controls
text = """
The organization maintains a SOC 2 Type II report.

Multi-factor authentication is enabled.

Customer data is encrypted using AES-256.

Incident response procedures are tested annually.

ISO 27001 certification is maintained.
"""
result=extract_controls(text)
print(result)