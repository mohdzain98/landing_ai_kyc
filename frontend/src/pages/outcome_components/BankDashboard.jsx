import React, { useState, useMemo } from "react";
// import {
//   PieChart,
//   Pie,
//   Cell,
//   BarChart,
//   Bar,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
//   ResponsiveContainer,
//   LineChart,
//   Line,
// } from "recharts";
import {
  // DollarSign,
  // TrendingDown,
  // TrendingUp,
  // AlertCircle,
  FileText,
} from "lucide-react";

const BankStatementDashboard = ({
  transaction,
  summary = "Unable to get summary",
}) => {
  const [activeView, setActiveView] = useState("transactions");
  console.log("transactions", transaction);
  const styles = `
    <style>
      .insight-card { border-left: 4px solid; padding-left: 1rem; padding-top: 0.5rem; padding-bottom: 0.5rem; }
      .insight-blue { border-color: #0d6efd; }
      .insight-red { border-color: #dc3545; }
      .insight-amber { border-color: #ffc107; }
      .insight-purple { border-color: #6f42c1; }
      .nav-btn { transition: all 0.3s; }
      .nav-btn:hover { background-color: #e9ecef; }
      .nav-btn.active { background-color: #0d6efd; color: white; }
      .table-hover tbody tr:hover { background-color: #f8f9fa; }
    </style>
  `;

  const transactions = transaction.transactions_table;

  function parseAmount(value) {
    if (typeof value === "string") {
      // Remove commas and extra spaces
      value = value.replace(/,/g, "").trim();
    }
    let num = Number(value);
    return isNaN(num) ? 0 : num;
  }

  // const OpeningBalance = parseAmount(transaction.transactions_table[0].amount);
  // // Calculate totals
  // const totalCredits = transactions
  //   .filter((t) => t.type === "Credit")
  //   .reduce((sum, t) => sum + parseAmount(t.amount), 0);

  // const totalDebits = transactions
  //   .filter((t) => t.type === "Debit")
  //   .reduce((sum, t) => sum + parseAmount(t.amount), 0);

  // const netChange = totalCredits - totalDebits;
  // const finalBalance = OpeningBalance + netChange;

  // Category breakdown
  // const categories = {
  //   Payroll: 0,
  //   "Bill Payments": 0,
  //   Purchases: 0,
  //   Transfers: 0,
  //   Fees: 0,
  //   Mortgage: 0,
  //   ATM: 0,
  //   Refunds: 0,
  //   Cheques: 0,
  // };

  // transactions.forEach((t) => {
  //   if (t.description.includes("Payroll"))
  //     categories["Payroll"] += t.type === "Credit" ? t.amount : -t.amount;
  //   else if (t.description.includes("Bill Payment"))
  //     categories["Bill Payments"] -= t.amount;
  //   else if (t.description.includes("Purchase"))
  //     categories["Purchases"] -= t.amount;
  //   else if (t.description.includes("Transfer"))
  //     categories["Transfers"] -= t.amount;
  //   else if (t.description.includes("Fee")) categories["Fees"] -= t.amount;
  //   else if (t.description.includes("Mortgage"))
  //     categories["Mortgage"] -= t.amount;
  //   else if (t.description.includes("ATM")) categories["ATM"] -= t.amount;
  //   else if (t.description.includes("Refund"))
  //     categories["Refunds"] += t.amount;
  //   else if (t.description.includes("Cheque"))
  //     categories["Cheques"] -= t.amount;
  // });

  // const categoryData = Object.entries(categories)
  //   .filter(([_, value]) => value !== 0)
  //   .map(([name, value]) => ({ name, value: Math.abs(value) }));

  // const creditDebitData = [
  //   { name: "Credits", value: totalCredits, color: "#10b981" },
  //   { name: "Debits", value: totalDebits, color: "#ef4444" },
  // ];

  // const COLORS = [
  //   "#3b82f6",
  //   "#ef4444",
  //   "#f59e0b",
  //   "#8b5cf6",
  //   "#ec4899",
  //   "#14b8a6",
  //   "#f97316",
  //   "#10b981",
  //   "#6366f1",
  // ];
  function parseTransactionDate(str) {
    const [mon, yr, day] = str.split("-");
    // convert "01" -> 2001
    const fullYear = 2000 + parseInt(yr, 10);
    return new Date(`${mon} ${day}, ${fullYear}`);
  }
  const firstDate = parseTransactionDate(transactions[1].date);
  const lastDate = parseTransactionDate(
    transactions[transactions.length - 1].date
  );
  const startDate = {
    month: firstDate.toLocaleString("en-US", { month: "short" }),
    year: firstDate.getFullYear(),
  };
  const endDate = {
    month: lastDate.toLocaleString("en-US", { month: "short" }),
    year: lastDate.getFullYear(),
  };

  const summaryParagraphs = useMemo(() => {
    if (!summary || typeof summary !== "string") {
      return [];
    }
    return summary
      .split(/\n+/)
      .map((line) => line.trim())
      .filter(Boolean);
  }, [summary]);

  return (
    <>
      <div dangerouslySetInnerHTML={{ __html: styles }} />
      <div className="min-vh-100 py-4 px-3">
        <div className="container" style={{ maxWidth: "1100px" }}>
          {/* Header */}
          <div className="card shadow-sm mb-4 border-0 border-top border-primary border-5">
            <div className="card-body p-4 p-md-5">
              <div className="d-flex justify-content-between align-items-start flex-wrap ">
                <div>
                  <h1 className="h3 fw-bold text-dark mb-3">
                    Bank Statement Analysis
                  </h1>
                  <p className="text-muted mt-1 mb-1">
                    {transaction.account_holder_name} • {transaction.bank_name}
                  </p>
                  <p className="text-muted small mb-0">
                    Account: {transaction.account_number_masked}
                  </p>
                </div>
                {/* <div className="text-end">
                  <p className="text-muted small mb-1">Statement Period</p>
                  <p className="fs-6 fw-semibold text-secondary">
                    {startDate.month} {startDate.year} to {endDate.month}
                    {endDate.year}
                  </p>
                </div> */}
              </div>
            </div>
          </div>

          {/* Summary Cards */}
          {/* <div className="row g-3 mb-4">
            <div className="col-12 col-sm-6 col-lg-3">
              <div className="card shadow-sm h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="text-muted small fw-medium">
                      Opening Balance
                    </span>
                    <DollarSign className="text-primary" size={20} />
                  </div>
                  <p className="h4 fw-bold text-dark mb-0">
                    ${OpeningBalance.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>

            <div className="col-12 col-sm-6 col-lg-3">
              <div className="card shadow-sm h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="text-muted small fw-medium">
                      Total Credits
                    </span>
                    <TrendingUp className="text-success" size={20} />
                  </div>
                  <p className="h4 fw-bold text-success mb-0">
                    ${totalCredits.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>

            <div className="col-12 col-sm-6 col-lg-3">
              <div className="card shadow-sm h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="text-muted small fw-medium">
                      Total Debits
                    </span>
                    <TrendingDown className="text-danger" size={20} />
                  </div>
                  <p className="h4 fw-bold text-danger mb-0">
                    ${totalDebits.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>

            <div className="col-12 col-sm-6 col-lg-3">
              <div className="card shadow-sm h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <span className="text-muted small fw-medium">
                      Estimated Balance
                    </span>
                    <AlertCircle className="text-warning" size={20} />
                  </div>
                  <p
                    className={`h4 fw-bold mb-0 ${
                      finalBalance >= 0 ? "text-dark" : "text-danger"
                    }`}
                  >
                    ${finalBalance.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          </div> */}

          {/* Navigation Tabs */}
          <div className="card shadow-sm mb-4">
            <div className="card-body p-2">
              <div className="d-flex gap-2">
                {/* <button
                  onClick={() => setActiveView("summary")}
                  className={`flex-fill btn fw-medium nav-btn ${
                    activeView === "summary" ? "active" : "btn-light"
                  }`}
                >
                  Summary
                </button> */}
                {/* <button
                  onClick={() => setActiveView("categories")}
                  className={`flex-fill btn fw-medium nav-btn ${
                    activeView === "categories" ? "active" : "btn-light"
                  }`}
                >
                  Categories
                </button> */}
                <button
                  onClick={() => setActiveView("transactions")}
                  className={`flex-fill btn fw-medium nav-btn ${
                    activeView === "transactions" ? "active" : "btn-light"
                  }`}
                >
                  Transactions
                </button>
              </div>
            </div>
          </div>

          {/* Charts */}
          {/* {activeView === "summary" && (
            <div className="row g-4">
              <div className="col-12 col-lg-12">
                <div className="card shadow-sm h-100">
                  <div className="card-body">
                    <h3 className="h5 fw-semibold text-dark mb-3">
                      Credits vs Debits
                    </h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={creditDebitData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, value }) =>
                            `${name}: ${value.toFixed(2)}`
                          }
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {creditDebitData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeView === "categories" && (
            <div className="card shadow-sm">
              <div className="card-body">
                <h3 className="h5 fw-semibold text-dark mb-3">
                  Spending by Category
                </h3>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={categoryData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                      dataKey="name"
                      angle={-45}
                      textAnchor="end"
                      height={100}
                    />
                    <YAxis />
                    <Tooltip formatter={(value) => `${value.toFixed(2)}`} />
                    <Bar dataKey="value" fill="#3b82f6">
                      {categoryData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )} */}

          {activeView === "transactions" && (
            <div className="card shadow-sm">
              <div className="card-body">
                <h3 className="h5 fw-semibold text-dark mb-3">
                  Transaction History
                </h3>
                <div className="table-responsive">
                  <table className="table table-hover align-middle">
                    <thead>
                      <tr className="border-bottom border-2">
                        <th className="text-muted fw-semibold">Date</th>
                        <th className="text-muted fw-semibold">Description</th>
                        <th className="text-muted fw-semibold text-end">
                          Amount($)
                        </th>
                        <th className="text-muted fw-semibold text-center">
                          Type
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {transactions.map((t, idx) => (
                        <tr key={idx}>
                          <td className="text-dark">{t.date}</td>
                          <td className="text-dark">{t.description}</td>
                          <td
                            className={`text-end fw-semibold ${
                              t.type === "Credit"
                                ? "text-success"
                                : t.type === "Debit"
                                ? "text-danger"
                                : "text-dark"
                            }`}
                          >
                            {/* {parseAmount(t.amount).toFixed(2)} */}
                            {t.amount}
                          </td>
                          <td className="text-center">
                            {t.type && (
                              <span
                                className={`badge ${
                                  t.type === "Credit"
                                    ? "bg-success-subtle text-success"
                                    : "bg-danger-subtle text-danger"
                                }`}
                              >
                                {t.type}
                              </span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
          {summaryParagraphs.length > 0 && (
            <div className="card shadow-sm mb-0 mt-3">
              <div className="card-body p-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h2 className="h6 fw-bold text-dark mb-0">Summary</h2>
                  <FileText size={18} className="text-primary" />
                </div>
                <div className="text-muted">
                  {summaryParagraphs.map((paragraph, idx) => (
                    <p key={idx} className="mb-3">
                      {paragraph}
                    </p>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default BankStatementDashboard;
