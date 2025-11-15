import json
import pandas as pd
import collections
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class FraudDetectionEngine:
    def __init__(self, base_path):
        """
        Initialize the FraudDetectionEngine with root path of json files.
        """
        self.base_path = base_path
        self.bank_statement_path = base_path + "/bank-statements/output/bank-statements.json"
        self.credit_report_path = base_path + "/credit-reports/output/credit-reports.json"
        self.identity_doc_path = base_path + "/identity-documents/output/identity-documents.json"
        self.income_proof_path = base_path + "/income-proof/output/income-proof.json"
        self.tax_statement_path = base_path + "/tax-statements/output/tax-statements.json"
        self.utility_bills_path = base_path + "/utility-bills/output/utility-bills.json"

    def load_json(self, file_path):
        """
        Reads a JSON file and returns the dictionary.
        """
        with open(Path(file_path), "r") as f:
            json_text = json.load(f)
        return json_text

    def pairwise_similarity(self, docs):
        """
        Returns list of document names where name mismatch (similarity < 0.95).
        """
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(docs)
        cosine_sim_matrix = cosine_similarity(tfidf_matrix)

        doc_labels = ["bank statement", "credit report", "identity document", "income document", "tax document", "utility bills"]
        df = pd.DataFrame(cosine_sim_matrix, columns=doc_labels, index=doc_labels)

        mismatch = []
        for col in df.columns:
            mismatch.extend(df[col][df[col] < 0.95].index.values.tolist())

        collections_dict = collections.Counter(mismatch)

        # FIX: If empty → return empty list (no mismatches)
        if not collections_dict:
            return []

        # find mismatched items (logic based on your code)
        min_value = min(collections_dict.values())
        mismatch_items = [item for item, count in collections_dict.items() if count > min_value]

        return mismatch_items

    def fraud_detection(self):
        """
        Compare names across documents using TF-IDF similarity.
        """
        bank_json = self.load_json(self.bank_statement_path)
        credit_json = self.load_json(self.credit_report_path)
        identity_json = self.load_json(self.identity_doc_path)
        income_json = self.load_json(self.income_proof_path)
        tax_json = self.load_json(self.tax_statement_path)
        utility_json = self.load_json(self.utility_bills_path)

        name_in_bank = bank_json["account_holder_name"]
        name_in_credit = credit_json["full_name"]
        name_in_identity = identity_json["full_name"]
        name_in_income = income_json["employee_name"]
        name_in_tax = tax_json["taxpayer_first_name"] + " " + tax_json["taxpayer_last_name"]
        name_in_utility = utility_json["customer_name"]

        similarity_search_docs = [
            name_in_bank,
            name_in_credit,
            name_in_identity,
            name_in_income,
            name_in_tax,
            name_in_utility
        ]

        mismatch_items = self.pairwise_similarity(similarity_search_docs)

        if len(mismatch_items) > 0:
            mismatch_message = {
                'type': "Warning",
                'text': "\n".join(f"- {item.capitalize()}" for item in mismatch_items),
                'message': 'Name inconsistencies detected across documents. Please expand the section below to view the documents with mismatched names.'
                
            }
        else:
            mismatch_message = {
                'type': "Authentic",
                'message': "",
                'text': ""
            }

        return mismatch_message

    def save_fraud_summary(self):
        """
        Run fraud detection and return summary + output path.
        """
        summary = str(self.fraud_detection())
        print(f"The fraud summary is {summary}")

        save_path = f"{self.base_path}/final_output/fraud_report.json"
        return summary, save_path
