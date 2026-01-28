"use client";

import { useState } from "react";

function GitHubIcon({ className = "" }: { className?: string }) {
  return (
    <svg
      height="20"
      width="20"
      viewBox="0 0 16 16"
      fill="currentColor"
      className={className}
    >
      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
    </svg>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="absolute top-4 right-4 px-3 py-1 text-xs bg-white/10 hover:bg-white/20 rounded-md transition-colors"
    >
      {copied ? "Copied!" : "Copy"}
    </button>
  );
}

function CodeBlock({
  children,
  showHeader = true,
  copyText,
}: {
  children: React.ReactNode;
  showHeader?: boolean;
  copyText?: string;
}) {
  return (
    <div className="code-block relative">
      {showHeader && (
        <div className="code-header">
          <span className="dot red" />
          <span className="dot yellow" />
          <span className="dot green" />
        </div>
      )}
      {copyText && <CopyButton text={copyText} />}
      <pre className="text-sm md:text-base">{children}</pre>
    </div>
  );
}

const features = [
  {
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
      </svg>
    ),
    title: "Automatic Extraction",
    description:
      "LLM-powered extraction of important facts, preferences, and context from conversations.",
  },
  {
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <circle cx="11" cy="11" r="8" />
        <path d="m21 21-4.35-4.35" />
      </svg>
    ),
    title: "Semantic Search",
    description:
      "Find relevant memories using vector similarity search powered by pgvector.",
  },
  {
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
        <circle cx="8.5" cy="8.5" r="1.5" />
        <polyline points="21 15 16 10 5 21" />
      </svg>
    ),
    title: "Image Support",
    description:
      "Automatic summarization of images in conversations. Supports base64, URLs, and file paths.",
  },
  {
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="8.5" cy="7" r="4" />
        <path d="M20 8v6M23 11h-6" />
      </svg>
    ),
    title: "Duplicate Detection",
    description:
      "Smart semantic similarity checks prevent storing redundant information.",
  },
  {
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z" />
      </svg>
    ),
    title: "Multiple Providers",
    description:
      "Works with OpenAI (GPT-4o-mini) and AWS Bedrock (Claude + Titan).",
  },
  {
    icon: (
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
      </svg>
    ),
    title: "Async Native",
    description:
      "Built with async/await from the ground up for high-performance applications.",
  },
];

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/10">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <a href="/" className="text-xl font-bold">
            cluttr
          </a>
          <div className="flex items-center gap-6">
            <a
              href="#features"
              className="text-sm text-gray-400 hover:text-white transition-colors hidden sm:block"
            >
              Features
            </a>
            <a
              href="#quickstart"
              className="text-sm text-gray-400 hover:text-white transition-colors hidden sm:block"
            >
              Quick Start
            </a>
            <a
              href="https://github.com/mkhizeryounas/cluttr"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors"
            >
              <GitHubIcon />
              <span className="hidden sm:inline">GitHub</span>
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <header className="pt-32 pb-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Long-term memory for{" "}
            <span className="gradient-text">AI agents</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
            Add persistent memory to your AI agents with semantic search and
            automatic fact extraction. Built on PostgreSQL + pgvector.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <a
              href="#quickstart"
              className="px-8 py-3 bg-white text-black font-medium rounded-lg hover:bg-gray-200 transition-colors"
            >
              Get Started
            </a>
            <a
              href="https://github.com/mkhizeryounas/cluttr"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-3 bg-white/10 text-white font-medium rounded-lg hover:bg-white/20 transition-colors flex items-center justify-center gap-2"
            >
              <GitHubIcon />
              View on GitHub
            </a>
          </div>

          <div className="max-w-2xl mx-auto">
            <CodeBlock
              copyText={`from cluttr import Cluttr

memory = Cluttr(config)

async with memory:
    # Store memories from conversations
    await memory.add(messages, user_id="user_123")

    # Search relevant memories
    results = await memory.search("What does the user prefer?")`}
            >
              <code>
                <span className="token-keyword">from</span> cluttr{" "}
                <span className="token-keyword">import</span> Cluttr
                {"\n\n"}
                memory = Cluttr(config)
                {"\n\n"}
                <span className="token-keyword">async with</span> memory:
                {"\n"}
                {"    "}
                <span className="token-comment">
                  # Store memories from conversations
                </span>
                {"\n"}
                {"    "}
                <span className="token-keyword">await</span> memory.add(
                messages, user_id=
                <span className="token-string">&quot;user_123&quot;</span>)
                {"\n\n"}
                {"    "}
                <span className="token-comment"># Search relevant memories</span>
                {"\n"}
                {"    "}
                results = <span className="token-keyword">await</span>{" "}
                memory.search(
                <span className="token-string">
                  &quot;What does the user prefer?&quot;
                </span>
                )
              </code>
            </CodeBlock>
          </div>
        </div>
      </header>

      {/* Features */}
      <section id="features" className="py-20 px-6 bg-white/[0.02]">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Everything you need for agent memory
          </h2>
          <p className="text-gray-400 text-center mb-16 max-w-2xl mx-auto">
            Cluttr handles the complexity of memory management so you can focus
            on building great AI experiences.
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 rounded-xl bg-white/[0.03] border border-white/10 hover:border-white/20 transition-colors"
              >
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500/20 to-blue-500/20 flex items-center justify-center text-purple-400 mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400 text-sm">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quick Start */}
      <section id="quickstart" className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">
            Quick Start
          </h2>
          <p className="text-gray-400 text-center mb-16">
            Get up and running in minutes.
          </p>

          <div className="space-y-8">
            {/* Step 1 */}
            <div className="flex gap-6">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center font-bold">
                1
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold mb-3">
                  Install the package
                </h3>
                <CodeBlock showHeader={false} copyText="uv add cluttr">
                  <code>uv add cluttr</code>
                </CodeBlock>
              </div>
            </div>

            {/* Step 2 */}
            <div className="flex gap-6">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center font-bold">
                2
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold mb-3">
                  Configure your provider
                </h3>
                <CodeBlock
                  showHeader={false}
                  copyText={`config = {
    "vector_db": {
        "engine": "postgres",
        "host": "localhost",
        "database": "cluttr",
        "user": "postgres",
        "password": "secret",
    },
    "llm": {
        "provider": "openai",  # or "bedrock"
        "api_key": "sk-...",
    },
}`}
                >
                  <code>
                    config = {"{"}
                    {"\n"}
                    {"    "}
                    <span className="token-string">&quot;vector_db&quot;</span>:{" "}
                    {"{"}
                    {"\n"}
                    {"        "}
                    <span className="token-string">&quot;engine&quot;</span>:{" "}
                    <span className="token-string">&quot;postgres&quot;</span>,
                    {"\n"}
                    {"        "}
                    <span className="token-string">&quot;host&quot;</span>:{" "}
                    <span className="token-string">&quot;localhost&quot;</span>,
                    {"\n"}
                    {"        "}
                    <span className="token-string">&quot;database&quot;</span>:{" "}
                    <span className="token-string">&quot;cluttr&quot;</span>,
                    {"\n"}
                    {"        "}
                    <span className="token-string">&quot;user&quot;</span>:{" "}
                    <span className="token-string">&quot;postgres&quot;</span>,
                    {"\n"}
                    {"        "}
                    <span className="token-string">&quot;password&quot;</span>:{" "}
                    <span className="token-string">&quot;secret&quot;</span>,
                    {"\n"}
                    {"    "}
                    {"}"},
                    {"\n"}
                    {"    "}
                    <span className="token-string">&quot;llm&quot;</span>: {"{"}
                    {"\n"}
                    {"        "}
                    <span className="token-string">&quot;provider&quot;</span>:{" "}
                    <span className="token-string">&quot;openai&quot;</span>,{" "}
                    <span className="token-comment">
                      # or &quot;bedrock&quot;
                    </span>
                    {"\n"}
                    {"        "}
                    <span className="token-string">&quot;api_key&quot;</span>:{" "}
                    <span className="token-string">&quot;sk-...&quot;</span>,
                    {"\n"}
                    {"    "}
                    {"}"},
                    {"\n"}
                    {"}"}
                  </code>
                </CodeBlock>
              </div>
            </div>

            {/* Step 3 */}
            <div className="flex gap-6">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center font-bold">
                3
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold mb-3">
                  Start using memories
                </h3>
                <CodeBlock
                  showHeader={false}
                  copyText={`memory = Cluttr(config)

async with memory:
    # Add memories from conversation
    await memory.add([
        {"role": "user", "content": "I love Python!"},
        {"role": "assistant", "content": "Great choice!"},
    ], user_id="user_123")

    # Search memories
    results = await memory.search(
        "programming preferences",
        user_id="user_123"
    )`}
                >
                  <code>
                    memory = Cluttr(config)
                    {"\n\n"}
                    <span className="token-keyword">async with</span> memory:
                    {"\n"}
                    {"    "}
                    <span className="token-comment">
                      # Add memories from conversation
                    </span>
                    {"\n"}
                    {"    "}
                    <span className="token-keyword">await</span> memory.add([
                    {"\n"}
                    {"        "}
                    {"{"}
                    <span className="token-string">&quot;role&quot;</span>:{" "}
                    <span className="token-string">&quot;user&quot;</span>,{" "}
                    <span className="token-string">&quot;content&quot;</span>:{" "}
                    <span className="token-string">
                      &quot;I love Python!&quot;
                    </span>
                    {"}"},
                    {"\n"}
                    {"        "}
                    {"{"}
                    <span className="token-string">&quot;role&quot;</span>:{" "}
                    <span className="token-string">&quot;assistant&quot;</span>,{" "}
                    <span className="token-string">&quot;content&quot;</span>:{" "}
                    <span className="token-string">
                      &quot;Great choice!&quot;
                    </span>
                    {"}"},
                    {"\n"}
                    {"    "}], user_id=
                    <span className="token-string">&quot;user_123&quot;</span>)
                    {"\n\n"}
                    {"    "}
                    <span className="token-comment"># Search memories</span>
                    {"\n"}
                    {"    "}
                    results = <span className="token-keyword">await</span>{" "}
                    memory.search(
                    {"\n"}
                    {"        "}
                    <span className="token-string">
                      &quot;programming preferences&quot;
                    </span>
                    ,
                    {"\n"}
                    {"        "}
                    user_id=
                    <span className="token-string">&quot;user_123&quot;</span>
                    {"\n"}
                    {"    "})
                  </code>
                </CodeBlock>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 bg-gradient-to-b from-white/[0.02] to-transparent">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to add memory to your agents?
          </h2>
          <p className="text-gray-400 mb-8">
            Open source and free to use. Star us on GitHub!
          </p>
          <a
            href="https://github.com/mkhizeryounas/cluttr"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-3 bg-white text-black font-medium rounded-lg hover:bg-gray-200 transition-colors"
          >
            <GitHubIcon />
            View on GitHub
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-white/10">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
              <span className="text-xl font-bold">cluttr</span>
              <p className="text-gray-400 text-sm mt-1">
                Long-term memory for AI agents
              </p>
            </div>
            <div className="flex items-center gap-6 text-sm text-gray-400">
              <a
                href="https://github.com/mkhizeryounas/cluttr"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-white transition-colors"
              >
                GitHub
              </a>
              <a
                href="https://github.com/mkhizeryounas/cluttr/issues"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-white transition-colors"
              >
                Issues
              </a>
              <span>MIT License</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
