import type { Metadata } from "next";
import { ReactQueryProvider } from "../components/providers/ReactQueryProvider";
import "./globals.css";

export const metadata: Metadata = {
  title: "DocBrain AI • Intelligent PDF Knowledge Assistant",
  description: "Production-ready AI Assistant for PDF Knowledge Base RAG Ingestion & Q&A",
  icons: { icon: "/icon.svg" },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased min-h-screen font-sans bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 transition-colors duration-200" suppressHydrationWarning>
        <ReactQueryProvider>{children}</ReactQueryProvider>
      </body>
    </html>
  );
}

