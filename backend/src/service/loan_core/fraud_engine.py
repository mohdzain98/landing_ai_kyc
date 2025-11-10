from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import json
import os
from pathlib import Path
from dotenv import load_dotenv


# ===========================
# 🔹 System Prompt Definition
# ===========================
SYSTEM_PROMPT = ''' 
You are a **Loan Approver Assistant**.
Your task is to compare two data sources — a customer's bank statement and salary slips — both provided in JSON format.

Identify and list any **factual discrepancies** between the two datasets.

Focus specifically on:
- Differences between the salary amount credited in the bank statement and the gross/net pay in the salary slips.
- Missing or inconsistent salary deposit dates in the bank statement compared to salary slip pay dates.
- Differences in employer name or salary source description between both documents.
- Unusual patterns such as multiple salary credits in one month, missing months, or partial credits.

Follow these strict rules:
- Do **not** make assumptions or judgments about reasons for discrepancies.
- Do **not** assess eligibility, risk, or authenticity.
- Report only **factual mismatches or inconsistencies** found between the JSON datasets.

Present your findings in a clear and concise summary labeled:
**“Discrepancy Summary:”**
If no discrepancies are found, state: **“No discrepancies found between bank statement and salary slips.”**
If there are discrepancies in bank statement and pay slips like name of company or the amount credited is not matching then send out a warning stating that: 
*"Warning:"* 
Upload the bank statement where your salary is credited"
'''


# ===========================
# 🔹 Human Prompt Definition
# ===========================
HUMAN_PROMPT = ''' 
Here is the customer's bank statement data in JSON format:
{bank_statement_json}

Here is the customer's salary slip data in JSON format:
{salary_slips_json}
'''


# ===========================
# 🔹 FraudDetectionEngine Class
# ===========================
class FraudDetectionEngine:
    def __init__(self, model_name="amazon.titan-text-express-v1"):
        """
        Initialize the FraudDetectionEngine with AWS Bedrock model credentials and configuration.
        """
        self.system_prompt = SYSTEM_PROMPT
        self.human_prompt = HUMAN_PROMPT

        # Load environment variables (for AWS credentials)
        load_dotenv()

        # Fetch AWS credentials
        access_key = os.getenv("AWS_ACCESS_KEY")
        secret_key = os.getenv("AWS_SECRET_KEY")

        # Initialize the Bedrock LLM client
        self.llm = ChatBedrock(
            model=model_name,
            region="us-east-1",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def load_json(self, file_path):
        '''
        Input: JSON file path
        Output: String (pretty formatted JSON)
        Reads a JSON file and returns a formatted string for model input.
        '''
        with open(Path(file_path), "r") as f:
            json_text = json.load(f)
        return json.dumps(json_text, indent=2)

    def fraud_detection(self, bank_json_path, income_json_path):
        """
        Compare bank statement and salary slip JSONs using the LLM to detect factual discrepancies.
        """
        # Load and format both JSONs
        bank_json = self.load_json(bank_json_path)
        income_json = self.load_json(income_json_path)

        # Prepare system and human message templates
        system_template = SystemMessagePromptTemplate.from_template(self.system_prompt)
        human_template = HumanMessagePromptTemplate.from_template(self.human_prompt)

        # Combine messages into a single chat prompt
        chat_prompt = ChatPromptTemplate.from_messages([system_template, human_template])

        # Format message inputs for LLM
        formated_message = chat_prompt.format_messages(
            bank_statement_json=bank_json,
            salary_slips_json=income_json
        )

        # Get response from the model
        response = self.llm.invoke(formated_message)
        return response.content

    def save_fraud_summary(self, base_path):
        """
        Run fraud detection on bank statement and income proof JSONs,
        print the summary, and return the summary with save path.
        """
        # Define file paths
        bank_json_path = f"{base_path}/bank-statements/output/bank-statements.json"
        income_json_path = f"{base_path}/income-proof/output/income-proof.json"

        # Generate fraud summary
        sumamry = self.fraud_detection(bank_json_path, income_json_path)
        print(f"The fraud summary is  {sumamry}")

        # Define output save path
        save_path = f"{base_path}/final_output/fraud_report.json"
        return sumamry, save_path
