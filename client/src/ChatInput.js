import { useEffect, useState, useRef, useMemo } from "react";
import { SendIcon } from "./icons";

// Component to handle the input field
export function ChatInput({
  onSubmit,
  promptInput,
  setPromptInput,
}) {
  const onPromptInputChange = (e) => {
    if (e.key === "Enter") {
      onSubmit(promptInput);
    } else {
      setPromptInput(e.target.value);
    }
  };

  const onSubmitPrompt = (e) => {
    onSubmit(promptInput);
  };

  return (
    <div className="flex flex-row p-2 rounded-full border">
      <input
        className="grow focus:outline-none mx-2"
        value={promptInput}
        onChange={onPromptInputChange}
        onKeyUp={onPromptInputChange}
      />
      <a
        className="cursor-pointer"
        onClick={onSubmitPrompt}
      >
        <SendIcon className="size-6" />
      </a>
    </div>
  );
}
