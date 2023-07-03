import React from "react";
import "./MessageComponent.css";
import SmartToyIcon from "@mui/icons-material/SmartToy";

function MessageComponent({ message, isSender }) {
  return (
    <div className={`message-box ${isSender ? "sender" : "reciever"}`}>
      {!isSender && <SmartToyIcon sx={{ paddingRight: "8px" }} />}
      <p>{message}</p>
    </div>
  );
}

export default MessageComponent;
