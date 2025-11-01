import React, { useContext, useMemo } from "react";
import { Link, useLocation } from "react-router-dom";
import Spinner from "../components/Spinner";
import { userContext } from "../context/userContext";

const STATUS_CONFIG = {
  idle: {
    label: "Waiting",
    badge: "secondary",
    description: "We are preparing this document for processing.",
  },
  uploading: {
    label: "Processing",
    badge: "info",
    description: "Hold tight while we finalize this document.",
  },
  completed: {
    label: "Completed",
    badge: "success",
    description: "Document processed successfully.",
  },
  error: {
    label: "Failed",
    badge: "danger",
    description: "Processing failed. Return to uploads to try again.",
  },
};

const Outcomes = () => {
  const location = useLocation();
  const { documentGroups, uploadStatuses, uploadSummary } =
    useContext(userContext);

  const caseId = location?.state?.caseId || uploadSummary?.caseId;

  const cards = useMemo(() => {
    if (!Array.isArray(documentGroups)) {
      return [];
    }
    return documentGroups.map((group) => {
      const state = uploadStatuses?.[group.key] || {};
      const statusKey = state.status || "idle";
      const status = STATUS_CONFIG[statusKey] || STATUS_CONFIG.idle;

      return {
        key: group.key,
        title: group.title,
        statusKey,
        status,
        response: state.response,
        error: state.error,
      };
    });
  }, [documentGroups, uploadStatuses]);

  return (
    <div className="container py-5">
      <div className="d-flex flex-column flex-lg-row align-items-lg-end justify-content-between gap-3 mb-4">
        <div>
          <h1 className="h3 fw-bold mb-1">Document Outcomes</h1>
          <p className="text-muted mb-0">
            Track each document as it moves from upload to completion.
          </p>
        </div>
        <div className="text-lg-end">
          {caseId && (
            <>
              <span className="d-block text-uppercase text-muted small">
                Case ID
              </span>
              <span className="fw-semibold text-break">{caseId}</span>
            </>
          )}
          <span className="d-block text-muted small mt-2">
            {uploadSummary?.completed ?? 0}/{uploadSummary?.total ?? 0} complete
          </span>
        </div>
      </div>

      <div className="row g-3">
        {cards.map((card) => (
          <div key={card.key} className="col-12 col-sm-6 col-lg-4">
            <div className="border rounded-3 p-3 h-100 shadow-sm">
              <div className="d-flex align-items-start justify-content-between mb-2">
                <h2 className="h6 fw-semibold mb-0">{card.title}</h2>
                <span className={`badge bg-${card.status.badge}`}>
                  {card.status.label}
                </span>
              </div>

              <p className="text-muted small mb-3">{card.status.description}</p>

              {card.statusKey !== "completed" && card.statusKey !== "error" && (
                <div className="d-flex justify-content-center py-3">
                  <Spinner color="primary" size="sm" />
                </div>
              )}

              {card.statusKey === "completed" && card.response && (
                <div className="bg-light border rounded-3 p-2">
                  <p className="small fw-semibold mb-1 text-success">
                    Result payload
                  </p>
                  <pre className="small mb-0 text-break">
                    {JSON.stringify(card.response, null, 2)}
                  </pre>
                </div>
              )}

              {card.statusKey === "completed" && !card.response && (
                <p className="small text-success mb-0">
                  No response data returned, but processing finished
                  successfully.
                </p>
              )}

              {card.statusKey === "error" && (
                <p className="small text-danger mb-0">
                  {card.error || "No additional error details provided."}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="text-center mt-5">
        <Link to="/" className="btn btn-outline-secondary px-4">
          Back to uploads
        </Link>
      </div>
    </div>
  );
};

export default Outcomes;
