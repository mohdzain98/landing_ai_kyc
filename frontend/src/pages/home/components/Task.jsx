import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styling/task.css";
import Spinner from "../../../components/Spinner";
import { v4 as uuidv4 } from "uuid";

const Task = ({ prop }) => {
  const [selectedFiles, setSelectedFiles] = useState({});
  const [loader, setLoader] = useState(false);
  const showAlert = prop?.showAlert;
  const host = "http://127.0.0.1:8000/api";
  const navigate = useNavigate();

  useEffect(() => {
    const tooltipTriggerList = document.querySelectorAll(
      '[data-bs-toggle="tooltip"]'
    );
    const tooltipList = [...tooltipTriggerList].map(
      (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
    );
  }, []);

  const documentGroups = useMemo(
    () => [
      {
        title: "Identity Documents",
        description:
          "Passports, national IDs, or driver’s licenses to verify the applicant.",
        icon: "fa-solid fa-id-card",
        accept: ".pdf,.jpg,.jpeg,.png",
        field: "identity_documents",
      },
      {
        title: "Bank Statements",
        description:
          "Recent bank statements for liquidity verification and cash-flow trends.",
        icon: "fa-solid fa-building-columns",
        accept: ".pdf,.csv,.xlsx",
        field: "bank_statements",
      },
      {
        title: "Tax Statements",
        description:
          "Latest tax returns or filings to confirm declared income and obligations.",
        icon: "fa-solid fa-file-invoice-dollar",
        accept: ".pdf",
        field: "tax_statements",
      },
      {
        title: "Credit Reports",
        description:
          "Bureau-rated credit histories to surface existing liabilities and scores.",
        icon: "fa-solid fa-chart-line",
        accept: ".pdf",
        field: "credit_reports",
      },
      {
        title: "Income Proof",
        description:
          "Payslips, employment letters, or audited financials for income validation.",
        icon: "fa-solid fa-briefcase",
        accept: ".pdf,.jpg,.jpeg,.png",
        field: "income_proof",
      },
      {
        title: "Utility Bills",
        description:
          "monthly invoice for essential services like water, electricity, gas",
        icon: "fa-solid fa-money-bills",
        accept: ".pdf,.jpg,.jpeg,.png",
        field: "utility_bills",
      },
    ],
    []
  );

  // const filesReady = useMemo(
  //   () =>
  //     Object.values(selectedFiles).some(
  //       (files) => Array.isArray(files) && files.length > 0
  //     ),
  //   [selectedFiles]
  // );
  const filesReady = useMemo(() => {
    const values = Object.values(selectedFiles);
    if (values.length < documentGroups.length) return false;
    return values.every((files) => Array.isArray(files) && files.length > 0);
  }, [selectedFiles, documentGroups]);

  const handleProcessDocuments = async (event) => {
    event.preventDefault();
    const sid = uuidv4();
    setLoader(true);
    const payload = Object.entries(selectedFiles).reduce(
      (acc, [category, files]) => {
        if (files && files.length) {
          acc[category] = files;
        }
        return acc;
      },
      {}
    );
    if (Object.keys(payload).length < documentGroups.length) {
      showAlert("Please upload all the document before processing.", "warning");
      setLoader(false);
      return;
    }
    const fd = new FormData();
    const backendFieldByTitle = documentGroups.reduce((acc, group) => {
      acc[group.title] = group.field;
      return acc;
    }, {});
    Object.entries(payload).forEach(([title, files]) => {
      const fieldName = backendFieldByTitle[title];
      if (!fieldName) return;
      files.forEach((file) => {
        fd.append(fieldName, file, file.name);
      });
    });
    const meta = { caseId: sid, source: "react-ui" };
    fd.append("metadata", JSON.stringify(meta));

    try {
      const res = await fetch(`${host}/upload/docs`, {
        method: "POST",
        body: fd,
      });

      if (!res.ok) {
        const text = await res.text();
        console.error("Upload failed:", text);
        showAlert("Some error occurred while uploading documents.", "danger");
        return;
      }

      const json = await res.json();
      showAlert("Documents uploaded successfully.", "success");
      navigate("/outcomes", { state: { caseId: json?.data?.caseId } });
    } catch (error) {
      console.error("Upload error:", error);
      showAlert("Network error while uploading documents.", "danger");
    } finally {
      setLoader(false);
    }
  };

  return (
    <section id="task" className="bg-light">
      <div className="container py-5">
        <div className="text-center mb-5">
          <h2 className="fw-bold">Upload Your Lending Documents</h2>
          <p className="text-muted mb-0">
            Provide the borrower artifacts below so Landing AI can fast-track
            Loan KYC checks.
          </p>
        </div>
        <div className="row g-4 justify-content-center">
          {documentGroups.map((item) => {
            const formats = item.accept
              .split(",")
              .map((format) => format.replace(".", "").toUpperCase())
              .join(" · ");
            return (
              <div key={item.title} className="col-12 col-md-6 col-lg-4">
                <div className="upload-card h-100 shadow-sm">
                  <div className="d-flex align-items-center mb-3">
                    <div className="upload-icon me-3">
                      <i className={`${item.icon}`} aria-hidden="true"></i>
                    </div>
                    <div>
                      <h5 className="mb-1">{item.title}</h5>
                      <small className="text-muted d-block">
                        {item.description}
                      </small>
                    </div>
                  </div>
                  <label className="form-label text-uppercase small fw-semibold text-muted">
                    Upload Files
                  </label>
                  <label className="upload-dropzone mt-2">
                    <input
                      type="file"
                      className="upload-input"
                      accept={item.accept}
                      multiple
                      aria-label={`Upload ${item.title}`}
                      onChange={(event) => {
                        const files = Array.from(event.target.files || []);
                        const dropzone =
                          event.target.closest(".upload-dropzone");
                        if (dropzone) {
                          dropzone.setAttribute(
                            "data-has-files",
                            files.length > 0 ? "true" : "false"
                          );
                        }
                        setSelectedFiles((prev) => ({
                          ...prev,
                          [item.title]: files,
                        }));
                      }}
                    />
                    <i className="fa-solid fa-cloud-arrow-up mb-3"></i>
                    <p className="mb-1 fw-semibold text-dark">
                      Drag &amp; drop or{" "}
                      <span className="text-warning">browse</span>
                    </p>
                    <small className="text-dark-50">
                      {formats} · up to 25MB each
                    </small>
                  </label>
                  <div className="selected-file-list mt-3">
                    {selectedFiles[item.title] &&
                      selectedFiles[item.title].length > 0 && (
                        <ul className="list-unstyled mb-0">
                          {selectedFiles[item.title].map((file, index) => (
                            <li
                              key={`${item.title}-${file.name}-${index}`}
                              className="selected-file-entry"
                            >
                              <i className="fa-solid fa-file-circle-check me-2 text-success" />
                              <span className="file-name">{file.name}</span>
                              <span className="file-size">
                                {` (${(file.size / (1024 * 1024)).toFixed(
                                  1
                                )} MB)`}
                              </span>
                            </li>
                          ))}
                        </ul>
                      )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        <div className="text-center mt-5">
          <button
            type="button"
            className={`btn btn-${
              !filesReady ? "secondary" : "primary"
            } btn-lg px-4 py-2 fw-semibold shadow`}
            onClick={handleProcessDocuments}
            disabled={!filesReady}
            data-toggle="tooltip"
            data-placement="top"
            title="Click to Process the Documents"
          >
            Process Documents
            {loader && <Spinner />}
          </button>
        </div>
      </div>
    </section>
  );
};

export default Task;
