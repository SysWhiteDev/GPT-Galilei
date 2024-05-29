import { AiOutlineOpenAI } from "react-icons/ai";
import Image from "next/image";
type ChatBubbleProps = {
  children: React.ReactNode;
  side: string;
  loading?: boolean;
};
import "./ChatBubble.css";
export default function ChatBubble({ children, side, loading }: ChatBubbleProps) {
  return (
    <>
      <div
        className={`${
          side === "right" ? " flex-row-reverse" : ""
        } flex items-start gap-2.5`}
      >
        <div className="p-1.5 translate-y-[5px] border-border border rounded-full">
          {side === "right" ? (
            <Image
              src={"/assets/galilei.png"}
              height={24}
              width={24}
              alt="Galilei logo"
            />
          ) : (
            <AiOutlineOpenAI size={24} />
          )}
        </div>
        <div
          className={`${
            side === "right" ? "bg-opacity-5" : "bg-opacity-15"
          } flex border-border flex-col min-w-[30%] bg-accent whitespace-normal shadow-md backdrop-blur-md py-2 px-4 max-w-[60%] rounded-xl z-20 my-1`}
        >
          <span className={` font-semibold whitespace-normal text-sm`}>
            {side === "right" ? "You" : "GPT + Galilei"}
          </span>
          <span className="w-full whitespace-break-spaces truncate">
            {loading ? "..." : children}
          </span>
        </div>
      </div>
    </>
  );
}
