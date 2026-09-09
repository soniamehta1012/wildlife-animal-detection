import React, { createContext, useContext, useEffect, useRef, useState, useCallback } from "react";
import {
  Leaf, Upload, Image as ImageIcon, Sparkles, ScanSearch, ShieldCheck,
  AlertTriangle, CircleCheck, Menu, X, ArrowRight, Mail, Send, Globe,
  TreePine, RefreshCcw, Trash2, MapPin, Users, BookOpen, Compass
} from "lucide-react";

/* ------------------------------------------------------------------ */
/* MOCK DATA                                                          */
/* ------------------------------------------------------------------ */

const STATUS_META = {
  "Extinct": { color: "#5C1A1A", bg: "#F5E4E4", icon: X, label: "Extinct" },
  "Extinct in the Wild": { color: "#7A2410", bg: "#F6E3DA", icon: AlertTriangle, label: "Extinct in the Wild" },
  "Critically Endangered": { color: "#9A2F14", bg: "#FBE4DA", icon: AlertTriangle, label: "Critically Endangered" },
  "Endangered": { color: "#B5560E", bg: "#FCEBDA", icon: AlertTriangle, label: "Endangered" },
  "Vulnerable": { color: "#8A6B0A", bg: "#FCF3D6", icon: ShieldCheck, label: "Vulnerable" },
  "Near Threatened": { color: "#5C7A1E", bg: "#EFF5DC", icon: ShieldCheck, label: "Near Threatened" },
  "Least Concern": { color: "#1E6B3C", bg: "#E1F1E5", icon: CircleCheck, label: "Least Concern" },
};

const MOCK_RESULTS = [
  {
    name: "Red Panda",
    scientificName: "Ailurus fulgens",
    status: "Endangered",
    confidence: 94,
    description:
      "The red panda is a small mammal native to the eastern Himalayas and southwestern China. Its population is threatened by habitat loss and fragmentation, with fewer than 10,000 mature individuals believed to remain in the wild.",
    habitat: "Temperate forests, Eastern Himalayas",
    diet: "Bamboo, fruit, insects",
  },
  {
    name: "Snow Leopard",
    scientificName: "Panthera uncia",
    status: "Vulnerable",
    confidence: 91,
    description:
      "Snow leopards inhabit the high mountain ranges of Central and South Asia. Their thick fur and wide paws are adaptations to cold, rocky terrain, but poaching and climate change continue to shrink their range.",
    habitat: "Alpine and subalpine zones, Central Asia",
    diet: "Blue sheep, ibex, marmots",
  },
  {
    name: "Amur Leopard",
    scientificName: "Panthera pardus orientalis",
    status: "Critically Endangered",
    confidence: 88,
    description:
      "One of the rarest big cats on Earth, the Amur leopard survives in a small pocket of forest along the Russia-China border. Conservation efforts have helped its numbers rise slowly from historic lows.",
    habitat: "Temperate forests, Russian Far East",
    diet: "Deer, hares, small mammals",
  },
];

function pickMockResult() {
  return MOCK_RESULTS[Math.floor(Math.random() * MOCK_RESULTS.length)];
}

/* ------------------------------------------------------------------ */
/* APP CONTEXT — simulates route state + shared analysis result       */
/* ------------------------------------------------------------------ */

const AppContext = createContext(null);
const usePage = () => useContext(AppContext);

const PAGES = [
  { id: "home", label: "Home" },
  { id: "about", label: "About Us" },
  { id: "results", label: "Results" },
  { id: "how-it-works", label: "How It Works" },
  { id: "contact", label: "Contact" },
];

/* ------------------------------------------------------------------ */
/* TOAST                                                              */
/* ------------------------------------------------------------------ */

function Toast({ toast, onClose }) {
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(onClose, 3600);
    return () => clearTimeout(t);
  }, [toast, onClose]);

  if (!toast) return null;
  const Icon = toast.type === "error" ? AlertTriangle : CircleCheck;

  return (
    <div className="wl-toast-wrap" aria-live="polite">
      <div className={`wl-toast wl-toast-${toast.type}`} role="status">
        <Icon size={18} strokeWidth={2.2} />
        <span>{toast.message}</span>
        <button aria-label="Dismiss notification" onClick={onClose} className="wl-toast-close">
          <X size={15} />
        </button>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* NAVBAR                                                             */
/* ------------------------------------------------------------------ */

function Navbar() {
  const { page, navigate } = usePage();
  const [open, setOpen] = useState(false);

  const go = (id) => {
    navigate(id);
    setOpen(false);
  };

  return (
    <header className="wl-nav-outer">
      <nav className="wl-nav" aria-label="Primary">
        <button className="wl-brand" onClick={() => go("home")} aria-label="WildLens home">
          <span className="wl-brand-mark">
            <Leaf size={18} strokeWidth={2.2} />
          </span>
          <span className="wl-brand-text">WildLens</span>
        </button>

        <ul className="wl-nav-links">
          {PAGES.map((p) => (
            <li key={p.id}>
              <button
                className={`wl-nav-link ${page === p.id ? "is-active" : ""}`}
                aria-current={page === p.id ? "page" : undefined}
                onClick={() => go(p.id)}
              >
                {p.label}
              </button>
            </li>
          ))}
        </ul>

        <button
          className="wl-nav-toggle"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </nav>

      <div className={`wl-nav-mobile ${open ? "is-open" : ""}`}>
        <ul>
          {PAGES.map((p) => (
            <li key={p.id}>
              <button
                className={`wl-nav-mobile-link ${page === p.id ? "is-active" : ""}`}
                onClick={() => go(p.id)}
              >
                {p.label}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </header>
  );
}

/* ------------------------------------------------------------------ */
/* FOOTER                                                             */
/* ------------------------------------------------------------------ */

function Footer() {
  const { navigate } = usePage();
  return (
    <footer className="wl-footer">
      <div className="wl-footer-inner">
        <div className="wl-footer-brand">
          <span className="wl-brand-mark small">
            <Leaf size={16} strokeWidth={2.2} />
          </span>
          <div>
            <p className="wl-footer-name">WildLens</p>
            <p className="wl-footer-desc">
              AI-powered wildlife identification for a more informed and conscious world.
            </p>
          </div>
        </div>
        <ul className="wl-footer-links">
          {PAGES.map((p) => (
            <li key={p.id}>
              <button onClick={() => navigate(p.id)}>{p.label}</button>
            </li>
          ))}
        </ul>
      </div>
      <div className="wl-footer-bottom">© 2026 WildLens. Built for wildlife awareness.</div>
    </footer>
  );
}

/* ------------------------------------------------------------------ */
/* STATUS BADGE                                                       */
/* ------------------------------------------------------------------ */

function StatusBadge({ status, size = "md" }) {
  const meta = STATUS_META[status] || STATUS_META["Least Concern"];
  const Icon = meta.icon;
  return (
    <span
      className={`wl-status-badge wl-status-${size}`}
      style={{ color: meta.color, background: meta.bg, borderColor: meta.color + "33" }}
    >
      <Icon size={size === "sm" ? 13 : 15} strokeWidth={2.4} />
      {meta.label}
    </span>
  );
}

/* ------------------------------------------------------------------ */
/* CONFIDENCE RING                                                    */
/* ------------------------------------------------------------------ */

function ConfidenceRing({ value }) {
  const [display, setDisplay] = useState(0);
  const r = 46;
  const c = 2 * Math.PI * r;

  useEffect(() => {
    let raf;
    const start = performance.now();
    const duration = 900;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      setDisplay(Math.round(value * (1 - Math.pow(1 - t, 3))));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [value]);

  const offset = c - (display / 100) * c;

  return (
    <div className="wl-ring" role="img" aria-label={`AI confidence ${value} percent`}>
      <svg viewBox="0 0 110 110" width="120" height="120">
        <circle cx="55" cy="55" r={r} fill="none" stroke="#E8F0E5" strokeWidth="9" />
        <circle
          cx="55" cy="55" r={r} fill="none" stroke="#198754" strokeWidth="9"
          strokeLinecap="round" strokeDasharray={c} strokeDashoffset={offset}
          transform="rotate(-90 55 55)"
        />
      </svg>
      <div className="wl-ring-label">
        <span className="wl-ring-value">{display}%</span>
        <span className="wl-ring-caption">Confidence</span>
      </div>
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* IMAGE UPLOADER                                                     */
/* ------------------------------------------------------------------ */

const MAX_BYTES = 10 * 1024 * 1024;
const ACCEPTED = ["image/jpeg", "image/jpg", "image/png"];

function ImageUploader({ file, previewUrl, onFile, onClear, showError }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const validate = (f) => {
    if (!f) return;
    if (!ACCEPTED.includes(f.type)) {
      showError("Please upload a JPG, JPEG, or PNG image.");
      return;
    }
    if (f.size > MAX_BYTES) {
      showError("Image size must be less than 10MB.");
      return;
    }
    onFile(f);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files?.[0];
    validate(f);
  };

  return (
    <div className="wl-uploader-wrap">
      {!previewUrl ? (
        <div
          className={`wl-dropzone ${dragging ? "is-dragging" : ""}`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={onDrop}
          onClick={() => inputRef.current?.click()}
          role="button"
          tabIndex={0}
          aria-label="Upload an animal image, drag and drop or click to browse"
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              inputRef.current?.click();
            }
          }}
        >
          <div className="wl-dropzone-icon">
            <ImageIcon size={30} strokeWidth={1.8} />
          </div>
          <p className="wl-dropzone-title">Drag &amp; Drop Your Animal Image</p>
          <p className="wl-dropzone-sub">or click to browse</p>
          <p className="wl-dropzone-meta">Supported formats: JPG, JPEG, PNG &nbsp;•&nbsp; Max size: 10MB</p>
          <input
            ref={inputRef}
            type="file"
            accept=".jpg,.jpeg,.png,image/jpeg,image/png"
            className="wl-sr-only"
            aria-hidden="true"
            tabIndex={-1}
            onChange={(e) => validate(e.target.files?.[0])}
          />
        </div>
      ) : (
        <div className="wl-preview">
          <img src={previewUrl} alt="Selected animal preview" className="wl-preview-img" />
          <div className="wl-preview-actions">
            <button className="wl-btn wl-btn-ghost" onClick={() => inputRef.current?.click()}>
              <RefreshCcw size={15} /> Change Image
            </button>
            <button className="wl-btn wl-btn-ghost wl-btn-danger" onClick={onClear}>
              <Trash2 size={15} /> Remove
            </button>
            <input
              ref={inputRef}
              type="file"
              accept=".jpg,.jpeg,.png,image/jpeg,image/png"
              className="wl-sr-only"
              aria-hidden="true"
              tabIndex={-1}
              onChange={(e) => validate(e.target.files?.[0])}
            />
          </div>
        </div>
      )}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* HOME PAGE                                                          */
/* ------------------------------------------------------------------ */

function Hero() {
  return (
    <section className="wl-hero">
      <div className="wl-hero-deco" aria-hidden="true">
        <svg viewBox="0 0 400 400" className="wl-hero-leaf">
          <path d="M40 360 C 40 180, 180 40, 360 40 C 340 220, 220 340, 40 360 Z" fill="none" stroke="#A8D96C" strokeWidth="1.4" opacity="0.55" />
          <path d="M60 340 C 90 220, 220 90, 340 60" fill="none" stroke="#43A047" strokeWidth="1" opacity="0.35" />
        </svg>
      </div>
      <div className="wl-hero-inner">
        <p className="wl-eyebrow">AI-Powered Wildlife Identification</p>
        <h1 className="wl-hero-title">Discover the Wild. Protect the Future.</h1>
        <p className="wl-hero-sub">
          Upload an animal image and discover its identity and conservation status in seconds.
        </p>
      </div>
    </section>
  );
}

function LoadingState() {
  return (
    <div className="wl-loading" role="status" aria-live="polite">
      <div className="wl-scanner">
        <ScanSearch size={26} strokeWidth={1.8} />
        <span className="wl-scanner-bar" />
      </div>
      <p className="wl-loading-title">Analyzing your image…</p>
      <p className="wl-loading-sub">Identifying species and conservation status</p>
    </div>
  );
}

function ResultPreview({ result, onViewFull }) {
  const meta = STATUS_META[result.status];
  return (
    <div className="wl-result-preview">
      <div className="wl-result-preview-header">
        <Sparkles size={16} />
        <span>Analysis complete</span>
      </div>
      <div className="wl-result-preview-body">
        <div>
          <p className="wl-result-name">{result.name}</p>
          <p className="wl-result-sci">{result.scientificName}</p>
          <StatusBadge status={result.status} size="sm" />
        </div>
        <div className="wl-result-preview-confidence">
          <span className="wl-result-preview-confidence-value">{result.confidence}%</span>
          <span className="wl-result-preview-confidence-label">AI confidence</span>
        </div>
      </div>
      <button className="wl-btn wl-btn-primary wl-btn-block" onClick={onViewFull}>
        View Full Result <ArrowRight size={16} />
      </button>
    </div>
  );
}

function ConservationAwareness() {
  return (
    <section className="wl-awareness">
      <div className="wl-awareness-inner">
        <TreePine size={22} strokeWidth={1.8} />
        <h2>Every identification can spark awareness.</h2>
        <p>Understanding the species around us is the first step toward protecting them.</p>
      </div>
    </section>
  );
}

function HomePage() {
  const { navigate, setResult, showToast } = usePage();
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | done
  const [localResult, setLocalResult] = useState(null);

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  const handleFile = (f) => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setFile(f);
    setPreviewUrl(URL.createObjectURL(f));
    setStatus("idle");
    setLocalResult(null);
  };

  const handleClear = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setFile(null);
    setPreviewUrl(null);
    setStatus("idle");
    setLocalResult(null);
  };

  const analyze = () => {
    if (!file) {
      showToast("Please upload an animal image first.", "error");
      return;
    }
    setStatus("loading");
    window.setTimeout(() => {
      const mock = pickMockResult();
      setLocalResult(mock);
      setResult({ ...mock, imageUrl: previewUrl });
      setStatus("done");
    }, 1500);
  };

  return (
    <>
      <Hero />

      <section className="wl-upload-section">
        <div className="wl-upload-inner">
          <ImageUploader
            file={file}
            previewUrl={previewUrl}
            onFile={handleFile}
            onClear={handleClear}
            showError={(msg) => showToast(msg, "error")}
          />

          <button
            className="wl-btn wl-btn-primary wl-btn-lg"
            onClick={analyze}
            disabled={status === "loading"}
          >
            <Sparkles size={18} />
            Analyze Animal
          </button>

          <div className="wl-result-slot">
            {status === "loading" && <LoadingState />}
            {status === "done" && localResult && (
              <ResultPreview result={localResult} onViewFull={() => navigate("results")} />
            )}
          </div>
        </div>
      </section>

      <ConservationAwareness />
    </>
  );
}

/* ------------------------------------------------------------------ */
/* RESULTS PAGE                                                       */
/* ------------------------------------------------------------------ */

function ResultCard({ result }) {
  return (
    <div className="wl-result-card">
      <div className="wl-result-card-media">
        <img src={result.imageUrl} alt={`Photo of a ${result.name}`} />
      </div>
      <div className="wl-result-card-body">
        <div className="wl-result-card-top">
          <div>
            <p className="wl-field-label">Animal</p>
            <h2 className="wl-result-card-name">{result.name}</h2>
            <p className="wl-field-label" style={{ marginTop: 10 }}>Scientific Name</p>
            <p className="wl-result-card-sci">{result.scientificName}</p>
          </div>
          <ConfidenceRing value={result.confidence} />
        </div>

        <div className="wl-result-card-status">
          <p className="wl-field-label">Conservation Status</p>
          <StatusBadge status={result.status} />
        </div>

        <div className="wl-result-card-grid">
          <div>
            <p className="wl-field-label">Habitat</p>
            <p className="wl-result-card-text">{result.habitat}</p>
          </div>
          <div>
            <p className="wl-field-label">Diet</p>
            <p className="wl-result-card-text">{result.diet}</p>
          </div>
        </div>

        <div>
          <p className="wl-field-label">Description</p>
          <p className="wl-result-card-desc">{result.description}</p>
        </div>
      </div>
    </div>
  );
}

function ResultsPage() {
  const { result, navigate } = usePage();

  return (
    <section className="wl-page">
      <div className="wl-page-inner">
        <p className="wl-eyebrow">Your Wildlife Discovery</p>
        <h1 className="wl-page-title">Analysis Result</h1>

        {result ? (
          <div className="wl-page-content">
            <ResultCard result={result} />
          </div>
        ) : (
          <div className="wl-empty-state">
            <div className="wl-empty-icon">
              <Compass size={26} strokeWidth={1.8} />
            </div>
            <p className="wl-empty-title">No animal has been analyzed yet.</p>
            <p className="wl-empty-sub">Upload an image above to discover its conservation status.</p>
            <button className="wl-btn wl-btn-primary" onClick={() => navigate("home")}>
              Analyze an Animal <ArrowRight size={16} />
            </button>
          </div>
        )}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* ABOUT PAGE                                                         */
/* ------------------------------------------------------------------ */

const ABOUT_CARDS = [
  {
    icon: Compass,
    title: "Our Mission",
    text: "Make wildlife identification and conservation awareness accessible to anyone with a camera and curiosity.",
  },
  {
    icon: BookOpen,
    title: "Wildlife Literacy",
    text: "Help people recognize the species around them and understand what their conservation status actually means.",
  },
  {
    icon: Globe,
    title: "Global Awareness",
    text: "Every identification connects a person to a wider story about habitat loss, climate change, and recovery.",
  },
];

const ABOUT_STATS = [
  { value: "7", label: "Conservation status tiers tracked" },
  { value: "3", label: "Simple steps from photo to insight" },
  { value: "100%", label: "Frontend demo, ready for a real model" },
];

function AboutPage() {
  return (
    <section className="wl-page">
      <div className="wl-page-inner">
        <p className="wl-eyebrow">Who We Are</p>
        <h1 className="wl-page-title">About WildLens</h1>
        <p className="wl-page-lede">
          WildLens is designed to make wildlife identification and conservation awareness more
          accessible. The platform helps people identify animals from images and understand their
          conservation status, encouraging greater awareness of endangered and threatened wildlife.
        </p>

        <div className="wl-card-grid">
          {ABOUT_CARDS.map((c) => (
            <div className="wl-info-card" key={c.title}>
              <div className="wl-info-card-icon">
                <c.icon size={20} strokeWidth={1.8} />
              </div>
              <h3>{c.title}</h3>
              <p>{c.text}</p>
            </div>
          ))}
        </div>

        <div className="wl-stats-row">
          {ABOUT_STATS.map((s) => (
            <div className="wl-stat" key={s.label}>
              <p className="wl-stat-value">{s.value}</p>
              <p className="wl-stat-label">{s.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* HOW IT WORKS PAGE                                                  */
/* ------------------------------------------------------------------ */

const STEPS = [
  { n: "01", title: "Upload", text: "Upload or drag and drop an animal image.", icon: Upload },
  { n: "02", title: "Analyze", text: "Our system analyzes the image and identifies the animal.", icon: ScanSearch },
  { n: "03", title: "Discover", text: "View the animal's conservation status and information.", icon: Leaf },
];

function HowItWorksPage() {
  return (
    <section className="wl-page">
      <div className="wl-page-inner">
        <p className="wl-eyebrow">The Process</p>
        <h1 className="wl-page-title">How It Works</h1>
        <p className="wl-page-lede">From a single image to meaningful wildlife insight.</p>

        <div className="wl-steps">
          {STEPS.map((s, i) => (
            <div className="wl-step-card" key={s.n}>
              <span className="wl-step-num">{s.n}</span>
              <div className="wl-step-icon">
                <s.icon size={22} strokeWidth={1.8} />
              </div>
              <h3>{s.title}</h3>
              <p>{s.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* CONTACT PAGE                                                       */
/* ------------------------------------------------------------------ */

const CONTACT_INFO = [
  { icon: Mail, title: "Email", text: "hello@wildlens.app" },
  { icon: MapPin, title: "Based", text: "Remote-first, worldwide" },
  { icon: Users, title: "Community", text: "Open to researchers &amp; naturalists" },
];

function ContactPage() {
  const { showToast } = usePage();
  const [form, setForm] = useState({ name: "", email: "", message: "" });

  const update = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = (e) => {
    e.preventDefault();
    if (!form.name.trim() || !form.email.trim() || !form.message.trim()) {
      showToast("Please fill in all required fields.", "error");
      return;
    }
    showToast("Thanks for reaching out! Your message has been received.", "success");
    setForm({ name: "", email: "", message: "" });
  };

  return (
    <section className="wl-page">
      <div className="wl-page-inner">
        <p className="wl-eyebrow">Get In Touch</p>
        <h1 className="wl-page-title">Connect With WildLens</h1>
        <p className="wl-page-lede">
          Have a question, suggestion, or idea for improving wildlife awareness? We'd love to hear from you.
        </p>

        <div className="wl-contact-grid">
          <form className="wl-form" onSubmit={submit} noValidate>
            <label className="wl-field">
              <span>Name</span>
              <input type="text" value={form.name} onChange={update("name")} placeholder="Your name" />
            </label>
            <label className="wl-field">
              <span>Email</span>
              <input type="email" value={form.email} onChange={update("email")} placeholder="you@example.com" />
            </label>
            <label className="wl-field">
              <span>Message</span>
              <textarea rows={5} value={form.message} onChange={update("message")} placeholder="Tell us what's on your mind" />
            </label>
            <button type="submit" className="wl-btn wl-btn-primary wl-btn-block">
              Send Message <Send size={15} />
            </button>
          </form>

          <div className="wl-contact-cards">
            {CONTACT_INFO.map((c) => (
              <div className="wl-contact-card" key={c.title}>
                <c.icon size={18} strokeWidth={1.8} />
                <div>
                  <p className="wl-contact-card-title">{c.title}</p>
                  <p className="wl-contact-card-text">{c.text}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* APP SHELL                                                          */
/* ------------------------------------------------------------------ */

const PAGE_COMPONENTS = {
  "home": HomePage,
  "about": AboutPage,
  "results": ResultsPage,
  "how-it-works": HowItWorksPage,
  "contact": ContactPage,
};

export default function WildLensApp() {
  const [page, setPage] = useState("home");
  const [transitioning, setTransitioning] = useState(false);
  const [result, setResult] = useState(null);
  const [toast, setToast] = useState(null);

  const navigate = useCallback((id) => {
    setTransitioning(true);
    window.setTimeout(() => {
      setPage(id);
      window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
      setTransitioning(false);
    }, 180);
  }, []);

  const showToast = useCallback((message, type = "success") => {
    setToast({ message, type, id: Date.now() });
  }, []);

  const Current = PAGE_COMPONENTS[page] || HomePage;

  return (
    <AppContext.Provider value={{ page, navigate, result, setResult, showToast }}>
      <div className="wl-root">
        <style>{CSS}</style>
        <Navbar />
        <main className={`wl-main ${transitioning ? "is-leaving" : "is-entering"}`}>
          <Current />
        </main>
        <Footer />
        <Toast toast={toast} onClose={() => setToast(null)} />
      </div>
    </AppContext.Provider>
  );
}

/* ------------------------------------------------------------------ */
/* STYLES                                                             */
/* ------------------------------------------------------------------ */

const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root{
  --deep-forest:#12372A;
  --dark-evergreen:#0B241B;
  --emerald:#198754;
  --fresh-green:#43A047;
  --lime:#A8D96C;
  --off-white:#F7F8F3;
  --sage:#E8F0E5;
  --muted-green:#78917F;
  --white:#FFFFFF;
}

.wl-root{
  font-family:'Inter', sans-serif;
  background:var(--off-white);
  color:var(--deep-forest);
  min-height:100vh;
  display:flex;
  flex-direction:column;
}
.wl-root *{ box-sizing:border-box; }
.wl-root h1,.wl-root h2,.wl-root h3{ font-family:'Plus Jakarta Sans', sans-serif; margin:0; }
.wl-root p{ margin:0; }
.wl-root button{ font-family:inherit; cursor:pointer; }
.wl-sr-only{ position:absolute; width:1px; height:1px; overflow:hidden; opacity:0; }

.wl-root button:focus-visible,
.wl-root a:focus-visible,
.wl-root input:focus-visible,
.wl-root textarea:focus-visible{
  outline:2px solid var(--emerald);
  outline-offset:2px;
  border-radius:6px;
}

/* ---------- Navbar ---------- */
.wl-nav-outer{
  position:sticky; top:0; z-index:40;
  padding:14px 20px 0;
}
.wl-nav{
  max-width:1180px; margin:0 auto;
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 18px;
  background:rgba(247,248,243,0.72);
  backdrop-filter:blur(14px);
  -webkit-backdrop-filter:blur(14px);
  border:1px solid rgba(18,55,42,0.09);
  border-radius:16px;
  box-shadow:0 8px 24px rgba(18,55,42,0.06);
}
.wl-brand{
  display:flex; align-items:center; gap:9px;
  background:none; border:none; padding:4px;
}
.wl-brand-mark{
  width:32px; height:32px; border-radius:10px;
  background:linear-gradient(135deg, var(--emerald), var(--fresh-green));
  color:#fff; display:flex; align-items:center; justify-content:center;
  flex-shrink:0;
}
.wl-brand-mark.small{ width:26px; height:26px; border-radius:8px; }
.wl-brand-text{ font-weight:800; font-size:1.08rem; color:var(--deep-forest); letter-spacing:-0.01em; }

.wl-nav-links{ list-style:none; display:flex; gap:2px; margin:0; padding:0; }
.wl-nav-link{
  position:relative; background:none; border:none;
  padding:9px 15px; font-size:0.92rem; font-weight:600;
  color:var(--deep-forest); border-radius:10px;
  transition:background 0.2s ease, color 0.2s ease;
}
.wl-nav-link::after{
  content:""; position:absolute; left:15px; right:15px; bottom:5px;
  height:2px; background:var(--emerald); border-radius:2px;
  transform:scaleX(0); transform-origin:left; transition:transform 0.25s ease;
}
.wl-nav-link:hover{ background:rgba(25,135,84,0.08); color:var(--emerald); }
.wl-nav-link:hover::after{ transform:scaleX(1); }
.wl-nav-link.is-active{ background:var(--sage); color:var(--emerald); }
.wl-nav-link.is-active::after{ transform:scaleX(1); }

.wl-nav-toggle{ display:none; background:none; border:none; color:var(--deep-forest); padding:6px; }

.wl-nav-mobile{
  max-width:1180px; margin:0 auto;
  max-height:0; overflow:hidden; opacity:0;
  transition:max-height 0.32s ease, opacity 0.25s ease, margin 0.3s ease;
}
.wl-nav-mobile.is-open{ max-height:320px; opacity:1; margin-top:8px; }
.wl-nav-mobile ul{
  list-style:none; margin:0; padding:10px;
  background:rgba(247,248,243,0.95); border:1px solid rgba(18,55,42,0.09);
  border-radius:14px; display:flex; flex-direction:column; gap:2px;
  backdrop-filter:blur(14px);
}
.wl-nav-mobile-link{
  width:100%; text-align:left; background:none; border:none;
  padding:11px 12px; border-radius:9px; font-weight:600; font-size:0.95rem;
  color:var(--deep-forest);
}
.wl-nav-mobile-link.is-active{ background:var(--sage); color:var(--emerald); }

/* ---------- Page transition ---------- */
.wl-main{ flex:1; transition:opacity 0.18s ease, transform 0.18s ease; }
.wl-main.is-leaving{ opacity:0; transform:translateY(6px); }
.wl-main.is-entering{ opacity:1; transform:translateY(0); }
@media (prefers-reduced-motion: reduce){
  .wl-main{ transition:none; }
}

/* ---------- Buttons ---------- */
.wl-btn{
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  border:none; border-radius:12px; font-weight:700; font-size:0.94rem;
  padding:13px 22px; transition:transform 0.18s ease, box-shadow 0.18s ease, background 0.2s ease;
}
.wl-btn-primary{
  background:var(--emerald); color:#fff;
  box-shadow:0 10px 24px rgba(25,135,84,0.28);
}
.wl-btn-primary:hover{ background:var(--fresh-green); transform:translateY(-2px); box-shadow:0 14px 28px rgba(25,135,84,0.34); }
.wl-btn-primary:active{ transform:translateY(0px) scale(0.98); }
.wl-btn-primary:disabled{ opacity:0.65; cursor:not-allowed; transform:none; }
.wl-btn-lg{ padding:15px 30px; font-size:1rem; }
.wl-btn-block{ width:100%; }
.wl-btn-ghost{
  background:#fff; color:var(--deep-forest); border:1px solid rgba(18,55,42,0.14);
}
.wl-btn-ghost:hover{ background:var(--sage); border-color:var(--emerald); }
.wl-btn-danger:hover{ background:#FBE4DA; color:#9A2F14; border-color:#9A2F1440; }

/* ---------- Hero ---------- */
.wl-hero{ position:relative; overflow:hidden; padding:70px 20px 30px; }
.wl-hero-inner{ max-width:720px; margin:0 auto; text-align:center; position:relative; z-index:1; }
.wl-eyebrow{
  font-size:0.82rem; font-weight:700; color:var(--emerald);
  letter-spacing:0.01em; margin-bottom:14px;
}
.wl-hero-title{
  font-size:clamp(2rem, 4.4vw, 3.1rem); font-weight:800; line-height:1.12;
  color:var(--deep-forest); letter-spacing:-0.02em; margin-bottom:16px;
}
.wl-hero-sub{ font-size:1.06rem; color:var(--muted-green); line-height:1.6; max-width:520px; margin:0 auto; }
.wl-hero-deco{ position:absolute; top:-40px; right:-60px; width:400px; height:400px; opacity:0.8; pointer-events:none; }
.wl-hero-leaf{ width:100%; height:100%; }

/* ---------- Upload section ---------- */
.wl-upload-section{ padding:20px 20px 10px; }
.wl-upload-inner{ max-width:640px; margin:0 auto; display:flex; flex-direction:column; align-items:center; gap:22px; }
.wl-uploader-wrap{ width:100%; }

.wl-dropzone{
  border:1.5px dashed rgba(18,55,42,0.25); border-radius:20px;
  background:#fff; padding:52px 24px; text-align:center;
  display:flex; flex-direction:column; align-items:center; gap:6px;
  transition:transform 0.2s ease, border-color 0.2s ease, background 0.2s ease, box-shadow 0.2s ease;
  box-shadow:0 4px 16px rgba(18,55,42,0.04);
}
.wl-dropzone:hover{
  border-color:var(--emerald); background:var(--sage);
  transform:translateY(-2px); box-shadow:0 12px 28px rgba(18,55,42,0.08);
}
.wl-dropzone.is-dragging{
  border-color:var(--emerald); background:var(--sage);
  transform:scale(1.01); box-shadow:0 16px 32px rgba(25,135,84,0.18);
}
.wl-dropzone-icon{
  width:56px; height:56px; border-radius:16px; background:var(--sage);
  color:var(--emerald); display:flex; align-items:center; justify-content:center;
  margin-bottom:8px; transition:transform 0.25s ease;
}
.wl-dropzone:hover .wl-dropzone-icon, .wl-dropzone.is-dragging .wl-dropzone-icon{ transform:translateY(-3px) scale(1.05); }
.wl-dropzone-title{ font-weight:700; font-size:1.05rem; color:var(--deep-forest); }
.wl-dropzone-sub{ color:var(--muted-green); font-size:0.92rem; }
.wl-dropzone-meta{ color:var(--muted-green); font-size:0.78rem; margin-top:10px; }

.wl-preview{
  background:#fff; border-radius:20px; border:1px solid rgba(18,55,42,0.08);
  padding:16px; box-shadow:0 8px 22px rgba(18,55,42,0.06);
  animation:wl-fade-in 0.35s ease;
}
.wl-preview-img{
  width:100%; max-height:360px; object-fit:contain; border-radius:14px; background:var(--sage);
}
.wl-preview-actions{ display:flex; gap:10px; margin-top:14px; }
@keyframes wl-fade-in{ from{opacity:0; transform:translateY(6px);} to{opacity:1; transform:translateY(0);} }

.wl-result-slot{ width:100%; min-height:2px; }

/* ---------- Loading ---------- */
.wl-loading{
  width:100%; background:#fff; border-radius:18px; padding:30px 24px; text-align:center;
  border:1px solid rgba(18,55,42,0.08); box-shadow:0 6px 20px rgba(18,55,42,0.05);
  animation:wl-fade-in 0.3s ease;
}
.wl-scanner{
  width:56px; height:56px; border-radius:16px; margin:0 auto 14px; background:var(--sage);
  color:var(--emerald); display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;
}
.wl-scanner-bar{
  position:absolute; left:0; right:0; height:2px; background:var(--emerald);
  animation:wl-scan 1.3s ease-in-out infinite;
}
@keyframes wl-scan{ 0%{ top:6px; } 50%{ top:44px; } 100%{ top:6px; } }
.wl-loading-title{ font-weight:700; color:var(--deep-forest); margin-bottom:4px; }
.wl-loading-sub{ color:var(--muted-green); font-size:0.9rem; }
@media (prefers-reduced-motion: reduce){ .wl-scanner-bar{ animation:none; top:24px; } }

/* ---------- Result preview (home) ---------- */
.wl-result-preview{
  width:100%; background:#fff; border-radius:18px; padding:22px;
  border:1px solid rgba(18,55,42,0.08); box-shadow:0 10px 26px rgba(18,55,42,0.07);
  animation:wl-fade-in 0.4s ease;
}
.wl-result-preview-header{
  display:flex; align-items:center; gap:7px; color:var(--emerald);
  font-weight:700; font-size:0.85rem; margin-bottom:14px;
}
.wl-result-preview-body{ display:flex; justify-content:space-between; align-items:flex-end; gap:16px; margin-bottom:18px; flex-wrap:wrap; }
.wl-result-name{ font-size:1.3rem; font-weight:800; color:var(--deep-forest); }
.wl-result-sci{ color:var(--muted-green); font-style:italic; font-size:0.9rem; margin:2px 0 10px; }
.wl-result-preview-confidence{ text-align:right; }
.wl-result-preview-confidence-value{ display:block; font-size:1.6rem; font-weight:800; color:var(--emerald); }
.wl-result-preview-confidence-label{ display:block; font-size:0.76rem; color:var(--muted-green); }

/* ---------- Status badge ---------- */
.wl-status-badge{
  display:inline-flex; align-items:center; gap:6px; font-weight:700;
  padding:6px 12px; border-radius:100px; font-size:0.82rem; border:1px solid;
}
.wl-status-sm{ padding:4px 10px; font-size:0.74rem; }

/* ---------- Awareness ---------- */
.wl-awareness{ padding:16px 20px 70px; }
.wl-awareness-inner{
  max-width:640px; margin:0 auto; text-align:center; padding:40px 30px; border-radius:22px;
  background:linear-gradient(135deg, var(--sage), #F1F7EE);
  border:1px solid rgba(18,55,42,0.06);
  color:var(--deep-forest);
}
.wl-awareness-inner svg{ color:var(--emerald); margin-bottom:12px; }
.wl-awareness-inner h2{ font-size:1.35rem; font-weight:700; margin-bottom:8px; }
.wl-awareness-inner p{ color:var(--muted-green); font-size:0.96rem; }

/* ---------- Generic page ---------- */
.wl-page{ padding:60px 20px 90px; }
.wl-page-inner{ max-width:900px; margin:0 auto; }
.wl-page-title{ font-size:clamp(1.9rem, 3.6vw, 2.6rem); font-weight:800; letter-spacing:-0.02em; margin-bottom:14px; }
.wl-page-lede{ color:var(--muted-green); font-size:1.02rem; max-width:620px; line-height:1.6; margin-bottom:20px; }
.wl-page-content{ margin-top:34px; }

/* ---------- Empty state ---------- */
.wl-empty-state{
  margin-top:40px; text-align:center; background:#fff; border-radius:20px;
  padding:60px 30px; border:1px solid rgba(18,55,42,0.07); box-shadow:0 8px 22px rgba(18,55,42,0.05);
}
.wl-empty-icon{
  width:56px; height:56px; border-radius:16px; background:var(--sage); color:var(--emerald);
  display:flex; align-items:center; justify-content:center; margin:0 auto 16px;
}
.wl-empty-title{ font-weight:700; font-size:1.1rem; color:var(--deep-forest); margin-bottom:6px; }
.wl-empty-sub{ color:var(--muted-green); margin-bottom:22px; }

/* ---------- Result card (results page) ---------- */
.wl-result-card{
  background:#fff; border-radius:24px; overflow:hidden;
  border:1px solid rgba(18,55,42,0.07); box-shadow:0 16px 40px rgba(18,55,42,0.08);
  display:grid; grid-template-columns:1fr; animation:wl-fade-in 0.4s ease;
}
@media(min-width:860px){ .wl-result-card{ grid-template-columns:0.85fr 1.15fr; } }
.wl-result-card-media{ background:var(--sage); min-height:260px; }
.wl-result-card-media img{ width:100%; height:100%; object-fit:cover; display:block; }
.wl-result-card-body{ padding:32px; display:flex; flex-direction:column; gap:20px; }
.wl-result-card-top{ display:flex; justify-content:space-between; align-items:flex-start; gap:16px; flex-wrap:wrap; }
.wl-result-card-name{ font-size:1.7rem; font-weight:800; color:var(--deep-forest); }
.wl-result-card-sci{ font-style:italic; color:var(--muted-green); }
.wl-field-label{ font-size:0.74rem; font-weight:700; color:var(--muted-green); margin-bottom:4px; }
.wl-result-card-grid{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.wl-result-card-text{ font-weight:600; color:var(--deep-forest); }
.wl-result-card-desc{ color:var(--deep-forest); line-height:1.65; }

.wl-ring{ position:relative; width:120px; height:120px; flex-shrink:0; }
.wl-ring-label{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.wl-ring-value{ font-size:1.3rem; font-weight:800; color:var(--emerald); }
.wl-ring-caption{ font-size:0.68rem; color:var(--muted-green); }

/* ---------- About page ---------- */
.wl-card-grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:18px; margin-top:14px; }
.wl-info-card{
  background:#fff; border:1px solid rgba(18,55,42,0.07); border-radius:18px; padding:24px;
  transition:transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.wl-info-card:hover{ transform:translateY(-4px); box-shadow:0 14px 28px rgba(18,55,42,0.08); border-color:rgba(25,135,84,0.28); }
.wl-info-card-icon{
  width:42px; height:42px; border-radius:12px; background:var(--sage); color:var(--emerald);
  display:flex; align-items:center; justify-content:center; margin-bottom:14px;
}
.wl-info-card h3{ font-size:1.05rem; margin-bottom:8px; color:var(--deep-forest); }
.wl-info-card p{ color:var(--muted-green); font-size:0.92rem; line-height:1.55; }

.wl-stats-row{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:16px; margin-top:34px;
  padding-top:30px; border-top:1px solid rgba(18,55,42,0.08);
}
.wl-stat-value{ font-size:2rem; font-weight:800; color:var(--emerald); }
.wl-stat-label{ color:var(--muted-green); font-size:0.86rem; margin-top:2px; }

/* ---------- How it works ---------- */
.wl-steps{ margin-top:36px; display:grid; grid-template-columns:1fr; gap:18px; position:relative; }
@media(min-width:860px){
  .wl-steps{ grid-template-columns:repeat(3,1fr); gap:0; }
  .wl-steps::before{
    content:""; position:absolute; top:60px; left:12%; right:12%; height:1px;
    background:rgba(18,55,42,0.12);
  }
}
.wl-step-card{
  background:#fff; border:1px solid rgba(18,55,42,0.07); border-radius:18px; padding:26px;
  position:relative; z-index:1; margin:0 8px;
  transition:transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.wl-step-card:hover{ transform:translateY(-5px); box-shadow:0 16px 30px rgba(18,55,42,0.09); border-color:rgba(25,135,84,0.3); }
.wl-step-num{ font-size:0.82rem; font-weight:800; color:var(--lime); }
.wl-step-icon{
  width:46px; height:46px; border-radius:14px; background:var(--sage); color:var(--emerald);
  display:flex; align-items:center; justify-content:center; margin:12px 0 14px;
  transition:transform 0.25s ease;
}
.wl-step-card:hover .wl-step-icon{ transform:scale(1.08) rotate(-4deg); }
.wl-step-card h3{ font-size:1.08rem; margin-bottom:6px; }
.wl-step-card p{ color:var(--muted-green); font-size:0.92rem; line-height:1.5; }

/* ---------- Contact ---------- */
.wl-contact-grid{ display:grid; grid-template-columns:1fr; gap:24px; margin-top:30px; }
@media(min-width:860px){ .wl-contact-grid{ grid-template-columns:1.3fr 1fr; } }
.wl-form{
  background:#fff; border-radius:20px; padding:28px; border:1px solid rgba(18,55,42,0.07);
  box-shadow:0 10px 26px rgba(18,55,42,0.05); display:flex; flex-direction:column; gap:16px;
}
.wl-field{ display:flex; flex-direction:column; gap:6px; font-size:0.86rem; font-weight:700; color:var(--deep-forest); }
.wl-field input, .wl-field textarea{
  border:1px solid rgba(18,55,42,0.16); border-radius:10px; padding:11px 13px; font-size:0.94rem;
  font-family:inherit; color:var(--deep-forest); background:var(--off-white); resize:vertical;
  transition:border-color 0.2s ease, background 0.2s ease;
}
.wl-field input:focus, .wl-field textarea:focus{ border-color:var(--emerald); background:#fff; outline:none; }

.wl-contact-cards{ display:flex; flex-direction:column; gap:14px; }
.wl-contact-card{
  display:flex; gap:12px; align-items:flex-start; background:#fff; border-radius:16px; padding:18px;
  border:1px solid rgba(18,55,42,0.07); color:var(--emerald);
}
.wl-contact-card-title{ font-weight:700; color:var(--deep-forest); font-size:0.92rem; }
.wl-contact-card-text{ color:var(--muted-green); font-size:0.86rem; margin-top:2px; }

/* ---------- Toast ---------- */
.wl-toast-wrap{ position:fixed; bottom:22px; left:0; right:0; display:flex; justify-content:center; z-index:100; padding:0 16px; pointer-events:none; }
.wl-toast{
  pointer-events:auto; display:flex; align-items:center; gap:10px;
  background:var(--deep-forest); color:#fff; padding:13px 16px; border-radius:14px;
  box-shadow:0 14px 34px rgba(11,36,27,0.35); font-size:0.9rem; font-weight:600;
  animation:wl-toast-in 0.28s ease;
  max-width:92vw;
}
.wl-toast-error{ background:#7A2410; }
.wl-toast-close{ background:none; border:none; color:#fff; opacity:0.75; display:flex; margin-left:4px; }
.wl-toast-close:hover{ opacity:1; }
@keyframes wl-toast-in{ from{ opacity:0; transform:translateY(12px); } to{ opacity:1; transform:translateY(0); } }
@media (prefers-reduced-motion: reduce){ .wl-toast{ animation:none; } }

/* ---------- Footer ---------- */
.wl-footer{ background:var(--dark-evergreen); color:#fff; margin-top:auto; }
.wl-footer-inner{
  max-width:1180px; margin:0 auto; padding:44px 24px 26px;
  display:flex; flex-wrap:wrap; justify-content:space-between; gap:28px;
}
.wl-footer-brand{ display:flex; gap:12px; max-width:340px; }
.wl-footer-name{ font-weight:800; font-size:1.05rem; }
.wl-footer-desc{ color:#B7C9BF; font-size:0.86rem; margin-top:4px; line-height:1.5; }
.wl-footer-links{ list-style:none; display:flex; flex-wrap:wrap; gap:6px 22px; margin:0; padding:0; align-self:center; }
.wl-footer-links button{ background:none; border:none; color:#DCE7DF; font-size:0.88rem; font-weight:600; position:relative; padding:2px 0; }
.wl-footer-links button::after{ content:""; position:absolute; left:0; bottom:-2px; width:0; height:1px; background:var(--lime); transition:width 0.2s ease; }
.wl-footer-links button:hover{ color:var(--lime); }
.wl-footer-links button:hover::after{ width:100%; }
.wl-footer-bottom{
  border-top:1px solid rgba(255,255,255,0.09); text-align:center;
  padding:16px; color:#8FA79A; font-size:0.78rem;
}

/* ---------- Responsive ---------- */
@media(max-width:860px){
  .wl-nav-links{ display:none; }
  .wl-nav-toggle{ display:flex; }
  .wl-hero-deco{ opacity:0.4; width:280px; height:280px; }
}
@media(max-width:600px){
  .wl-result-card-grid{ grid-template-columns:1fr; }
  .wl-preview-actions{ flex-direction:column; }
}
`;
