import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const [name, setName] = useState("user");

  const navigate = useNavigate();

  const startInterview = () => {
    navigate("/conversation");
  };

  useEffect(() => {
    setName(sessionStorage.getItem("user_name"));
  }, []);

  return (
    <div>
      <div className="dashboard-header">
        <img
          src={"/ai-seva.png"}
          alt="Logo"
          className="dashboard-header-logo"
        ></img>

        <img
          src={"/logout.png"}
          alt="Logo"
          className="dashboard-header-logout"
        ></img>
      </div>
      <div className="dashboard-content">
        <h2 className="dashboard-heading">Welcome {name}</h2>
        <p className="dashboard-p">
          I'm <b>Ravi</b>, your AI assistant to help you guide with any
          questions you have related to any Indian policies, services, or laws
        </p>
        <br></br>
        <button className="dashboard-button" onClick={startInterview}>
          ASK ME ANYTHING
        </button>
      </div>

      <br></br>
      <br></br>
      <div className="dashboard-pi-content">
        <h3 className="dashboard-pi-heading">Your Past Conversations</h3>
        <div className="pi-div">
          <p className="title">
            <b>पासपोर्ट सत्यापन केंद्र</b>
          </p>
          <p className="time">11 June 2023</p>
          <button className="dashboard-button">CONTINUE</button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
