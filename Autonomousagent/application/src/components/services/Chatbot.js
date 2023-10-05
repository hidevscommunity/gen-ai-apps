import React, { useState } from "react";
import styled from "styled-components";

const ChatbotContainer = styled.div`
  background: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  @media screen and (min-width: 480px) {
    width: 90%; /* Adjust width for small screens */
}

@media screen and (min-width: 768px) {
    width: 80%; /* Adjust width for medium screens */
    margin: 0 auto; /* Center the card horizontally */
}

@media screen and (min-width: 1000px) {
    width: 900px; /* Set a fixed width for larger screens */
}

@media screen and (min-width: 1000px) {
    width: 900px; /* Set a fixed width for larger screens */
}

`;

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Welcome to the chatbot!" },
  ]);
  const [inputText, setInputText] = useState("");

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSendMessage = () => {
    if (inputText.trim() !== "") {
      setMessages([...messages, { text: inputText, user: "user" }]);
      setInputText("");
      // Implement chatbot response logic here
    }
  };

  return (
    <ChatbotContainer>
      <div>
        {messages.map((message, index) => (
          <Message key={index} user={message.user}>
            {message.text}
          </Message>
        ))}
      </div>
      <MessageInputContainer>
        <MessageInput
          type="text"
          placeholder="Type your message..."
          value={inputText}
          onChange={handleInputChange}
        />
        <SendMessageButton onClick={handleSendMessage}>Send</SendMessageButton>
      </MessageInputContainer>
    </ChatbotContainer>
  );
};

const Message = styled.div`
  background-color: ${({ user }) => (user ? "#ffffff" : "#d3e8ff")};
  padding: 8px 12px;
  border-radius: ${({ user }) =>
    user ? "10px 10px 10px 0" : "10px 10px 0 10px"};
  margin: 4px 0;
  align-self: ${({ user }) => (user ? "flex-end" : "flex-start")};
`;

const MessageInputContainer = styled.div`
  display: flex;
  flex-direction: column; /* Change to column layout */
  align-items: center; /* Center align horizontally */
  margin-top: 10px;
`;

const MessageInput = styled.input`
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px 0 0 5px;
`;

const SendMessageButton = styled.button`
  border: none;
  background-color: #007bff;
  color: white;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px; /* Add margin for spacing */
`;

export default Chatbot;
