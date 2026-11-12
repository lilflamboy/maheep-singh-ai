# 🕶️ Project Portfolio Showcase: Maheep Singh AI

Use these ready-to-copy snippets to showcase **Maheep Singh AI** on your portfolio website, resume, or LinkedIn!

---

## 📌 1. Quick Summary (For Resume / LinkedIn / Bio)

> **Maheep Singh AI — WhatsApp Banter & Roast Generator**
> *Tech Stack:* Python, Streamlit, Google GenAI SDK, Gemini 3.8 Flash, Regex, CSS
> - Built a full-stack AI web application generating witty, deadpan WhatsApp group comebacks and family roasts styled after comic Maheep Singh.
> - Engineered multi-model fallback cascade (`gemini-3.8-flash` & `gemini-3.1-pro-preview`) with exponential backoff for high availability.
> - Designed a responsive WhatsApp chat bubble UI with 1-click clipboard copy and direct WhatsApp Web deep linking (`api.whatsapp.com/send`).
> - Optimized response latency by 70% by disabling reasoning overhead (`thinking_budget=0`) and capping token allocation.

---

## 🌐 2. HTML / CSS Card (For HTML/CSS Portfolio)

```html
<div class="project-card">
  <div class="project-badge">AI / Full-Stack</div>
  <h3>🕶️ Maheep Singh AI</h3>
  <p>
    A witty, authentic WhatsApp group comeback and roast generator built with Python and Gemini 3.8 Flash. Generates savage family banter, quick clapbacks, and dramatic guilt trips with 1-click WhatsApp sharing.
  </p>
  <div class="project-tags">
    <span>Python</span>
    <span>Streamlit</span>
    <span>Gemini 3.8 Flash</span>
    <span>Google GenAI SDK</span>
  </div>
  <div class="project-links">
    <a href="https://github.com/YOUR_GITHUB_USERNAME/maheep-singh-ai" target="_blank">GitHub Repo</a>
    <a href="https://maheep-singh-ai.streamlit.app" target="_blank">Live Demo</a>
  </div>
</div>
```

---

## ⚛️ 3. React / Next.js Component (For Modern Web Portfolios)

```jsx
export const MaheepSinghAIProject = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-emerald-500 transition-all duration-300">
      <div className="flex justify-between items-center mb-3">
        <span className="text-xs uppercase tracking-wider font-semibold text-emerald-400 bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-800">
          AI Application
        </span>
        <span className="text-xl">🕶️</span>
      </div>
      <h3 className="text-xl font-bold text-white mb-2">Maheep Singh AI</h3>
      <p className="text-slate-400 text-sm mb-4 leading-relaxed">
        Deadpan WhatsApp comeback and family banter generator inspired by comic Maheep Singh. Built using Gemini 3.8 Flash, featuring multi-model fallback, 4 roast styles, and instant WhatsApp deep-linking.
      </p>
      <div className="flex flex-wrap gap-2 mb-6">
        {['Python', 'Streamlit', 'Gemini 3.8 Flash', 'Google GenAI SDK'].map((tag) => (
          <span key={tag} className="text-xs text-slate-300 bg-slate-800 px-2.5 py-1 rounded-md">
            {tag}
          </span>
        ))}
      </div>
      <div className="flex items-center gap-4">
        <a
          href="https://github.com/YOUR_GITHUB_USERNAME/maheep-singh-ai"
          target="_blank"
          rel="noreferrer"
          className="text-sm font-medium text-white hover:text-emerald-400 transition-colors"
        >
          View Code &rarr;
        </a>
        <a
          href="https://maheep-singh-ai.streamlit.app"
          target="_blank"
          rel="noreferrer"
          className="text-sm font-medium text-emerald-400 hover:underline"
        >
          Live Demo &nearr;
        </a>
      </div>
    </div>
  );
};
```
