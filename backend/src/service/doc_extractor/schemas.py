from pydantic import BaseModel, Field

class TransactionRow(BaseModel):
    date: str = Field(description="Date of the transaction, if available")
    description: str = Field(description="Description or details of the transaction")
    amount: str = Field(description="Amount involved in the transaction")
    type: str = Field(description="Type of transaction such as Credit, Debit, or Transfer")

class Account(BaseModel):
    account_holder_name: str = Field(description="Name of the account holder as mentioned in the document")
    bank_name: str = Field(description="Name of the bank")
    account_number_masked: str = Field(description="Account number as shown in the document")
    transactions_table: list[TransactionRow] = Field(description="Table of transactions extracted from the document")

class IdentityDocument(BaseModel):
    full_name: str = Field(description="Full name of the passport holder as mentioned in the document")
    date_of_birth: str = Field(description="Date of birth of the passport holder")
    address: str = Field(description="Residential address of the passport holder")
    passport_number: str = Field(description="Unique passport number assigned to the holder")
    expiry_date: str = Field(description="Passport expiry date")
    issuing_country: str = Field(description="Country that issued the passport")

class TaxStatement(BaseModel):
    employer_name_ein: str = Field(description="Employer name along with Employer Identification Number (EIN) as mentioned in the tax statement")
    annual_wages: str = Field(description="Total annual wages or salary reported in the tax statement")
    tax_withheld: str = Field(description="Total tax amount withheld during the year as shown in the tax statement")
    ytd_income: str = Field(description="Year-to-date income up to the reporting period as mentioned in the tax statement")


class CreditReport(BaseModel):
    credit_score: str = Field(description="Credit score (such as FICO) of the individual as mentioned in the credit report")
    total_debt: str = Field(description="Total outstanding debt amount across all credit accounts")
    open_credit_lines: str = Field(description="Number of open credit lines or active credit accounts")
    monthly_debt_payments: str = Field(description="Total monthly debt payment obligations")
    delinquencies_defaults_collections: str = Field(description="Summary of any delinquencies, defaults, or collection accounts reported")
    bankruptcy_history: str = Field(description="Details about any bankruptcy filings or history present in the credit report")
    hard_inquiries_last_12_months: str = Field(description="Number of hard credit inquiries made in the past 12 months")


class IncomeProof(BaseModel):
    employer_name: str = Field(description="Name of the employer as mentioned on the pay slip or income proof document")
    pay_period: str = Field(description="Pay period or duration covered by the income statement")
    gross_pay: str = Field(description="Total gross pay before deductions for the specified pay period")
    net_pay: str = Field(description="Net pay received after all deductions")
    ytd_earnings: str = Field(description="Year-to-date total earnings as shown in the income proof")
    bonus_commission: str = Field(description="Details of any bonuses or commissions earned during the pay period")
    deductions: str = Field(description="Breakdown of deductions such as benefits, tax, retirement contributions, and insurance")

class UtilityBill(BaseModel):
    bill_for: str = Field(description="Type of utility service the bill is for, such as Electricity, Water, Internet, or Gas")
    amount: str = Field(description="Total amount due as mentioned in the utility bill")