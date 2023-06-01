import React, { useState } from "react";
import "./Chat.css";
import { TextareaAutosize, IconButton, Drawer } from "@mui/material";
import { MenuIcon } from "@mui/icons-material";
import PersistentDrawerLeft from "../components/PersistentDrawerLeft";
import SendIcon from "@mui/icons-material/Send";

export default function Chat() {
  const [message, setMessage] = useState();

  const onEnterMessage = (e) => {
    setMessage(e.target.value);
  };
  return (
    <div className="general">
      <div className="left-panel">
        <PersistentDrawerLeft />
      </div>
      <div className="left-panel-mobile">
        <h1>LegiBot</h1>
      </div>
      <div className="main-panel">
        <div className="response-area">Here is the response</div>
        <div className="input-area">
          <TextareaAutosize className="textarea" maxRows={4} minRows={1} onChange={onEnterMessage} />
          <SendIcon />
        </div>
      </div>
    </div>
  );
}
