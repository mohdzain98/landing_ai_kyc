import React, { useContext, useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
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

const Outcomes = (props) => {
  const { showToast } = props.prop;
  const location = useLocation();
  const navigate = useNavigate();
  const {
    documentGroups,
    uploadStatuses,
    uploadSummary,
    resetUploads,
    changeUploadCount,
  } = useContext(userContext);

  const caseId = location?.state?.caseId || uploadSummary?.caseId;

  const [activeKey, setActiveKey] = useState(
    () => documentGroups?.[0]?.key ?? null
  );
  const [expandedMap, setExpandedMap] = useState({});

  useEffect(() => {
    if (!documentGroups || documentGroups.length === 0) {
      return;
    }
    // Ensure the active key always points to a valid document group.
    const validKeys = documentGroups.map((item) => item.key);
    if (!validKeys.includes(activeKey)) {
      setActiveKey(validKeys[0]);
    }
  }, [documentGroups, activeKey]);

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
        icon: group.icon,
      };
    });
  }, [documentGroups, uploadStatuses]);

  const handleCopy = (content, copy, msg) => {
    if (typeof showToast === "function") {
      showToast(content, copy, msg);
    }
  };

  const activeCard =
    cards.find((card) => card.key === activeKey) || cards[0] || null;

  const isExpanded =
    activeCard && expandedMap.hasOwnProperty(activeCard.key)
      ? expandedMap[activeCard.key]
      : false;

  const toggleExpanded = () => {
    if (!activeCard) {
      return;
    }
    setExpandedMap((prev) => ({
      ...prev,
      [activeCard.key]: !isExpanded,
    }));
  };

  const verdict =
    cards.length > 0 && cards.every((card) => card.statusKey === "completed")
      ? "Yes"
      : "Still Processing";

  const verdictVariant = verdict === "Yes" ? "success" : "danger";
  const verdictIcon =
    verdict === "Yes"
      ? "fa-solid fa-circle-check fa-beat-fade"
      : "fa-solid fa-spinner fa-beat";
  const verdictCopy =
    verdict === "Yes" ? "You are Eligible for the Loan." : "Processing";
  const verdictPanelStyle =
    verdict === "Yes"
      ? { backgroundColor: "rgba(25, 135, 84, 0.07)" }
      : { backgroundColor: "rgba(220, 53, 69, 0.07)" };

  const handleTryOtherDocument = () => {
    changeUploadCount(6);
    navigate("/");
  };

  const handleRestart = () => {
    resetUploads();
    changeUploadCount(0);
    navigate("/");
  };

  return (
    <div className="container py-5">
      <div className="d-flex flex-column flex-lg-row align-items-lg-end justify-content-between gap-3 mb-4">
        <div>
          <h1 className="h3 fw-bold mb-1">Hi, Thanks for visting</h1>
          <p className="text-muted mb-0">
            Our Smart system has analysed the documents and below are detailed
            report against each document.
          </p>
        </div>
        <div className="text-lg-end">
          {caseId && (
            <>
              <span className="d-block text-muted small">
                For any further clarification, please reach out with reference
                id
              </span>
              <span className="text-break" style={{ fontSize: "13px" }}>
                {caseId}
                <span
                  style={{ cursor: "pointer" }}
                  onClick={() => handleCopy(caseId, true, "Case Id")}
                >
                  <i className="fa-regular fa-copy fa-sm ms-1"></i>
                </span>
              </span>
            </>
          )}
          {/* <span className="d-block text-muted small mt-2">
            {uploadSummary?.completed ?? 0}/{uploadSummary?.total ?? 0} complete
          </span> */}
        </div>
      </div>

      <div className="mb-4 d-flex flex-wrap gap-2">
        {cards.map((card) => (
          <button
            key={card.key}
            type="button"
            className={`btn btn-sm ${
              card.key === activeKey ? "btn-primary" : "btn-outline-secondary"
            }`}
            onClick={() => setActiveKey(card.key)}
          >
            {card.icon && <i className={`${card.icon} me-2 `}></i>}
            {card.title}
          </button>
        ))}
      </div>

      <div className="border rounded-3 p-4 shadow-sm">
        {activeCard ? (
          <>
            <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-2 mb-3">
              <div>
                <h2 className="h5 mb-1">{activeCard.title}</h2>
                <p className="text-muted small mb-0">
                  {activeCard.status.description}
                </p>
              </div>
              <span className={`badge bg-${activeCard.status.badge} px-3`}>
                {activeCard.status.label}
              </span>
            </div>

            {activeCard.statusKey !== "completed" &&
              activeCard.statusKey !== "error" && (
                <div className="d-flex justify-content-center py-4">
                  <Spinner color="primary" size="sm" />
                </div>
              )}

            {activeCard.statusKey === "completed" &&
              activeCard.response?.data?.content && (
                <div className="bg-light border rounded-3 p-3 mb-3">
                  <p className="small fw-semibold mb-2 text-success">Result</p>
                  <div
                    className="position-relative"
                    style={
                      !isExpanded
                        ? {
                            maxHeight: "800px",
                            overflow: "hidden",
                          }
                        : undefined
                    }
                  >
                    <div className="result-markdown">
                      <ReactMarkdown>
                        {activeCard.response.data.content}
                      </ReactMarkdown>
                    </div>
                    {!isExpanded &&
                      activeCard.response.data.content.length > 400 && (
                        <div
                          className="position-absolute bottom-0 start-0 end-0"
                          style={{
                            height: "72px",
                            background:
                              "linear-gradient(180deg, rgba(248,249,250,0) 0%, rgba(248,249,250,1) 85%)",
                          }}
                        ></div>
                      )}
                  </div>
                  {activeCard.response.data.content.length > 400 && (
                    <button
                      type="button"
                      className="btn btn-link p-0 mt-2"
                      onClick={toggleExpanded}
                    >
                      {isExpanded ? "Show less" : "Show more"}
                    </button>
                  )}
                </div>
              )}

            {activeCard.statusKey === "completed" &&
              activeCard.response &&
              !activeCard.response?.data && (
                <div className="bg-light border rounded-3 p-3 mb-3">
                  <p className="small fw-semibold mb-2 text-success">
                    Result payload
                  </p>
                  <pre className="small mb-0 text-break">
                    {JSON.stringify(activeCard.response, null, 2)}
                  </pre>
                </div>
              )}

            {activeCard.statusKey === "completed" && !activeCard.response && (
              <p className="small text-success mb-3">
                Processing completed successfully. No response payload was
                returned.
              </p>
            )}

            {activeCard.statusKey === "error" && (
              <div className="bg-light border border-danger rounded-3 p-3 mb-3">
                <p className="small text-danger mb-0">
                  {activeCard.error ||
                    "Processing failed. Please try re-uploading this document."}
                </p>
              </div>
            )}
          </>
        ) : (
          <p className="text-muted mb-0">
            No documents available. Return to uploads to begin a new case.
          </p>
        )}
      </div>

      {cards.length > 0 && (
        <section className="mt-4">
          <div
            className={`rounded-4 border border-${verdictVariant} shadow-sm p-4`}
            style={verdictPanelStyle}
          >
            <div className="d-flex flex-column flex-md-row align-items-start align-items-md-center gap-3">
              <div
                className={`rounded-circle bg-${verdictVariant} text-white d-flex align-items-center justify-content-center flex-shrink-0`}
                style={{ width: "56px", height: "56px" }}
              >
                <i className={`${verdictIcon} fa-lg`}></i>
              </div>
              <div>
                <h3 className="h5 fw-bold mb-1">The Final Verdict</h3>
                <p className={`fs-4 fw-semibold text-${verdictVariant} mb-2`}>
                  {verdict}
                </p>
                <p className="mb-0 text-muted">{verdictCopy}</p>
              </div>
            </div>
          </div>
        </section>
      )}

      <div className="d-flex flex-column flex-md-row justify-content-center gap-3 mt-5">
        <button
          type="button"
          className="btn btn-outline-secondary px-4"
          onClick={handleTryOtherDocument}
        >
          <i class="fa-solid fa-rotate me-2"></i>Try with other document
        </button>
        <button
          type="button"
          className="btn btn-outline-danger px-4"
          onClick={handleRestart}
        >
          <i class="fa-solid fa-power-off me-2"></i>Restart
        </button>
      </div>
    </div>
  );
};

export default Outcomes;
