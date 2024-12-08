import { useEffect, useState, useRef, useMemo } from "react";
import { clsx } from "clsx";
import Markdown from "react-markdown";
import { Comment, Oval } from "react-loader-spinner";

// Component to handle the chat response from the server
export function ChatOutput({
  stream,
  isStreaming,
  messages,
}) {
  // Scroll to the bottom of the chat panel
  const outputScrollTarget = useRef(null);
  const outputScrollBottom = () => {
    if (outputScrollTarget.current) {
      const scrollHeight = outputScrollTarget.current.scrollHeight;
      const clientHeight = outputScrollTarget.current.clientHeight;
      const maxScrollTop = scrollHeight - clientHeight;
      outputScrollTarget.current.scrollTop = Math.max(0, maxScrollTop);
    }
  };

  // When the chat output changes, scroll to the bottom
  useEffect(() => {
    outputScrollBottom();
  }, [stream, messages]);

  // Memoize the messages in case it gets long
  const renderedMessages = useMemo(() =>
    messages.map((msg, idx) => (
      (msg.role === "assistant" || msg.role === "user") && (
        <div key={idx} className="flex flex-col w-full">
          <div className={clsx("max-w-[90%] prose p-2", {
            //"bg-slate-200": msg.role === "assistant",
            "self-end bg-slate-400 rounded-lg": msg.role === "user",
          })}>
            <Markdown
              children={msg.content}
            />
          </div>
        </div>
      )
    )
  ), [messages]);

  return (
  <div className="grow overflow-y-auto" ref={outputScrollTarget}>
    <div>
      {renderedMessages}
      {isStreaming && (
      <div className="max-w-[90%] prose p-2">
        <Markdown
          children={stream}
        />
        <Comment
          backgroundColor="#999999"
          color="#000000"
          height={40}
          width={40}
        />
      </div>
      )}
    </div>
  </div>
  );
}
