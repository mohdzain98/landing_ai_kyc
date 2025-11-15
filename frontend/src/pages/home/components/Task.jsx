import React, { useContext, useEffect, useMemo, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "../styling/task.css";
import ProcessingBlink from "../../../components/Blink";
import { userContext } from "../../../context/userContext";

const DOC_CONFLICT_REGEX = {
  identity_documents: [
    /(bank|statement)/i,
    /(tax|1040|w[-\s]?2)/i,
    /(credit|bureau)/i,
    /(utility|bill)/i,
    /(pay\s?stub|payslip|salary|income)/i,
  ],
  bank_statements: [
    /(identity|passport|license)/i,
    /(tax|1040|w[-\s]?2)/i,
    /(credit|bureau)/i,
    /(utility|bill)/i,
    /(pay\s?stub|payslip|salary|income)/i,
  ],
  tax_statements: [
    /(identity|passport|license)/i,
    /(bank)/i,
    /(credit|bureau)/i,
    /(utility|bill)/i,
    /(pay\s?stub|payslip|salary|income)/i,
  ],
  credit_reports: [
    /(identity|passport|license)/i,
    /(bank|statement)/i,
    /(tax|1040|w[-\s]?2)/i,
    /(utility|bill)/i,
    /(pay\s?stub|payslip|salary|income)/i,
  ],
  income_proof: [
    /(identity|passport|license)/i,
    /(tax|1040|w[-\s]?2)/i,
    /(utility|bill)/i,
    /(credit|bureau)/i,
    /(bank|statement)/i,
  ],
  utility_bills: [
    /(identity|passport|license)/i,
    /(tax|1040|w[-\s]?2)/i,
    /(credit|bureau)/i,
    /(bank|statement)/i,
    /(pay\s?stub|payslip|salary|income)/i,
  ],
};

const Task = (props) => {
  const { showAlert } = props.prop;
  // const [uploadCount, setUploadCount] = useState(0);
  const navigate = useNavigate();
  const location = useLocation();
  const {
    documentGroups,
    uploadStatuses,
    uploadSummary,
    uploadDocumentGroup,
    caseId,
    uploadCount,
    changeUploadCount,
  } = useContext(userContext);

  useEffect(() => {
    const tooltipTriggerList = document.querySelectorAll(
      '[data-bs-toggle="tooltip"]'
    );
    // Initialize Bootstrap tooltips when available on the page.
    [...tooltipTriggerList].forEach((tooltipTriggerEl) => {
      if (window.bootstrap?.Tooltip) {
        // eslint-disable-next-line no-new
        new window.bootstrap.Tooltip(tooltipTriggerEl);
      }
    });
  }, [location.pathname == "/"]);

  const anyUploadInFlight = useMemo(() => {
    if (!documentGroups || documentGroups.length === 0) {
      return false;
    }
    return documentGroups.some(
      (group) => uploadStatuses[group.key]?.status === "processing"
    );
  }, [documentGroups, uploadStatuses]);

  const handleFileChange = async (group, event) => {
    const inputEl = event.target;
    const files = Array.from(inputEl.files || []);

    if (files.length === 0) {
      return;
    }

    const conflictMatchers = DOC_CONFLICT_REGEX[group.key] || [];

    const conflictFile = files.find((file) =>
      conflictMatchers.some((regex) => regex.test(file.name))
    );

    if (conflictFile) {
      showAlert(
        <>
          The selected file <strong>{conflictFile.name} </strong> doesn't look
          like <strong>{group.title}</strong>. Please double-check and upload
          the correct document.
        </>,
        "warning"
      );
      if (inputEl) {
        inputEl.value = "";
      }
      return;
    }
    try {
      changeUploadCount();
      await uploadDocumentGroup(group.key, files);
      if (inputEl) {
        inputEl.value = "";
      }
    } catch (error) {
      console.error(`Upload failed for ${group.key}`, error);
    }
  };

  const handleProcessDocuments = () => {
    if (!uploadCount == 6) {
      showAlert(
        "Please upload each document before navigating to outcomes.",
        "warning"
      );
      return;
    }

    navigate(`/outcomes/${caseId}`, {
      state: { caseId: uploadSummary.caseId || caseId },
    });
  };

  return (
    <section id="task" className="bg-light">
      <div className="container py-5">
        <div className="text-center mb-5">
          <h2 className="fw-bold">Upload Your Lending Documents</h2>
          <p className="text-muted mb-0">
            Provide the borrower artifacts below so LoanLens AI can fast-track
            loan approval.
          </p>
        </div>
        <div className="row g-4 justify-content-center">
          {documentGroups?.map((item) => {
            const uploadState = uploadStatuses[item.key] || {};
            const formats = item.accept
              .split(",")
              .map((format) => format.replace(".", "").toUpperCase())
              .join(" · ");
            const isUploading = uploadState.status === "processing";
            const isCompleted = uploadState.status === "completed";
            const hasError = uploadState.status === "error";
            const hasFiles =
              Array.isArray(uploadState.filesMeta) &&
              uploadState.filesMeta.length > 0;

            return (
              <div key={item.key} className="col-12 col-md-6 col-lg-4">
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
                  <label
                    className="upload-dropzone mt-2"
                    data-has-files={hasFiles ? "true" : "false"}
                  >
                    <input
                      type="file"
                      className="upload-input"
                      accept={item.accept}
                      multiple
                      aria-label={`Upload ${item.title}`}
                      onChange={(event) => handleFileChange(item, event)}
                    />
                    <i className="fa-solid fa-cloud-arrow-up mb-2"></i>
                    <p className="mb-1 fw-semibold text-dark">
                      Drag &amp; drop or{" "}
                      <span className="text-warning">browse</span>
                    </p>
                    <small className="text-dark-50">{formats}</small>
                  </label>
                  <div className="mt-2">
                    {isUploading && <ProcessingBlink tag="Processing" />}
                    {isCompleted && !hasError && (
                      <small className="text-success fw-semibold">
                        Processed
                      </small>
                    )}
                    {hasError && (
                      <small className="text-danger fw-semibold">
                        Failed to upload. Try again.
                      </small>
                    )}
                  </div>
                  <div className="selected-file-list">
                    {hasFiles && (
                      <ul className="list-unstyled">
                        {uploadState.filesMeta.map((file, index) => (
                          <li
                            key={`${item.key}-${file.name}-${index}`}
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
              uploadCount < 6 ? "secondary" : "primary"
            } btn-lg px-4 py-2 fw-semibold shadow`}
            onClick={handleProcessDocuments}
            disabled={uploadCount < 6}
            // data-bs-toggle="tooltip"
            // data-bs-placement="top"
            // title="Click to view outcomes once all documents are uploaded"
          >
            <i
              className={`fa-solid fa-check-double ${
                uploadCount == 6 && "fa-fade"
              } me-2`}
            ></i>
            See Results
          </button>
        </div>
      </div>
    </section>
  );
};

export default Task;
