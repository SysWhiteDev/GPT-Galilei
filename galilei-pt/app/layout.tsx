import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AiOutlineOpenAI } from "react-icons/ai";
import Link from "next/link";
import { Suspense } from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "GPT + Galilei",
  description: "Made by the school IISS Galileo Galilei",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Suspense>
          <main className="flex  text-text h-dvh overflow-hidden">
            <div className="transition-all w-[300px]  flex-shrink-0 flex flex-col items-left text-lg px-5 p-4 bg-secondary bg-opacity-5 border-r-border border-r">
              <div className="mx-auto w-full ">
                <h1 className="font-semibold flex gap-1.5 justify-between  items-center">
                  <AiOutlineOpenAI size={30} />
                  <span>GPT + Galilei</span>
                </h1>
              </div>
              <span className="text-sm font-bold mt-8">Today</span>
              <Link
                href={"/"}
                className="w-full mt-2 text-sm bg-secondary bg-opacity-20 px-3 py-2.5 rounded-lg"
              >
                <p>App showcase</p>
              </Link>

              <span className="text-sm mt-8 font-bold">
                Found hallucinations
              </span>
              <Link
                href={"/"}
                className="w-full mt-2 text-sm hover:bg-secondary hover:bg-opacity-10 px-3 py-2.5 rounded-lg"
              >
                <p>Allucinazione nr.1</p>
              </Link>
              <Link
                href={"/"}
                className="w-full mt-2 text-sm hover:bg-secondary hover:bg-opacity-10 px-3 py-2.5 rounded-lg"
              >
                <p>Allucinazione nr.2</p>
              </Link>
              <Link
                href={"/"}
                className="w-full mt-2 text-sm hover:bg-secondary hover:bg-opacity-10 px-3 py-2.5 rounded-lg"
              >
                <p>Allucinazione nr.3</p>
              </Link>
            </div>
            <div className="w-full">{children}</div>
          </main>
        </Suspense>
      </body>
    </html>
  );
}
