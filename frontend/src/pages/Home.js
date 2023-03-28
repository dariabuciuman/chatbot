import React from "react";
import "./Home.css";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();
  return (
    <div className="home">
      <div className="dark-overlay">
        <div className="greeting">
          <div className="greeting-text">
            <h1>Salut!</h1>
            <h1>Vrei să discuți cu domnul consilier chatbot?</h1>
          </div>
          <div
            className="imageButton"
            onClick={() => {
              navigate("/chat");
            }}
          >
            <img src="https://cdn-icons-png.flaticon.com/512/5111/5111412.png"></img>
          </div>
        </div>
      </div>
    </div>
  );
}
