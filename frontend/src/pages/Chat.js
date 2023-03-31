import React from "react";
import "./Chat.css";
import { TextField } from "@mui/material";

export default function Chat() {
  return (
    <div className="general">
      <div className="left-panel">LogiBot</div>
      <div className="main-panel">
        <div className="response-area">Here is the response</div>
        <div className="input-area">
          {/* <TextField sx={{ borderStyle: "none", color: "red" }} fullWidth id="filled-multiline-flexible" multiline maxRows={5} variant="filled" /> */}
          <textarea className="textarea"></textarea>
        </div>
      </div>
    </div>
  );
}
