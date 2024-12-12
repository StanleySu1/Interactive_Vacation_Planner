import { useEffect, useState, useRef, useMemo } from "react";
import { clsx } from "clsx";

import { Attractions, AttractionDetails } from "./Attractions";
import { sendPrompt } from "./utils";
import { ChatInput } from "./ChatInput";
import { ChatOutput } from "./ChatOutput";
import { PlaneIcon } from "./icons";

export default function App() {
  const [promptInput, setPromptInput] = useState("Plan trip to Paris focus on art and food");
  const [searchParams, setSearchParams] = useState(null);
  const [stream, setStream] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [attractions, setAttractions] = useState([]);
  const [currentAttraction, setCurrentAttraction] = useState(null);
  const [messages, setMessages] = useState([
    {
      "role": "system",
      "content": "Your goal is to create a complete itinerary for their trip. When the traveler specifies a city and their interests, generate a detailed day-by-day itinerary including attraction names, descriptions, and estimated time for each activity. Ensure the itinerary is logical, well-paced, and includes recommendations for meals or rest breaks. You only know have information on the following cities:Amsterdam, Barcelona, Dubai, Lisbon, Lonndon, Marrakech, New York City, Paris, Rome, Las Vegas"
    },
    {
      "role": "assistant",
      "content": "Where would you like to go and what are you interested in doing?"
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
    setSearchParams(null);

    sendPrompt({messages:newMessages}, (m) => {
      // Returning text stream?
      if (m.fullText) {
        setStream(m.fullText);
      // Received search parameters?
      } else if (m.search) {
        setSearchParams(m.search);
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
            attractions.push(attraction);
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
        <div className="grow flex flex-row gap-2">
          <PlaneIcon className="size-6" />
          <span>Vacation Buddy</span>
        </div>
        {searchParams && (
          <div className="flex flex-row gap-4 text-sm">
            <div>
              <strong>City:</strong>
              {searchParams.city}
            </div>
            <div>
              <strong>Interests:</strong>
              {searchParams.interests.join(", ")}
            </div>
          </div>
        )}
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
