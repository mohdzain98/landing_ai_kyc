import json
import logging
from datetime import datetime
from collections import defaultdict
from typing import Optional, Dict
from pathlib import Path
from src.service.doc_extractor.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

class BankStatementKPIService:
    
    def parse_amount(self, amount: str) -> float:
        """Convert string amount to float safely."""
        try:
            return float(amount.replace(",", "").replace("$", "").strip())
        except Exception as e:
            logger.error(f"Error parsing amount '{amount}': {e}")
            return 0.0

    def get_month_key(self, date_str: str) -> Optional[str]:
        """Convert date string into 'YYYY-MM' format, supporting multiple formats."""
        for fmt in ("%d %b %Y", "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m")
            except ValueError:
                continue
        logger.warning(f"Unrecognized date format: {date_str}")
        return None

    def calculate_bank_kpis(
        self,
        statement: dict,
        daily_balances: Optional[Dict[str, float]] = None,
        opening_balance: Optional[float] = None
    ) -> dict:
        """Calculate key KPIs from bank statement transactions."""
        try:
            transactions = statement.get("transactions_table", [])
            if not transactions:
                logger.warning("No transactions found in statement.")
                return {
                    "average_monthly_transaction_count": None,
                    "monthly_average_debit": None,
                    "monthly_average_credit": None,
                    "average_monthly_debit_credit_ratio": None,
                    "average_monthly_balance": None
                }

            monthly_data = defaultdict(lambda: {"count": 0, "debits": 0.0, "credits": 0.0})

            # Process each transaction
            for txn in transactions:
                date_str = txn.get("date")
                txn_type = txn.get("type", "").lower()
                amount_str = txn.get("amount", "0")

                if not date_str:
                    logger.warning(f"Skipping transaction with missing date: {txn}")
                    continue

                month = self.get_month_key(date_str)
                if not month:
                    logger.warning(f"Skipping transaction with invalid date format: {date_str}")
                    continue

                amount = self.parse_amount(amount_str)
                monthly_data[month]["count"] += 1
                if txn_type == "debit":
                    monthly_data[month]["debits"] += amount
                else:
                    monthly_data[month]["credits"] += amount

            months = list(monthly_data.keys())
            n_months = len(months)

            def safe_div(a, b):
                return a / b if (b and b != 0) else None

            avg_txn_count = safe_div(sum(m["count"] for m in monthly_data.values()), n_months)
            avg_debit = safe_div(sum(m["debits"] for m in monthly_data.values()), n_months)
            avg_credit = safe_div(sum(m["credits"] for m in monthly_data.values()), n_months)
            debit_credit_ratio = safe_div(avg_debit, avg_credit)

            # --- Average Monthly Balance Calculation ---
            avg_monthly_balance = None

            if daily_balances:
                monthly_balances = defaultdict(list)
                for date_str, bal in daily_balances.items():
                    try:
                        for fmt in ("%Y-%m-%d", "%d %b %Y", "%d-%m-%Y"):
                            try:
                                dt = datetime.strptime(date_str.strip(), fmt)
                                break
                            except ValueError:
                                dt = None
                        if not dt:
                            continue
                        monthly_balances[dt.strftime("%Y-%m")].append(bal)
                    except Exception as e:
                        logger.error(f"Error processing daily balance '{date_str}': {e}")

                if monthly_balances:
                    avg_monthly_balance = sum(
                        sum(bals) / len(bals) for bals in monthly_balances.values()
                    ) / len(monthly_balances)

            elif opening_balance is not None:
                daily_net = defaultdict(float)
                for txn in transactions:
                    for fmt in ("%d %b %Y", "%Y-%m-%d", "%d-%m-%Y"):
                        try:
                            dt_key = datetime.strptime(txn["date"], fmt).strftime("%Y-%m-%d")
                            break
                        except ValueError:
                            dt_key = None
                    if not dt_key:
                        continue
                    amount = self.parse_amount(txn["amount"])
                    daily_net[dt_key] += -amount if txn["type"].lower() == "debit" else amount

                if daily_net:
                    bal = opening_balance
                    monthly_balances = defaultdict(list)
                    for d in sorted(daily_net.keys()):
                        bal += daily_net[d]
                        key = datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m")
                        monthly_balances[key].append(bal)

                    avg_monthly_balance = sum(
                        sum(bals) / len(bals) for bals in monthly_balances.values()
                    ) / len(monthly_balances)

            result = {
                "average_monthly_transaction_count": round(avg_txn_count, 2) if avg_txn_count else None,
                "monthly_average_debit": round(avg_debit, 2) if avg_debit else None,
                "monthly_average_credit": round(avg_credit, 2) if avg_credit else None,
                "average_monthly_debit_credit_ratio": round(debit_credit_ratio, 4) if debit_credit_ratio else None,
                "average_monthly_balance": round(avg_monthly_balance, 2) if avg_monthly_balance else None
            }

            logger.info(f"Bank KPI calculation completed successfully for {n_months} months.")
            return result

        except Exception as e:
            logger.exception(f"Unexpected error while calculating bank KPIs: {e}")
            return {"error": str(e)}

    def save_json_to_file(self, data: dict, base_path: str, document_type: str) -> Optional[str]:
        """Save JSON object to 'base_path/output/{document_type}.json'."""
        try:
            file_path = Path(base_path) /f"{document_type}"/ "output"/ f"{document_type}_kpis.json"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"JSON saved successfully at {file_path}")
            return str(file_path)
        except Exception as e:
            logger.exception(f"Error saving JSON file: {e}")
            return None
