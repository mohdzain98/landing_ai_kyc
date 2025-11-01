import React, { useContext, useEffect, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import "../styling/task.css";
import Spinner from "../../../components/Spinner";
import { userContext } from "../../../context/userContext";

const Task = ({ prop }) => {
  const showAlert = prop?.showAlert;
  const navigate = useNavigate();
  const {
    documentGroups,
    uploadStatuses,
    uploadSummary,
    uploadDocumentGroup,
    caseId,
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
  }, []);

  const allUploadsCompleted = useMemo(() => {
    if (!documentGroups || documentGroups.length === 0) {
      return false;
    }
    return documentGroups.every(
      (group) => uploadStatuses[group.key]?.status === "completed"
    );
  }, [documentGroups, uploadStatuses]);

  const anyUploadInFlight = useMemo(() => {
    if (!documentGroups || documentGroups.length === 0) {
      return false;
    }
    return documentGroups.some(
      (group) => uploadStatuses[group.key]?.status === "uploading"
    );
  }, [documentGroups, uploadStatuses]);

  const handleFileChange = async (group, event) => {
    const files = Array.from(event.target.files || []);
    if (files.length === 0) {
      return;
    }

    try {
      await uploadDocumentGroup(group.key, files);
    } catch (error) {
      console.error(`Upload failed for ${group.key}`, error);
    }
  };

  const handleProcessDocuments = () => {
    if (!allUploadsCompleted) {
      if (typeof showAlert === "function") {
        showAlert(
          "Please upload each document before navigating to outcomes.",
          "warning"
        );
      }
      return;
    }

    navigate("/outcomes", {
      state: { caseId: uploadSummary.caseId || caseId },
    });
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
          {documentGroups?.map((item) => {
            const uploadState = uploadStatuses[item.key] || {};
            const formats = item.accept
              .split(",")
              .map((format) => format.replace(".", "").toUpperCase())
              .join(" · ");
            const isUploading = uploadState.status === "uploading";
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
                    <i className="fa-solid fa-cloud-arrow-up mb-3"></i>
                    <p className="mb-1 fw-semibold text-dark">
                      Drag &amp; drop or{" "}
                      <span className="text-warning">browse</span>
                    </p>
                    <small className="text-dark-50">
                      {formats} · up to 25MB each
                    </small>
                  </label>
                  <div className="mt-2">
                    {isUploading && (
                      <small className="text-info fw-semibold">
                        Uploading…
                      </small>
                    )}
                    {isCompleted && !hasError && (
                      <small className="text-success fw-semibold">
                        Uploaded
                      </small>
                    )}
                    {hasError && (
                      <small className="text-danger fw-semibold">
                        Failed to upload. Try again.
                      </small>
                    )}
                  </div>
                  <div className="selected-file-list mt-3">
                    {hasFiles && (
                      <ul className="list-unstyled mb-0">
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
              !allUploadsCompleted ? "secondary" : "primary"
            } btn-lg px-4 py-2 fw-semibold shadow`}
            onClick={handleProcessDocuments}
            disabled={!allUploadsCompleted}
            data-bs-toggle="tooltip"
            data-bs-placement="top"
            title="Click to view outcomes once all documents are uploaded"
          >
            Process Documents
            {anyUploadInFlight && <Spinner />}
          </button>
        </div>
      </div>
    </section>
  );
};

export default Task;
