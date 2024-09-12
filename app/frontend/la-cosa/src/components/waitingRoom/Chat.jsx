import React, { useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([]);

  const [newMessage, setNewMessage] = useState("");

  const handleInputChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (newMessage.trim() === "") return;

    // Simulate sending the message (you would send this via WebSocket)
    setMessages((prevMessages) => [
      ...prevMessages,
      { text: newMessage, sender: "User" },
    ]);
    setNewMessage("");
  };

  return (
    <div>
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${
              message.sender === "User" ? "user" : "other"
            }`}
          >
            <span className="message-sender">{message.sender}:</span>{" "}
            {message.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="chat-form">
        <input
          type="text"
          placeholder="Ingresar mensaje..."
          value={newMessage}
          onChange={handleInputChange}
        />
        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}

export default Chat;
