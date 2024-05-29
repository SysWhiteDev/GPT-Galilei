/* eslint-disable react-hooks/exhaustive-deps */
"use client";
import ChatBubble from "@/components/ChatBubble";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { FaArrowUp } from "react-icons/fa6";
import { LuFileStack } from "react-icons/lu";
import { Switch } from "@/components/ui/switch";
import { useSearchParams } from "next/navigation";

type ChatLogType = {
  side: string;
  text: string;
  loading: boolean;
};

export default function Home() {
  const chatBottom = useRef<any>();
  const [chatInput, setChatInput] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [context, setContext] = useState<{
    text: string;
    google: boolean;
    urls: Array<string>;
  }>({
    text: "",
    google: false,
    urls: [],
  });
  const [isContextDialogOpen, setIsContextDialogOpen] =
    useState<boolean>(false);
  const [chatLog, setChatLog] = useState<Array<ChatLogType>>([]);

  const sendMessage = async () => {
    if (chatInput === "" || loading) return;

    await setChatLog((prevChatLog) => [
      ...prevChatLog,
      { side: "right", text: chatInput, loading: false },
    ]);
    chatBottom.current.scrollIntoView({ behavior: "smooth" });
    setLoading(true);

    setTimeout(() => {
      setChatLog((prevChatLog) => [
        ...prevChatLog,
        {
          side: "left",
          text: chatInput,
          loading: true,
        },
      ]);
      chatBottom.current.scrollIntoView({ behavior: "smooth" });
      requestResponse(chatInput).then(async (response) => {
        setChatInput("");
        setChatLog((prevChatLog) => [
          ...prevChatLog.slice(0, prevChatLog.length - 1),
          {
            ...prevChatLog[prevChatLog.length - 1],
            text: response?.text || "OpenAI refused to repond",
            loading: false,
          },
        ]);
        chatBottom.current.scrollIntoView({ behavior: "smooth" });
        setLoading(false);
      });
    }, 800);
  };

  const requestResponse = async (text: string) => {
    const baseUrl = `http://localhost:8000/?question=${text}&text=${context.text}&google=${context.google}`;
    let url = new URL(baseUrl);

    if (context.urls.length > 0) {
      url.searchParams.append("urls", JSON.stringify(context.urls));
    }

    const response = await fetch(url.toString(), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    return await response.json();
  };

  const handleKeyDown = (e: any) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  // load history
  const query = useSearchParams();
  const history = query.get("history");

  useEffect(() => {
    if (history) {
      const getHistory = async () => {
        const response = await fetch("/histories/" + history + ".json");
        const data = await response.json();
        setChatLog([...chatLog, ...data?.messages]);
      };
      getHistory();
    } else {
      setChatLog([
        {
          side: "left",
          text: "Hello, I am Galilei. I am here to help you with your questions.",
          loading: false,
        },
      ]);
    }
  }, []);

  return (
    <main className="flex  text-text h-dvh overflow-hidden gap-1">
      <div className="flex justify-end h-full w-full items-center flex-col">
        <div className="chat-content relative pb-6 w-full overflow-y-auto z-10">
          <div className="max-w-[calc(48rem+95px)] w-full mx-auto">
            {chatLog.map((m, i) => (
              <ChatBubble side={m.side} loading={m.loading} key={i}>
                {m.text}
              </ChatBubble>
            ))}
            <span ref={chatBottom} />
          </div>
        </div>
        <div
          onKeyDown={(e) => handleKeyDown(e)}
          className="chatbar flex-shrink-0 border-border border shadow z-0 max-w-3xl flex flex-col items-center w-full"
        >
          {isContextDialogOpen && (
            <div className="w-full overflow-hidden flex-col flex px-8 py-4 bg-secondary bg-opacity-5 border-b-border border-b">
              <span className="font-semibold text-lg mb-2">
                Personalizza il modello in base alle tue esigenze
              </span>
              <span className="text-sm mb-1 opacity-80">
                Contesto testuale aggiuntivo
              </span>
              <textarea
                value={context.text}
                onChange={(e) => {
                  setContext({ ...context, text: e.target.value });
                }}
                rows={5}
                className="resize-none p-3 py-2 rounded-md text-md border-border border overflow-hidden flex-1 bg-transparent active:outline-0 focus:outline-none text-text"
                placeholder={"..."}
              />
              <div className="flex items-center justify-between mt-4">
                <span className="text-sm opacity-80">URL</span>
              </div>
              {context?.urls?.map((url: string, i: number) => (
                <div
                  key={i}
                  className="flex h-[36px] items-center gap-1.5 mt-2"
                >
                  <input
                    type="text"
                    value={context.urls[i]}
                    onChange={(e) => {
                      let urls = context.urls;
                      urls[i] = e.target.value;
                      setContext({ ...context, urls });
                    }}
                    placeholder="URL/Link"
                    className="bg-accent flex-1 bg-opacity-5 focus:outline-none px-3 py-2 rounded-md"
                  />
                  <button
                    onClick={() => {
                      let urls = context.urls;
                      urls.splice(i, 1);
                      setContext({ ...context, urls });
                    }}
                    className="text-black bg-red-500 hover:opacity-80 py-2 px-3 text-sm h-full rounded-md"
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                className="bg-white mt-3 py-2 rounded-md text-black font-semibold hover:opacity-90"
                onClick={() => {
                  let urls = context.urls;
                  urls.push("https://");
                  setContext({ ...context, urls });
                }}
              >
                Add new URL
              </button>
              <div className="flex text-sm opacity-80 items-center mt-4 justify-between">
                Enable the model to perform Google searches?
                <Switch
                  checked={context.google}
                  className="data-[state=checked]:!bg-accent data-[state=unchecked]:!bg-border "
                  onCheckedChange={() =>
                    setContext({ ...context, google: !context.google })
                  }
                />
              </div>
            </div>
          )}
          <div className="flex-shrink-0 z-0  px-5 pr-2 py-2   flex items-center h-[56px] w-full">
            <div className="flex  min-w-0 flex-1 flex-col">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => {
                  if (!loading) {
                    setChatInput(e.target.value);
                  }
                }}
                className={`${
                  loading ? "select-none opacity-60" : ""
                } resize-none overflow-hidden flex-1 text-lg bg-transparent active:outline-0 focus:outline-none text-text`}
                placeholder={"Cosa vorresti sapere?"}
              />
            </div>
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => setIsContextDialogOpen(!isContextDialogOpen)}
                className={`${
                  isContextDialogOpen
                    ? "bg-accent bg-opacity-25"
                    : "hover:bg-accent hover:bg-opacity-25"
                } transition-all hover:bg-accent hover:bg-opacity-25 h-[40px] w-[40px] flex items-center justify-center rounded-md`}
              >
                <LuFileStack size={20} />
              </button>
              <button
                onClick={() => sendMessage()}
                className="bg-accent transition-all hover:bg-opacity-35 h-[40px] w-[40px] flex items-center justify-center rounded-full bg-opacity-10"
              >
                <FaArrowUp />
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
