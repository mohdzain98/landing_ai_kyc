import React from "react";
import { Link as ScrollLink } from "react-scroll";
import "../styling/intro.css";
import TypingEffect from "./TypingEffect";

const Main = () => {
  return (
    <div className="main-page py-5">
      <div className="content-container container" id="con">
        <div className="row align-items-center g-5">
          <div className="col-12 col-md-8">
            <h2 className="animated-text fw-bold mb-4 fs-1">
              Loanlens <span className="name-highlight">AI</span>
            </h2>
            <TypingEffect
              className="role-text mb-3"
              speed={40}
              textSegments={[
                { text: "Your AI " },
                { text: "Powered", className: "ade-highlight" },
                {
                  text: " Document Intelligence Hub",
                },
              ]}
            />
            <div className="description-text">
              <ul className="mb-0 ps-3">
                <li>
                  Auto-check income proofs, bank statements, and identity docs
                  with ADE precision.
                </li>
                <li>
                  Gemini-powered narratives explain risk signals and policy
                  exceptions instantly.
                </li>
                {/* <li>
                  Unified borrower profiles keep compliance teams, analysts, and
                  advisors aligned.
                </li> */}
              </ul>
            </div>
            <div>
              <ScrollLink
                className="mt-4 get-started-btn"
                to="task"
                smooth={true}
                duration={50}
              >
                Get Started
              </ScrollLink>
            </div>
          </div>
          <div className="col-12 col-md-4">
            <div className="partner-stack">
              <div className="partner-card shadow-lg">
                <img
                  src={
                    new URL("../../../assets/landingai.png", import.meta.url)
                      .href
                  }
                  alt="Landing AI symbol"
                  className="partner-icon"
                />
                <div>
                  <span className="badge bg-warning text-dark text-uppercase mb-2">
                    Landing AI
                  </span>
                  <p className="mb-0 small">
                    Flight-tested ADE pipelines powering automated document
                    intelligence.
                  </p>
                </div>
              </div>
              <div className="partner-card shadow-lg">
                <img
                  src={
                    new URL("../../../assets/awsbg.png", import.meta.url).href
                  }
                  alt="Gemini icon"
                  className="partner-icon"
                />
                <div>
                  <span className="badge bg-info text-dark text-uppercase mb-2">
                    Bedrock
                  </span>
                  <p className="mb-0 small">
                    Narrative copilots powered by AWS Bedrock that contextualize
                    each borrower in plain language.
                  </p>
                </div>
              </div>
              <div className="partner-card shadow-lg">
                <img
                  src="https://img.icons8.com/color/96/bank-cards.png"
                  alt="Financial insights icon"
                  className="partner-icon"
                />
                <div>
                  <span className="badge bg-light text-dark text-uppercase mb-2">
                    Credit Insights
                  </span>
                  <p className="mb-0 small">
                    Aggregated bureau feeds and cash-flow scoring in one secure
                    dashboard.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Main;
