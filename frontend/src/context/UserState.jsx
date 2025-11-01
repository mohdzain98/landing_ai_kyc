import React, {
  useCallback,
  useEffect,
  useMemo,
  useState,
  useRef,
} from "react";
import { v4 as uuidv4 } from "uuid";
import { userContext } from "./userContext";

const API_HOST = "http://127.0.0.1:8000/api";

const DOCUMENT_GROUPS = [
  {
    key: "identity_documents",
    title: "Identity Documents",
    description:
      "Passports, national IDs, or driver’s licenses to verify the applicant.",
    icon: "fa-solid fa-id-card",
    accept: ".pdf,.jpg,.jpeg,.png",
    endpoint: "upload/identity_document",
    formField: "identity_documents",
    successMessage: "Identity documents uploaded successfully.",
    errorMessage: "Unable to upload identity documents.",
  },
  {
    key: "bank_statements",
    title: "Bank Statements",
    description:
      "Recent bank statements for liquidity verification and cash-flow trends.",
    icon: "fa-solid fa-building-columns",
    accept: ".pdf,.csv,.xlsx",
    endpoint: "upload/bank_statement",
    formField: "bank_statements",
    successMessage: "Bank statements uploaded successfully.",
    errorMessage: "Unable to upload bank statements.",
  },
  {
    key: "tax_statements",
    title: "Tax Statements",
    description:
      "Latest tax returns or filings to confirm declared income and obligations.",
    icon: "fa-solid fa-file-invoice-dollar",
    accept: ".pdf",
    endpoint: "upload/tax_statement",
    formField: "tax_statements",
    successMessage: "Tax statements uploaded successfully.",
    errorMessage: "Unable to upload tax statements.",
  },
  {
    key: "credit_reports",
    title: "Credit Reports",
    description:
      "Bureau-rated credit histories to surface existing liabilities and scores.",
    icon: "fa-solid fa-chart-line",
    accept: ".pdf",
    endpoint: "upload/credit_report",
    formField: "credit_reports",
    successMessage: "Credit reports uploaded successfully.",
    errorMessage: "Unable to upload credit reports.",
  },
  {
    key: "income_proof",
    title: "Income Proof",
    description:
      "Payslips, employment letters, or audited financials for income validation.",
    icon: "fa-solid fa-briefcase",
    accept: ".pdf,.jpg,.jpeg,.png",
    endpoint: "upload/income_proof",
    formField: "income_proof",
    successMessage: "Income proof uploaded successfully.",
    errorMessage: "Unable to upload income proof.",
  },
  {
    key: "utility_bills",
    title: "Utility Bills",
    description:
      "Monthly invoice for essential services like water, electricity, gas.",
    icon: "fa-solid fa-money-bills",
    accept: ".pdf,.jpg,.jpeg,.png",
    endpoint: "upload/utility_bills",
    formField: "utility_bills",
    successMessage: "Utility bills uploaded successfully.",
    errorMessage: "Unable to upload utility bills.",
  },
];

const createInitialUploadState = () =>
  DOCUMENT_GROUPS.reduce((acc, group) => {
    acc[group.key] = {
      status: "idle",
      error: null,
      response: null,
      filesMeta: [],
      updatedAt: null,
    };
    return acc;
  }, {});

const UserState = ({ children, prop }) => {
  const showAlert = prop?.showAlert;
  const [uploads, setUploads] = useState(() => createInitialUploadState());
  const [summary, setSummary] = useState({
    completed: 0,
    total: DOCUMENT_GROUPS.length,
    lastUpdated: null,
    caseId: null,
  });
  const caseIdRef = useRef(uuidv4());

  const resetUploads = useCallback(() => {
    setUploads(createInitialUploadState());
    setSummary({
      completed: 0,
      total: DOCUMENT_GROUPS.length,
      lastUpdated: null,
      caseId: caseIdRef.current,
    });
  }, []);

  const uploadDocumentGroup = useCallback(
    async (groupKey, filesOrFile) => {
      const fileList = Array.isArray(filesOrFile)
        ? filesOrFile
        : filesOrFile
        ? [filesOrFile]
        : [];

      if (fileList.length === 0) {
        return;
      }
      const group = DOCUMENT_GROUPS.find((item) => item.key === groupKey);
      if (!group) {
        console.warn(
          `Unknown document group "${groupKey}" supplied to upload.`
        );
        return;
      }

      const [primaryFile] = fileList;
      const filesMeta = [
        {
          name: primaryFile.name,
          size: primaryFile.size,
        },
      ];
      setUploads((prev) => ({
        ...prev,
        [groupKey]: {
          ...prev[groupKey],
          status: "uploading",
          error: null,
          filesMeta,
          updatedAt: Date.now(),
        },
      }));

      const fd = new FormData();
      const formField = group.formField || group.key;
      fd.append(formField, primaryFile, primaryFile.name);
      const meta = {
        caseId: caseIdRef.current,
        documentType: group.key,
        source: "react-ui",
      };
      fd.append("metadata", JSON.stringify(meta));
      try {
        const response = await fetch(`${API_HOST}/${group.endpoint}`, {
          method: "POST",
          body: fd,
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || "Upload failed");
        }

        const data = await response.json().catch(() => ({}));

        setUploads((prev) => ({
          ...prev,
          [groupKey]: {
            ...prev[groupKey],
            status: "completed",
            error: null,
            response: data,
            updatedAt: Date.now(),
          },
        }));

        if (data?.data?.caseId && caseIdRef.current !== data.data.caseId) {
          caseIdRef.current = data.data.caseId;
        }

        showAlert(group.successMessage, "success");
        return data;
      } catch (error) {
        console.error(`Upload error for ${group.key}:`, error);

        setUploads((prev) => ({
          ...prev,
          [groupKey]: {
            ...prev[groupKey],
            status: "error",
            error: error.message || "Unknown error",
            updatedAt: Date.now(),
          },
        }));
        showAlert(group.errorMessage, "danger");
        throw error;
      }
    },
    [showAlert]
  );

  useEffect(() => {
    const completed = Object.values(uploads).filter(
      (item) => item.status === "completed"
    ).length;

    const lastUpdated = Object.values(uploads).reduce((latest, item) => {
      if (!item.updatedAt) {
        return latest;
      }
      if (!latest || item.updatedAt > latest) {
        return item.updatedAt;
      }
      return latest;
    }, null);

    setSummary((prev) => ({
      ...prev,
      completed,
      lastUpdated,
      caseId: caseIdRef.current,
    }));
  }, [uploads]);

  const value = useMemo(
    () => ({
      documentGroups: DOCUMENT_GROUPS,
      uploadStatuses: uploads,
      uploadSummary: summary,
      uploadDocumentGroup,
      resetUploads,
      caseId: caseIdRef.current,
    }),
    [uploads, summary, uploadDocumentGroup, resetUploads]
  );

  return <userContext.Provider value={value}>{children}</userContext.Provider>;
};

export default UserState;
