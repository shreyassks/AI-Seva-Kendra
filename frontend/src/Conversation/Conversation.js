import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { ReactMic } from "react-mic";
import "./Conversation.css";
import config from "../config";

function Conversation() {
  const user_name = sessionStorage.getItem("user_name");
  const [recording, setRecording] = useState(false);
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [conversations, setConversations] = useState([
    {
      message: `हैलो ${user_name}, मैं आपकी कैसे मदद कर सकता हूं?`,
      sender: "ai",
    },
  ]);

  const chatboxContainerRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (chatboxContainerRef.current) {
      chatboxContainerRef.current.scrollTop =
        chatboxContainerRef.current.scrollHeight;
    }
  }, [conversations]);

  // Callback function for receiving audio data
  const onStop = (recordedData) => {
    const audioData = recordedData.blob;
    // console.log("The audioData is", audioData);

    const fetchAudio = async () => {
      const formData = new FormData();
      formData.append("audio", audioData, "recording.webm");
      const response = await fetch(
        config.backendUrl + "/conversation/submit-audio",
        {
          method: "POST",
          body: formData,
        }
      );

      const audioBlob = await response.blob();
      const responseAI = response.headers.get("X-Response-Answer-ai");
      const responseYou = response.headers.get("X-Response-Answer-you");

      setConversations((prevConversations) => {
        const updatedConversations = [
          ...prevConversations,
          {
            message: responseYou,
            sender: "you",
          },
          {
            message: responseAI,
            sender: "ai",
          },
        ];

        return updatedConversations;
      });

      const audioElement = new Audio();
      audioElement.src = URL.createObjectURL(audioBlob);
      audioElement.addEventListener("ended", () => {
        setListening(false);
      });

      setLoading(false);
      setListening(true);
      audioElement.play();

      // with the audioblob, set it as objecturl to an audio element and play
    };

    setLoading(true);
    fetchAudio();
  };

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
      <div className="conversation-content">
        <div className="conversation-flex">
          <div className="conversation-container">
            <div className="audio-visualizers">
              <div
                className="person-div"
                onClick={() => {
                  setRecording(!recording);
                }}
              >
                <div className="icon-name">{user_name.charAt(0)}</div>
                <div className="hidden">
                  <ReactMic
                    record={recording}
                    onStop={onStop}
                    visualSetting="frequencyBars"
                    echoCancellation={true}
                    autoGainControl={true}
                    noiseSuppression={true}
                    channelCount={1} // mono
                  />
                </div>
                <div className="visualizer">
                  {recording ? (
                    <div className="icon">
                      <span />
                      <span />
                      <span />
                    </div>
                  ) : null}
                </div>
              </div>

              <div className="person-div">
                <div className="icon-name">
                  {/* R */}
                  <img
                    src={"/ai-bot-traced.png"}
                    alt="R"
                    className="ai-bot-png"
                  ></img>
                </div>
                <div className="visualizer">
                  {listening ? (
                    <div className="icon">
                      <span />
                      <span />
                      <span />
                    </div>
                  ) : null}
                </div>
              </div>
            </div>
            {loading ? (
              <div className="spinner loading">
                <div className="rect1"></div>
                <div className="rect2"></div>
                <div className="rect3"></div>
                <div className="rect4"></div>
                <div className="rect5"></div>
              </div>
            ) : null}

            <div className="chatbox" ref={chatboxContainerRef}>
              <div className="actually-chatbox">
                {conversations.map((conversation, index) => (
                  <div
                    className={
                      conversation.sender === "ai" ? "ai-chat" : "you-chat"
                    }
                    key={index}
                  >
                    <div className="conversation-box">
                      {conversation.message}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="end-conversation-container">
        <p
          onClick={() => {
            navigate("/dashboard");
          }}
          className="end-conversation"
        >
          End Conversation
        </p>
      </div>
    </div>
  );
}

export default Conversation;
