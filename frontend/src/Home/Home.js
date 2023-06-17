import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import config from "../config";
import "./Home.css";

function Home() {
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [pincode, setPincode] = useState("");

  const navigate = useNavigate();

  const signIn = () => {
    fetch(config.backendUrl + "/signin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
      },
      body: JSON.stringify({
        user_name: name,
        user_address: address,
        user_pincode: pincode,
      }),
    })
      .then((res) => {
        if (res.ok) {
          sessionStorage.setItem("user_name", name);
          navigate("/dashboard");
        } else {
          console.log("something went wrong", res);
        }
      })
      .catch((e) => {
        console.log(e);
      });
  };

  return (
    <div className="home-page">
      <div className="banner">
        <div className="banner-overlay"></div>
        <div className="banner-content">
          <img src={"/ai-seva.png"} alt="Logo" className="logo"></img>
          <br></br>
          <br></br>
          <br></br>
          <br></br>
          <p className="banner-p">For all your bureaucratic queries</p>
          <p className="banner-p">आपकी सभी प्रशासनिक जरूरतों के लिए</p>
        </div>
      </div>
      <div className="form">
        {/* <p className="form-heading">About yourself</p> */}
        <div className="form-content">
          <p className="form-label">Name</p>
          <input
            className="form-input"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          ></input>
          <p className="form-label">Address (Locality, City)</p>
          <input
            className="form-input"
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          ></input>
          <p className="form-label">Pin code</p>
          <input
            className="form-input"
            type="text"
            value={pincode}
            onChange={(e) => setPincode(e.target.value)}
          ></input>
          <button className="form-button" onClick={signIn}>
            SIGN IN
          </button>
        </div>
      </div>
    </div>
  );
}

export default Home;
