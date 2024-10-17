import React from "react";
import { Link } from "react-router-dom";
import "./Landingpage.css"; // Import the CSS file

function LandingPage() {
  return (
    <div className="landing-container">
      <div className="left-content">
        <h1 className="heading">Intelligent PDF Querying System (IPQS)</h1>
        <h2>Welcome to IPQS: Your Smart PDF Interaction Tool</h2>
        <p>
          IPQS enables seamless querying and analysis of PDF documents, providing you with
          intelligent insights at your fingertips. Our system efficiently processes uploaded PDFs
          to extract valuable information and generate relevant questions for enhanced understanding.
        </p>
        <p>
          Whether you are a researcher, student, or professional, IPQS empowers you to validate 
          information, explore document content, and interact with your PDFs like never before. 
        </p>
        <ul>
          <li className="btn-1">
            <Link to="/upload" className="button">
              Upload PDF
            </Link>
          </li>
        </ul>
      </div>
      
    </div>
  );
}

export default LandingPage;