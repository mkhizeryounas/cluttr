import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cluttr - Long-term Memory for AI Agents",
  description:
    "Add persistent memory to your AI agents with semantic search and automatic fact extraction. Supports OpenAI and AWS Bedrock.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
