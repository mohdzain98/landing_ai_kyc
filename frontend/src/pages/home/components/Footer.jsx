import React from "react";
import "../styling/intro.css";

const Footer = () => {
  return (
    <footer className="footer-bar text-white py-4">
      <div className="container d-flex flex-column flex-md-row align-items-center justify-content-between gap-3">
        <div>
          <h6 className="mb-1 text-uppercase">Landing AI Loan KYC</h6>
          <small className="text-white-50">
            Financial AI Hackathon Championship 2025
          </small>
        </div>
        <div className="text-white-50 small">
          © {new Date().getFullYear()} Landing AI. Crafted for smarter lending.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
