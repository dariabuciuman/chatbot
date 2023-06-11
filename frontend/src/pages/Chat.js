import React, { useState } from "react";
import "./Chat.css";
import { TextareaAutosize } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import BouncyLoader from "../components/loader/BouncyLoader";
import MessageComponent from "../components/message/MessageComponent";
import FlagIcon from "@mui/icons-material/Flag";
import Tooltip from "@mui/material/Tooltip";

export default function Chat() {
  const [message, setMessage] = useState();
  const [response, setResponse] = useState();
  const [loading, setLoading] = useState(false);
  const [chat, setChat] = useState([]);

  const onEnterMessage = (e) => {
    e.preventDefault();
    setMessage(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = async () => {
    const messageToServer = message;
    setChat((current) => [...current, { message: messageToServer, isSender: true }]);
    setMessage("");
    console.log("Sending message to API");
    setLoading(true);
    const response = await fetch("http://localhost:5000/api/chatbot/response", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: messageToServer }),
    });

    const content = await response.json();
    setLoading(false);
    setResponse(content.response);
    setChat((current) => [...current, { message: content.response, isSender: false }]);
  };

  const reportProblem = async () => {
    const request = await fetch("http://localhost:5000/api/chatbot/report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ chat: chat }),
    });
    if (request.status === 200) {
      alert("Am recepționat raportul tău de eroare. Ne cerem scuze pentru această problemă, incercăm să remediem problema cât de curând!");
    } else {
      alert("A intervenit o problema");
    }
  };

  return (
    <div className="general">
      {/* <div className="left-panel">
        <PersistentDrawerLeft />
      </div>
      <div className="left-panel-mobile">
        <h1>LegiBot</h1>
      </div> */}
      <div className="main-panel">
        <div className="response-area">
          {!loading && chat.length > 0 && (
            <Tooltip title="Raportează o problemă">
              <FlagIcon className="report" onClick={reportProblem} />
            </Tooltip>
          )}
          {loading && <BouncyLoader />}
          {chat
            .slice(0)
            .reverse()
            .map((chat) => {
              return <MessageComponent key={Math.random()} message={chat.message} isSender={chat.isSender} />;
            })}
        </div>
        <div className="input-area">
          <TextareaAutosize className="textarea" maxRows={4} minRows={2} onChange={onEnterMessage} onKeyDown={handleKeyDown} value={message} />
          <SendIcon className="sendIcon" onClick={sendMessage} />
        </div>

        <footer className="footer">
          Atenție: Acest chatbot se află într-un stadiu de dezvoltare prematură. Cunoștințele sale sunt limitate și ar putea oferi răspunsuri greșite sau
          incorecte. Dacă observați răspunsuri greșite sau probleme legate de funcționalitatea sa, vă rugăm să ne trimiteți un raport apăsând pictograma cu
          steagul.{" "}
        </footer>
      </div>
    </div>
  );
}
