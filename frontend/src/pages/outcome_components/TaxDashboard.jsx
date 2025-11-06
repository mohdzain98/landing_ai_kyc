import React, { useMemo } from "react";
import {
  DollarSign,
  TrendingDown,
  Calculator,
  FileText,
  User,
  MapPin,
  ShieldCheck,
  AlertCircle,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from "recharts";

const TAX_BRACKETS_2024_SINGLE = [
  { limit: 11600, rate: 0.1, label: "10%" },
  { limit: 47150, rate: 0.12, label: "12%" },
  { limit: 100525, rate: 0.22, label: "22%" },
  { limit: 191950, rate: 0.24, label: "24%" },
  { limit: 243725, rate: 0.32, label: "32%" },
  { limit: 609350, rate: 0.35, label: "35%" },
  { limit: Infinity, rate: 0.37, label: "37%" },
];

const parseCurrency = (value) => {
  if (value === null || value === undefined || value === "") {
    return null;
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  const cleaned = Number(
    value
      .toString()
      .replace(/[^0-9.-]+/g, "")
      .replace(/(?!^)-/g, "")
  );
  return Number.isFinite(cleaned) ? cleaned : null;
};

const formatCurrency = (value) => {
  if (value === null || value === undefined || !Number.isFinite(value)) {
    return "—";
  }
  return `$${value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
};

const formatPercent = (value, options = {}) => {
  if (value === null || value === undefined || !Number.isFinite(value)) {
    return "—";
  }
  const { precision = 2 } = options;
  return `${value.toFixed(precision)}%`;
};

const formatLabel = (text) =>
  text
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/\b\w/g, (char) => char.toUpperCase());

const maskSsn = (value) => {
  if (!value) {
    return null;
  }
  const digits = value.toString().replace(/\D/g, "");
  if (digits.length < 4) {
    return null;
  }
  return `***-**-${digits.slice(-4)}`;
};

const calculateFederalTax = (taxableIncome) => {
  if (!Number.isFinite(taxableIncome) || taxableIncome <= 0) {
    return { estimatedTax: null, contributions: [] };
  }

  let tax = 0;
  let previousLimit = 0;
  const contributions = [];

  for (const bracket of TAX_BRACKETS_2024_SINGLE) {
    if (taxableIncome <= previousLimit) {
      break;
    }
    const taxableInBracket =
      Math.min(taxableIncome, bracket.limit) - previousLimit;
    const amount = taxableInBracket * bracket.rate;
    tax += amount;
    contributions.push({
      label: bracket.label,
      amount,
      range:
        bracket.limit === Infinity
          ? `$${previousLimit.toLocaleString()}+`
          : `$${previousLimit.toLocaleString()} - $${bracket.limit.toLocaleString()}`,
    });
    previousLimit = bracket.limit;
  }

  return { estimatedTax: tax, contributions };
};

const COLORS = [
  "#0d6efd",
  "#dc3545",
  "#198754",
  "#ffc107",
  "#20c997",
  "#6f42c1",
  "#fd7e14",
];

const TaxReturnDashboard = ({ report = {}, summary }) => {
  const taxpayerName = useMemo(() => {
    const parts = [
      report.taxpayer_first_name,
      report.taxpayer_last_name,
    ].filter(Boolean);
    return parts.length ? parts.join(" ") : "Taxpayer";
  }, [report.taxpayer_first_name, report.taxpayer_last_name]);

  const locationLine = useMemo(() => {
    const parts = [
      report.address_line,
      [report.city, report.state].filter(Boolean).join(", "),
      report.zip_code,
    ]
      .filter(Boolean)
      .join(", ");
    return parts || null;
  }, [report.address_line, report.city, report.state, report.zip_code]);

  const maskedSsn = useMemo(
    () => maskSsn(report.taxpayer_ssn),
    [report.taxpayer_ssn]
  );

  const taxData = useMemo(() => {
    const totalWages = parseCurrency(report.total_wages);
    const totalIncome =
      parseCurrency(report.total_income) ??
      parseCurrency(report.total_wages) ??
      null;
    const adjustedGrossIncome = parseCurrency(report.adjusted_gross_income);
    const standardDeduction = parseCurrency(report.standard_deduction);
    const taxableIncome = parseCurrency(report.taxable_income);
    const totalTax = parseCurrency(report.total_tax);
    const totalPayments = parseCurrency(report.total_payments);
    const refundOrAmountOwed = parseCurrency(report.refund_or_amount_owed);

    return {
      totalWages,
      totalIncome,
      adjustedGrossIncome,
      standardDeduction,
      taxableIncome,
      totalTax,
      totalPayments,
      refundOrAmountOwed,
    };
  }, [
    report.total_wages,
    report.total_income,
    report.adjusted_gross_income,
    report.standard_deduction,
    report.taxable_income,
    report.total_tax,
    report.total_payments,
    report.refund_or_amount_owed,
  ]);

  const taxComputation = useMemo(
    () => calculateFederalTax(taxData.taxableIncome),
    [taxData.taxableIncome]
  );

  const infoItems = [
    ["Occupation", report.occupation],
    ["Signature Date", report.signature_date],
    ["Routing Number", report.routing_number],
  ].filter(([, value]) => Boolean(value));

  const taxItems = [
    ["Total Tax", taxData.totalTax],
    ["Total Payments", taxData.totalPayments],
  ].filter(([, value]) => Number.isFinite(value));

  const hasData = infoItems.length > 0 || taxItems.length > 0;

  const effectiveTaxRate = useMemo(() => {
    if (
      taxComputation.estimatedTax === null ||
      !Number.isFinite(taxData.totalIncome) ||
      taxData.totalIncome === 0
    ) {
      return null;
    }
    return (taxComputation.estimatedTax / taxData.totalIncome) * 100;
  }, [taxComputation.estimatedTax, taxData.totalIncome]);

  const incomeBreakdown = useMemo(() => {
    const items = [];
    if (Number.isFinite(taxData.taxableIncome)) {
      items.push({
        name: "Taxable Income",
        value: taxData.taxableIncome,
        color: COLORS[1],
      });
    }
    if (Number.isFinite(taxData.standardDeduction)) {
      items.push({
        name: "Standard Deduction",
        value: taxData.standardDeduction,
        color: COLORS[2],
      });
    }
    if (Number.isFinite(taxData.totalIncome)) {
      items.push({
        name: "Reported Income",
        value: taxData.totalIncome,
        color: COLORS[0],
      });
    }
    return items;
  }, [taxData]);

  const calculationSteps = useMemo(() => {
    const steps = [
      {
        label: "Total Wages",
        value: taxData.totalWages,
      },
      {
        label: "Total Income",
        value:
          taxData.totalIncome !== taxData.totalWages
            ? taxData.totalIncome
            : null,
      },
      {
        label: "Adjusted Gross Income",
        value: taxData.adjustedGrossIncome,
      },
      {
        label: "Standard Deduction",
        value: taxData.standardDeduction
          ? -1 * taxData.standardDeduction
          : null,
      },
      {
        label: "Taxable Income",
        value: taxData.taxableIncome,
      },
    ].filter((item) => Number.isFinite(item.value) && item.value !== 0);

    return steps.map((item) => ({
      step: item.label,
      amount: item.value,
    }));
  }, [taxData]);

  const summaryParagraphs = useMemo(() => {
    if (!summary || typeof summary !== "string") {
      return [];
    }
    return summary
      .split(/\n+/)
      .map((line) => line.trim())
      .filter(Boolean);
  }, [summary]);

  const highlights = useMemo(() => {
    const items = [
      Number.isFinite(taxData.taxableIncome) && {
        icon: Calculator,
        label: "Taxable Income",
        value: formatCurrency(taxData.taxableIncome),
        helper: "Income subject to federal tax after deductions.",
      },
      Number.isFinite(taxComputation.estimatedTax) && {
        icon: DollarSign,
        label: "Estimated Federal Tax",
        value: formatCurrency(taxComputation.estimatedTax),
        helper:
          "Approximate liability based on 2024 brackets for a single filer.",
      },
      Number.isFinite(effectiveTaxRate) && {
        icon: ShieldCheck,
        label: "Effective Tax Rate",
        value: formatPercent(effectiveTaxRate, { precision: 1 }),
        helper: "Total tax as a percentage of reported income.",
      },
      Number.isFinite(taxData.refundOrAmountOwed) && {
        icon: AlertCircle,
        label:
          taxData.refundOrAmountOwed >= 0 ? "Amount Owed" : "Estimated Refund",
        value: formatCurrency(Math.abs(taxData.refundOrAmountOwed)),
        helper:
          taxData.refundOrAmountOwed >= 0
            ? "Additional tax expected after payments."
            : "Approximate refund once payments are reconciled.",
      },
    ].filter(Boolean);
    return items;
  }, [taxData, taxComputation, effectiveTaxRate]);

  const bracketBarData = useMemo(
    () =>
      taxComputation.contributions.map((item) => ({
        name: item.label,
        amount: Number(item.amount.toFixed(2)),
        range: item.range,
      })),
    [taxComputation.contributions]
  );

  const hasIncomeBreakdown =
    incomeBreakdown.length > 0 &&
    incomeBreakdown.some((item) => Number.isFinite(item.value));

  const hasCalculationSteps =
    calculationSteps.length > 0 &&
    calculationSteps.some((item) => Number.isFinite(item.amount));

  const hasBracketBars =
    bracketBarData.length > 0 &&
    bracketBarData.some((item) => Number.isFinite(item.amount));

  return (
    <div className="min-vh-100 py-4 px-3">
      <div className="container" style={{ maxWidth: "1280px" }}>
        <div className="card shadow-sm mb-4 border-0 border-top border-primary border-5">
          <div className="card-body p-4 p-md-5">
            <div className="row gy-4 align-items-center">
              <div className="col-md-8">
                <h1 className="display-6 fw-bold text-dark mb-3">
                  Tax Return Summary
                </h1>
                <div className="d-flex align-items-center gap-2 text-secondary mb-2">
                  <User size={16} />
                  <p className="mb-0 fw-semibold">{taxpayerName}</p>
                </div>
                {locationLine && (
                  <div className="d-flex align-items-center gap-2 text-muted small">
                    <MapPin size={16} />
                    <p className="mb-0">{locationLine}</p>
                  </div>
                )}
              </div>
              <div className="col-md-4 text-md-end">
                {maskedSsn && (
                  <div className="border rounded p-3 d-inline-block">
                    <p className="small text-primary fw-medium mb-1">SSN</p>
                    <p className="mb-0 fw-bold font-monospace">{maskedSsn}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {highlights.length > 0 && (
          <div className="row g-3 g-md-4 mb-4">
            {highlights.map((item, index) => {
              const Icon = item.icon;
              return (
                <div className="col-sm-6 col-lg-3" key={item.label}>
                  <div
                    className="card shadow-sm h-100 text-white border-0"
                    style={{
                      background: `linear-gradient(135deg, ${
                        COLORS[index % COLORS.length]
                      } 0%, rgba(0,0,0,0.25) 100%)`,
                    }}
                  >
                    <div className="card-body p-4">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <span className="small fw-medium opacity-75">
                          {item.label}
                        </span>
                        <Icon size={22} className="opacity-75" />
                      </div>
                      <p className="fw-bold fs-5 mb-1">{item.value}</p>
                      {item.helper && (
                        <p className="small mb-0 opacity-75">{item.helper}</p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        <div className="row g-4 mb-4">
          {hasIncomeBreakdown && (
            <div className="col-lg-5">
              <div className="card shadow-sm h-100">
                <div className="card-body p-4">
                  <div className="d-flex justify-content-between align-items-center mb-3">
                    <h2 className="h6 fw-bold text-dark mb-0">
                      Income Composition
                    </h2>
                    <FileText size={18} className="text-primary" />
                  </div>
                  <div style={{ width: "100%", height: 260 }}>
                    <ResponsiveContainer>
                      <PieChart>
                        <Pie
                          data={incomeBreakdown}
                          dataKey="value"
                          nameKey="name"
                          innerRadius={55}
                          outerRadius={95}
                          paddingAngle={4}
                        >
                          {incomeBreakdown.map((entry, idx) => (
                            <Cell
                              key={entry.name}
                              fill={entry.color || COLORS[idx % COLORS.length]}
                            />
                          ))}
                        </Pie>
                        <Tooltip
                          formatter={(value, name) => [
                            formatCurrency(value),
                            name,
                          ]}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <ul className="list-unstyled small mb-0">
                    {incomeBreakdown.map((item) => (
                      <li
                        key={item.name}
                        className="d-flex justify-content-between align-items-center py-1"
                      >
                        <span>{item.name}</span>
                        <span className="fw-semibold">
                          {formatCurrency(item.value)}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {hasCalculationSteps && (
            <div className="col-lg-7">
              <div className="card shadow-sm h-100">
                <div className="card-body p-4">
                  <div className="d-flex justify-content-between align-items-center mb-3">
                    <h2 className="h6 fw-bold text-dark mb-0">
                      Taxable Income Walkthrough
                    </h2>
                    <Calculator size={18} className="text-primary" />
                  </div>
                  <div style={{ width: "100%", height: 260 }}>
                    <ResponsiveContainer>
                      <BarChart data={calculationSteps}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="step" tick={{ fontSize: 12 }} />
                        <YAxis />
                        <Tooltip
                          formatter={(value, name) => [
                            formatCurrency(value),
                            name,
                          ]}
                        />
                        <Bar dataKey="amount" fill="#0d6efd" radius={4} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {hasBracketBars && (
          <div className="card shadow-sm mb-4">
            <div className="card-body p-4">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h2 className="h6 fw-bold text-dark mb-0">
                  Estimated Tax By Bracket
                </h2>
                <TrendingDown size={18} className="text-danger" />
              </div>
              <div style={{ width: "100%", height: 260 }}>
                <ResponsiveContainer>
                  <BarChart data={bracketBarData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip
                      formatter={(value, name, { payload }) => [
                        formatCurrency(value),
                        `${name} (${payload.range})`,
                      ]}
                    />
                    <Bar dataKey="amount" fill="#dc3545" radius={6} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        <div className="row g-4 mb-4">
          <div className="col-lg-6">
            <div className="card shadow-sm h-100">
              <div className="card-body p-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h2 className="h6 fw-bold text-dark mb-0">Return Details</h2>
                  <FileText size={18} className="text-secondary" />
                </div>
                <div className="row gy-3">
                  {hasData ? (
                    <>
                      {infoItems.map(([label, value]) => (
                        <div className="col-sm-6" key={label}>
                          <p className="text-muted small mb-1">{label}</p>
                          <p className="fw-semibold mb-0">{value}</p>
                        </div>
                      ))}
                      {taxItems.map(([label, value]) => (
                        <div className="col-sm-6" key={label}>
                          <p className="text-muted small mb-1">{label}</p>
                          <p className="fw-semibold mb-0">
                            {formatCurrency(value)}
                          </p>
                        </div>
                      ))}
                    </>
                  ) : (
                    <div className="col-12 text-center text-muted text-uppercase">
                      No data available
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="col-lg-6">
            <div className="card shadow-sm h-100">
              <div className="card-body p-4">
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <h2 className="h6 fw-bold text-dark mb-0">
                    Additional Insight
                  </h2>
                  <ShieldCheck size={18} className="text-success" />
                </div>
                <ul className="list-unstyled mb-0">
                  {highlights.length === 0 && (
                    <li className="text-muted small">
                      No taxable income metrics were detected in this return.
                    </li>
                  )}
                  {highlights.map((item) => (
                    <li
                      key={`${item.label}-insight`}
                      className="d-flex flex-column border rounded p-3 mb-2"
                      style={{ borderLeft: "4px solid #0d6efd" }}
                    >
                      <span className="fw-semibold">{item.label}</span>
                      <span className="text-muted small">{item.value}</span>
                      {item.helper && (
                        <span className="text-muted small mt-1">
                          {item.helper}
                        </span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {summaryParagraphs.length > 0 && (
          <div className="card shadow-sm mb-4">
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
  );
};

export default TaxReturnDashboard;
