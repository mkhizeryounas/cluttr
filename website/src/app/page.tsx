"use client";

import { useState, useEffect } from "react";

function Logo({ className = "" }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="relative w-8 h-8">
        {/* Brain/memory icon */}
        <svg
          viewBox="0 0 32 32"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full"
        >
          <defs>
            <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#a855f7" />
              <stop offset="50%" stopColor="#6366f1" />
              <stop offset="100%" stopColor="#06b6d4" />
            </linearGradient>
          </defs>
          {/* Outer circle */}
          <circle cx="16" cy="16" r="14" stroke="url(#logoGradient)" strokeWidth="2" fill="none" />
          {/* Inner connected nodes - representing memory/neural network */}
          <circle cx="16" cy="10" r="2.5" fill="url(#logoGradient)" />
          <circle cx="10" cy="18" r="2.5" fill="url(#logoGradient)" />
          <circle cx="22" cy="18" r="2.5" fill="url(#logoGradient)" />
          <circle cx="16" cy="22" r="2" fill="url(#logoGradient)" />
          {/* Connecting lines */}
          <path
            d="M16 12.5V20M12 17L20 17M12.5 16.5L16 12.5L19.5 16.5"
            stroke="url(#logoGradient)"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      <span className="text-xl font-bold tracking-tight">cluttr</span>
    </div>
  );
}

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
      className="absolute top-4 right-4 px-3 py-1.5 text-xs font-medium bg-white/10 hover:bg-white/20 rounded-lg transition-all hover:scale-105"
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
      "LLM extracts important facts, preferences, and context from conversations automatically.",
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
    title: "Smart Query Expansion",
    description:
      "Queries are automatically optimized by LLM for better semantic vector matching.",
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
      "Images in conversations are automatically summarized and stored as searchable memories.",
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
      "LLM-powered deduplication prevents storing redundant or semantically similar facts.",
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
      "Works with OpenAI (GPT-4o-mini) and AWS Bedrock (Claude + Titan embeddings).",
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
        <ellipse cx="12" cy="5" rx="9" ry="3" />
        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
      </svg>
    ),
    title: "PostgreSQL + pgvector",
    description:
      "Built on battle-tested PostgreSQL with pgvector for reliable vector similarity search.",
  },
];

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#050507]/80 backdrop-blur-xl border-b border-white/5">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <a href="/" className="hover:opacity-80 transition-opacity">
            <Logo />
          </a>
          <div className="flex items-center gap-4 sm:gap-6">
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
              className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-300 hover:text-white bg-white/5 hover:bg-white/10 rounded-lg transition-all"
            >
              <GitHubIcon />
              <span className="hidden sm:inline">GitHub</span>
            </a>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <header className="hero-bg grid-bg pt-24 sm:pt-32 pb-20 px-4 sm:px-6 min-h-screen flex items-center">
        {/* Glow orbs */}
        <div className="glow-orb glow-orb-1" />
        <div className="glow-orb glow-orb-2" />
        <div className="glow-orb glow-orb-3" />

        <div className="max-w-4xl mx-auto text-center relative z-10 w-full">
          <div
            className={`transition-all duration-1000 ${
              mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-gray-400 mb-8">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              Open source &amp; free to use
            </div>
          </div>

          <h1
            className={`text-4xl sm:text-5xl md:text-7xl font-extrabold mb-6 leading-tight tracking-tight transition-all duration-1000 delay-100 ${
              mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            Long-term memory
            <br />
            for <span className="gradient-text">AI agents</span>
          </h1>

          <p
            className={`text-base sm:text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed transition-all duration-1000 delay-200 ${
              mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            Add persistent memory to your AI agents with semantic search and
            automatic fact extraction. Built on PostgreSQL + pgvector.
          </p>

          <div
            className={`flex flex-col sm:flex-row gap-4 justify-center mb-12 sm:mb-16 transition-all duration-1000 delay-300 ${
              mounted ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            }`}
          >
            <a
              href="#quickstart"
              className="btn-glow px-8 py-3.5 bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-purple-500/25 transition-all hover:-translate-y-0.5"
            >
              Get Started
            </a>
            <a
              href="https://github.com/mkhizeryounas/cluttr"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-3.5 bg-white/5 text-white font-semibold rounded-xl border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all flex items-center justify-center gap-2 hover:-translate-y-0.5"
            >
              <GitHubIcon />
              View on GitHub
            </a>
          </div>

          <div
            className={`max-w-2xl mx-auto text-left transition-all duration-1000 delay-500 ${
              mounted ? "opacity-100 translate-y-0 scale-100" : "opacity-0 translate-y-8 scale-95"
            }`}
          >
            <CodeBlock
              copyText={`from cluttr import Cluttr

memory = Cluttr(config)

async with memory:
    # Store memories from conversations
    await memory.add(messages, user_id="user_123")

    # Search relevant memories
    results = await memory.search("programming language preferences", user_id="user_123")`}
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
                  &quot;programming language preferences&quot;
                </span>
                , user_id=
                <span className="token-string">&quot;user_123&quot;</span>)
              </code>
            </CodeBlock>
          </div>
        </div>
      </header>

      {/* Features */}
      <section id="features" className="py-20 sm:py-28 px-4 sm:px-6 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-purple-500/5 via-transparent to-transparent" />
        <div className="max-w-6xl mx-auto relative">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">
              Everything you need for{" "}
              <span className="gradient-text">agent memory</span>
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto text-base sm:text-lg">
              Cluttr handles the complexity of memory management so you can focus
              on building great AI experiences.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {features.map((feature, index) => (
              <div
                key={index}
                className="feature-card p-6 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.04]"
              >
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500/20 to-indigo-500/20 flex items-center justify-center text-purple-400 mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quick Start */}
      <section id="quickstart" className="py-20 sm:py-28 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">
              Quick Start
            </h2>
            <p className="text-gray-400 text-base sm:text-lg">
              Get up and running in minutes.
            </p>
          </div>

          <div className="space-y-8 sm:space-y-12">
            {/* Step 1 */}
            <div className="flex gap-4 sm:gap-6">
              <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center font-bold text-sm sm:text-base shadow-lg shadow-purple-500/25">
                1
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-lg sm:text-xl font-semibold mb-3">
                  Install the package
                </h3>
                <CodeBlock showHeader={false} copyText="uv add cluttr">
                  <code>uv add cluttr</code>
                </CodeBlock>
              </div>
            </div>

            {/* Step 2 */}
            <div className="flex gap-4 sm:gap-6">
              <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center font-bold text-sm sm:text-base shadow-lg shadow-purple-500/25">
                2
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-lg sm:text-xl font-semibold mb-3">
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
            <div className="flex gap-4 sm:gap-6">
              <div className="flex-shrink-0 w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center font-bold text-sm sm:text-base shadow-lg shadow-purple-500/25">
                3
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-lg sm:text-xl font-semibold mb-3">
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
      <section className="py-20 sm:py-28 px-4 sm:px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-t from-purple-500/10 via-transparent to-transparent" />
        <div className="max-w-2xl mx-auto text-center relative">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">
            Ready to add memory
            <br />
            to your agents?
          </h2>
          <p className="text-gray-400 mb-8 text-base sm:text-lg">
            Open source and free to use. Star us on GitHub!
          </p>
          <a
            href="https://github.com/mkhizeryounas/cluttr"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-glow inline-flex items-center gap-2 px-8 py-3.5 bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-purple-500/25 transition-all hover:-translate-y-0.5"
          >
            <GitHubIcon />
            View on GitHub
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 border-t border-white/5">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col sm:flex-row justify-between items-center gap-6">
            <div className="text-center sm:text-left">
              <Logo />
              <p className="text-gray-500 text-sm mt-2">
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
