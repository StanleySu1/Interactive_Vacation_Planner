import { useEffect, useState, useRef, useMemo } from "react";
import { clsx } from "clsx";

import { Attractions, AttractionDetails } from "./Attractions";
import { sendPrompt } from "./utils";
import { ChatInput } from "./ChatInput";
import { ChatOutput } from "./ChatOutput";
import { PlaneIcon } from "./icons";

export default function App() {
  const [promptInput, setPromptInput] = useState("I'd like to find out more about Paris");
  const [stream, setStream] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [attractions, setAttractions] = useState([]);
  const [currentAttraction, setCurrentAttraction] = useState(null);
  const [messages, setMessages] = useState([
    {
      "role": "system",
      "content": "You are a travel concierge, adept at recommending activities for a visitor. You will enter into a conversation with the traveller.  Start a friendly conversation by introducing yourself. Then ask the following questions to find out where the traveller is going to and what types of activities they're interested in."
    },
    {
      "role": "assistant",
      "content": "How may I assist you?"
    },
  ]);

  // Submitting a user query
  const onSubmitPrompt = (text) => {
    console.log("SUBMIT:", text);
    setIsStreaming(true);
    const newMessages = [...messages];
    newMessages.push({
      "role": "user",
      "content": text,
    });
    setMessages(newMessages);
    setPromptInput("");

    sendPrompt({messages:newMessages}, (m) => {
      // Returning text stream?
      if (m.fullText) {
        setStream(m.fullText);
      // Received array of final messages?
      } else if (m.messages) {
        setMessages(m.messages);
        setStream("");
      // Received array of attractions?
      } else if (m.attractions) {
        const attractions = [];
        // De-dupe by attraction id
        const seenIds = new Set();
        for (const attraction of m.attractions) {
          if (!seenIds.has(attraction.id)) {
            attractions.unshift(attraction);
            seenIds.add(attraction.id);
          }
        }
        setAttractions(attractions);
      }
    }).then(() => {
      // Done with websocket
      setIsStreaming(false);
      setStream("");
    });
  };

  // user clicked on an attraction to view its details
  const showAttraction = (attraction) => {
    setCurrentAttraction(attraction);
  };

  // "tell me more" button
  const onTellMore = (name) => {
    setPromptInput(`Tell me more about ${name}`);
    setCurrentAttraction(null);
  };

  return (
    <main className="flex flex-col gap-2 p-4 max-w-full h-screen overflow-hidden">
      <header className="flex flex-row gap-2">
        <PlaneIcon className="size-6" />
        <span>Vacation Buddy</span>
      </header>
      <div className="grow flex flex-row gap-2 overflow-hidden">
        {attractions && attractions.length > 0 && (
        <div className="grow flex flex-col w-1/4 overflow-y-auto no-bg-slate-100">
          <Attractions
            attractions={attractions}
            showAttraction={showAttraction}
          />
        </div>
        )}
        <div
          className={clsx("flex flex-col min-h-full overflow-hidden gap-2", {
            "w-3/4": attractions.length > 0,
            "grow": !attractions.length,
          })}
        >
          {currentAttraction ? ( // hide attractions if we don't have any
            <AttractionDetails
              attraction={currentAttraction}
              onHide={() => setCurrentAttraction(null)}
              onTellMore={onTellMore}
            />
          ) : (
          <>
            <ChatOutput
              messages={messages}
              stream={stream}
              isStreaming={isStreaming}
            />
            <ChatInput
              promptInput={promptInput}
              setPromptInput={setPromptInput}
              onSubmit={onSubmitPrompt}
            />
          </>
          )}
        </div>
      </div>
    </main>
  );
}
