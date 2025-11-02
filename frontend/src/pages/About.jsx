import React from "react";

const About = ({ prop }) => {
  const showAlert = prop?.showAlert;

  const handleConnectClick = () => {
    if (typeof showAlert === "function") {
      showAlert("Thanks for reaching out! We'll get back soon.", "success");
    }
  };

  const pipelineSteps = [
    {
      title: "Upload",
      description: "Borrower files arrive via drag-and-drop or secure API.",
      icon: "fa-cloud-arrow-up",
    },
    {
      title: "Classify",
      description: "ADE detects the document type automatically.",
      icon: "fa-layer-group",
    },
    {
      title: "Extract",
      description: "Key fields and values are captured with confidence scores.",
      icon: "fa-robot",
    },
    {
      title: "Validate",
      description: "Rules compare declared data with policy thresholds.",
      icon: "fa-list-check",
    },
    {
      title: "Narrate",
      description: "Analyst-ready summary highlights risk signals and gaps.",
      icon: "fa-comments",
    },
  ];

  const team = [
    {
      name: "Tanika Gupta",
      role: "Director Data Science",
      focus: "",
    },
    {
      name: "Ritesh Kumar",
      role: "Principal Data Scientist",
      focus: "",
    },
    {
      name: "Abhisek Banerjee",
      role: "Senior Lead Data Scientist",
      focus: "",
    },
    {
      name: "Nilanjan Sahu",
      role: "Lead Data Scientist",
      focus: "",
    },
  ];

  const documentTypes = [
    "Identity proofs (IDs, passports, Driving License)",
    "Income proofs & payslips",
    "Bank statements and cash-flow exports",
    "Tax returns",
    "Credit bureau reports & scorecards",
  ];

  return (
    <div className="bg-light">
      <section className="py-5 text-white bg-dark">
        <div className="container py-4">
          <span className="badge bg-warning text-dark text-uppercase mb-3">
            About Landing AI Loan KYC
          </span>
          <h1 className="display-5 fw-bold">
            The document intelligence workspace for smarter lending
          </h1>
          <p className="lead text-white-50 mt-3 col-lg-8 px-0">
            Built for the Financial AI Hackathon Championship 2025, this tool
            accelerates Loan KYC by pairing ADE extraction with guided policy
            checks and easy-to-read summaries.
          </p>
        </div>
      </section>

      <section className="container py-5">
        <div className="row g-4 align-items-center">
          <div className="col-12 col-lg-6">
            <h2 className="fw-bold mb-3">What the platform does</h2>
            <p className="text-muted">
              Loan KYC ingests the common lending document pack, structures the
              data with ADE, and stages it for rapid review. Underwriters get a
              single view that combines extracted values, rule outcomes, and
              narrative insights—so approvals or escalations happen faster.
            </p>
            <ul className="list-unstyled text-muted">
              <li className="mb-2">
                <i className="fa-solid fa-sparkles text-primary me-2"></i>
                ADE-powered parsing captures the fields lending teams track
                most.
              </li>
              <li className="mb-2">
                <i className="fa-solid fa-chart-simple text-primary me-2"></i>
                Configurable policy checks flag gaps, mismatches, or missing
                paperwork instantly.
              </li>
              <li>
                <i className="fa-solid fa-person-chalkboard text-primary me-2"></i>
                Gemini-style narratives explain what changed and what to do
                next.
              </li>
            </ul>
          </div>
          <div className="col-12 col-lg-6">
            <div className="card border-0 shadow-sm">
              <div className="card-body">
                <h5 className="text-uppercase text-muted mb-3">
                  Document types handled
                </h5>
                <div className="row g-3">
                  {documentTypes.map((doc) => (
                    <div className="col-12 col-sm-6" key={doc}>
                      <div className="p-3 bg-light border rounded-3 h-100">
                        <i className="fa-solid fa-file-lines text-primary me-2"></i>
                        {doc}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-5 bg-white border-top border-bottom">
        <div className="container">
          <h2 className="fw-bold text-center mb-4">Pipeline flow</h2>
          <p className="text-muted text-center col-lg-8 mx-auto mb-5">
            Each stage keeps analysts informed and maintains an audit trail.
          </p>
          <div className="p-4 bg-light rounded-4 shadow-sm">
            <div className="row gy-4 gx-0 align-items-center text-center text-md-start">
              {pipelineSteps.map((step, index) => (
                <React.Fragment key={step.title}>
                  <div className="col-12 col-md">
                    <div className="h-100 px-3">
                      <div className="d-inline-flex align-items-center justify-content-center rounded-circle bg-primary-subtle text-primary fs-4 px-3 py-3">
                        <i className={`fa-solid ${step.icon}`}></i>
                      </div>
                      <h6 className="fw-semibold mt-3">{step.title}</h6>
                      <p className="small text-muted mb-0">
                        {step.description}
                      </p>
                    </div>
                  </div>
                  {index !== pipelineSteps.length - 1 && (
                    <div className="col-auto d-none d-md-flex justify-content-center">
                      <i className="fa-solid fa-arrow-right text-secondary"></i>
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="container py-5">
        <div className="text-center mb-5">
          <h2 className="fw-bold">Hackathon team</h2>
          <p className="text-muted mb-0">
            A cross-functional crew building the Landing AI Loan KYC pilot.
          </p>
        </div>
        <div className="row g-4">
          {team.map((member) => (
            <div className="col-12 col-md-6 col-lg-3" key={member.name}>
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body text-center">
                  <div
                    className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center mx-auto mb-3"
                    style={{ width: "56px", height: "56px" }}
                  >
                    <span className="fw-bold">{member.name.charAt(0)}</span>
                  </div>
                  <h5 className="mb-1">{member.name}</h5>
                  <small className="text-primary fw-semibold d-block mb-2">
                    {member.role}
                  </small>
                  <p className="text-muted mb-0">{member.focus}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default About;
