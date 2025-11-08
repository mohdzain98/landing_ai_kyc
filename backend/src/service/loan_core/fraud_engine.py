from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import json
import os
from pathlib import Path
from dotenv import load_dotenv


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

HUMAN_PROMPT = ''' 
Here is the customer's bank statement data in JSON format:
{bank_statement_json}

Here is the customer's salary slip data in JSON format:
{salary_slips_json}
'''
class FraudDetectionEngine:
    def __init__(self, model_id:str ="gemini-2.5-flash-lite"):
        self.model_id = model_id
        self.llm = ChatGoogleGenerativeAI(model=self.model_id)
        self.system_prompt = SYSTEM_PROMPT
        self.human_prompt = HUMAN_PROMPT

    def load_json(self,file_path):
        '''
        input: json file path
        output: text
        Reads a JSON file and returns a pretty string for model input. 
        '''

        with open(Path(file_path), "r") as f:
            json_text = json.load(f)
        return json.dumps(json_text, indent=2)
        

    def fraud_detection(self, bank_json_path, income_json_path):
        bank_json = self.load_json(bank_json_path)
        income_json = self.load_json(income_json_path)

        system_template = SystemMessagePromptTemplate.from_template(self.system_prompt)
        human_template = HumanMessagePromptTemplate.from_template(self.human_prompt)

        chat_prompt = ChatPromptTemplate.from_messages([system_template, human_template])
        formated_message = chat_prompt.format_messages(bank_statement_json=bank_json, salary_slips_json=income_json)
        response = self.llm.invoke(formated_message)
        return response.content

    def save_fraud_summary(self,  base_path):
        bank_json_path  = f"{base_path}/bank-statements/output/bank-statements.json"
        income_json_path  = f"{base_path}/income-proof/output/income-proof.json"
        sumamry = self.fraud_detection(bank_json_path, income_json_path)
        print(f"The fraud summary is  {sumamry}")
        save_path = f"{base_path}/final_output/fraud_report.json"
        # print(save_path)
        # with open(save_path, "w") as f:
        #     f.write(sumamry)

        return sumamry,save_path
