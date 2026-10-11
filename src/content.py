# ─────────────────────────────────────────────────────────────────────────────
#  ALL THE TEXT ON THE SITE LIVES IN THIS FILE.
#
#  How to edit:
#    Easiest: run  python3 src/editor.py  and edit right on the page in your browser.
#    Or edit this file: run  python3 src/build.py --watch  once, then save + refresh.
#
#  Tips:
#    • Keep the quotes "…" around text, and the comma after each item.
#    • Plain characters are fine: & < > are handled for you… except write <em>…</em>
#      or <strong>…</strong> if you want italics / bold.
#    • Use "#" as a link while you don't have the real URL yet.
#    • Images go in the  photos/  folder and are written as "photos/name.jpg".
# ─────────────────────────────────────────────────────────────────────────────

NAME = "Ashee B Bansaal"
EMAIL = "ab3235@cornell.edu"
GITHUB = "https://github.com/ashee-b-bansaal"
LINKEDIN = "https://linkedin.com/in/ashee-b-bansaal"
TAGLINE = "Software &amp; ML Engineering · CS @ Cornell"

ABOUT_HEAD = "Hi, I'm Ashee."
ABOUT = [
    "I'm a Computer Science (Honors) undergraduate at Cornell University, minoring in Electrical and Computer Engineering. I'm passionate about software engineering, machine learning, and building intelligent systems that solve real-world problems. My interests span scalable software systems, applied AI, computer vision, and ML-driven applications, with a particular focus on turning complex ideas into practical, reliable technology.",
    "I enjoy working across the stack—from designing backend systems and optimizing ML pipelines to building applications that people can actually use.",
]
SEEKING = "Looking for <strong>Summer 2027</strong> SWE and ML internships."

# Big headings above each section
TITLES = {
    "experience": "Where I’ve worked",
    "projects": "Projects Build Log",
    "hobbies": "When I’m not coding",
    "skills": "Toolbox",
}

# Lines from your own poems, used as small epigraphs. Replace these.
EPIGRAPHS = {
    "about": "[a line from one of your poems]",
    "projects": "",
    "hobbies": "[a line from your book]",
}

EXPERIENCE = [
    dict(logo="CMU", logo_img="logos/cmu.png", logo_tile=True, role="ML Research Intern", org="Carnegie Mellon University · Semantic Signal Lab",
         when="Jun 2026 – Aug 2026", where="Pittsburgh, PA", now=False,
         text="Developed AI visual memory systems for tracking objects across long-form video. Built DINOv2-based identity matching and CUDA/PyTorch GPU pipelines, processing 3,700+ targets in 283 seconds.",
         tags=["Python", "PyTorch", "CUDA", "DINOv2", "Sinkhorn Optimal Transport", "Computer Vision"]),
    dict(logo="C", role="Founder &amp; ML Engineer", org="Cognify",
         when="Aug 2025 – Present", where="Ithaca, NY", now=True,
         text="Building a hands-free brain-computer interface powered by EEG signals. Developed Conv-LSTM attention models achieving 93% classification accuracy and reduced model iteration time from 5 to 2 days.",
         tags=["Python", "PyTorch", "EEGNet", "Conv-LSTM", "Docker", "Kubernetes", "Optuna"]),
    dict(logo="Sci-Fi", logo_img="logos/cornell.svg", role="Machine Learning Intern", org="Cornell University · Sci-Fi Lab",
         when="Jun 2025 – Aug 2025", where="Ithaca, NY", now=False,
         text="Developed multimodal deep learning models for wearable gesture recognition. Trained Conformer-CTC models on 6,000+ sequences, achieving 98.9% gesture accuracy.",
         tags=["Python", "PyTorch", "Conformer-CTC", "Multimodal Learning", "Acoustic Sensing", "IMU"]),
    dict(logo="cult", logo_img="logos/cultfit.png", logo_tile=True, role="Software Engineer Intern", org="Cult.fit · Android &amp; Backend",
         when="May 2024 – Jul 2024", where="Bengaluru, India", now=False,  # EDIT: confirm location
         text="Developed wearable integrations and backend systems for a fitness app with 150K monthly users. Built fault-tolerant pipelines processing 500K+ daily events and reduced database query latency by 60%.",
         tags=["Kotlin", "Java", "Android", "Health Connect", "SQLite", "Coroutines", "Firebase", "BigQuery"]),
    dict(logo="XR", logo_img="logos/cuxr.png", logo_tile=True, role="BCI Sub-team Lead", org="Cornell Extended Reality Project Team",
         when="Jan 2025 – Present", where="Ithaca, NY", now=True,
         text="Lead a team of six: GitHub Actions CI, code review, and sprint planning, which cut integration bugs by 40%. See the BCI project below.",
         tags=["Leadership", "CI/CD", "Python"]),
]

# ── PROJECTS ─────────────────────────────────────────────────────────────────
#  Shown as cards, 3 per row, in this order. To add a project, copy one whole
#  dict(...) block, paste it where you want it, and change the text.
#
#    name      the big title
#    subtitle  one line under the title
#    link      where the title and image go when clicked ("" = not clickable)
#    image     a screenshot / photo in photos/  ("" = coloured placeholder)
#    fit       "contain" shows the whole image (best for app screenshots),
#              "cover" fills the box and crops (best for photos)
#    focus     with "cover": which part to keep, e.g. "50% 20%" = keep the top
#    text      the paragraph
#    details   bold lines under the paragraph, as ("Label", "value") pairs
#    buttons   small link buttons at the bottom, as ("Label", "url") pairs
PROJECTS = [
    dict(
        name="Select-or-Sign",
        subtitle="AI-Powered AR Communication Interface",
        link="#",
        image="photos/ar-cafe-conversation-interface.png",
        fit="cover", focus="75% 62%",
        text="An AR interface enabling real-time communication between Deaf, hard-of-hearing, and hearing users. Built a 7-task asynchronous AI pipeline with sub-second latency and 95%+ gesture recognition accuracy.",
        details=[("Tech Stack", "Python, Asyncio, TensorFlow Lite, MediaPipe, Whisper, GPT-4o-mini, Azure TTS")],
        buttons=[("GitHub", "https://github.com/ashee-b-bansaal/Select-or-Sign-AI-powered-AR-glass-interface-.git"), ("Poster", "https://yourimageshare.com/ib/TU3qqC6SM9.png"), ("Demo Video", "https://youtu.be/lZsJfs5ApfI?si=pSJ_sRxYps5A_zno")],
    ),
    dict(
        name="I Can’t Tell Anyone",
        subtitle="Privacy-First AI Social Platform",
        link="#",
        image="photos/i-cant-tell-anyone.jpg",
        fit="cover",
        text="A social platform designed to encourage meaningful conversations and reduce harmful interactions. Built a real-time WebSocket infrastructure supporting 5,000+ data streams and optimized AI safety inference to under 25 ms.",
        details=[("Tech Stack", "React, Next.js, Python, FastAPI, WebSockets, PyTorch, ONNX, NVIDIA Triton, Docker, Llama 3.2"), ("Team", "Co-built with another developer")],
        buttons=[("Demo Video", "https://youtu.be/d6EKJWPPSjk")],
        focus="50% 50%",
    ),
    dict(
        name="CalibraType",
        subtitle="Real-world Adaptive Mobile Keyboard",
        link="#",
        image="photos/calibratype.jpg",
        fit="cover",
        text="An iOS keyboard that automatically adapts to how users type. Built a C++ probabilistic learning engine that continuously adjusts touch predictions, reducing typing errors by 28%.",
        details=[("Tech Stack", "C++, Swift, iOS, UIKit, Online Learning, Probabilistic Modeling")],
        buttons=[("GitHub", "https://github.com/JimmyChen02/ios-typing-data-collector")],
        focus="50% 50%",
    ),
    dict(
        name="FaceSign",
        subtitle="Multimodal AR Sign Language Recognition",
        link="https://kommodo.ai/i/aLtOEzaXE31cF5kimyjV",
        image="photos/facesign.jpg",
        fit="cover",
        text="A smart-glasses system that recognizes sign language gestures and facial expressions. Developed a multimodal Conformer-CTC model combining acoustic and motion sensors, achieving 98.9% gesture accuracy and 97.4% facial-expression F1.",
        details=[("Tech Stack", "Python, PyTorch, Conformer-CTC, CNNs, Multitask Learning, Acoustic Sensing, IMU")],
        buttons=[("Demo Video", "https://youtu.be/iAjPd3CNK30"), ("Concept", "https://yourimageshare.com/ib/ulscpG3rD8.png")],
        focus="50% 50%",
    ),
    dict(
        name="Legal Eagle",
        subtitle="Multi-Agent Legal Podcast Generator",
        link="#",
        image="photos/legal-eagle.jpg",
        fit="cover",
        text="An AI platform that transforms complex legal documents into conversational podcasts. Built a multi-agent RAG pipeline that reduced hallucinations by 35% and LLM token costs by 98.5%.",
        details=[("Tech Stack", "Python, LangGraph, Pinecone, RAG, LLMs, Redis, JavaScript, HTML/CSS"), ("Team", "Co-built with another developer")],
        buttons=[("Demo Video", "https://youtu.be/ReSZEn3ARvg")],
        focus="50% 50%",
    ),
    dict(
        name="Cornell XR · BCI",
        subtitle="Live EEG inference for extended reality",
        link="#",
        image="photos/xr.jpg",
        fit="cover", focus="50% 22%",
        text="Our sub-team streams EEG at 256 Hz into a real-time inference pipeline built on FFT spectral features (82% accuracy across 20+ users), so XR experiences can respond to the person wearing the headset. I lead six engineers and set up our CI, code review, and sprint process, which cut integration bugs by 40%.",
        details=[("Built With", "Python, FFT features, Streaming"), ("Team", "Sub-team lead · 6 engineers")],
        buttons=[("GitHub", "https://github.com/CUXR/BCI-VR-Navigation.git"), ("Demo Video 1", "https://www.youtube.com/watch?v=tk2hOVV74W4"), ("Demo Video 2", "https://www.youtube.com/watch?v=xWrw_kHVDX8")],
    ),
    dict(
        name="Spatial Moves",
        subtitle="Interactive Personalized Learning Graphs",
        link="#",
        image="",
        fit="contain",
        text="A web platform that visualizes personalized learning paths as interactive knowledge graphs. Built React/D3.js visualizations and vector-search services supporting 100+ adaptive learning nodes.",
        details=[("Tech Stack", "React, TypeScript, D3.js, Python, Node.js, FAISS, Pinecone, Neo4j")],
        buttons=[("GitHub", "#")],
    ),
    dict(
        name="AirDrum Duel",
        subtitle="Real-Time Embedded Rhythm Game",
        link="https://pages.github.coecis.cornell.edu/ece3140-spr2026/ab3235-svo8/",
        image="",
        fit="contain",
        text="A two-player rhythm game that turns mid-air gestures into virtual drum beats using motion-sensing microcontrollers. Built a 6-stage concurrent embedded pipeline with IMU gesture classification, earliest-deadline-first scheduling, and 10 ms sensor sampling for responsive gameplay.",
        details=[("Tech Stack", "Embedded C, FRDM-KL46Z, IMU Sensors, RT Scheduling (EDF), UART, Hardware Timers, Concurrent Programming")],
        buttons=[("Demo Video", "https://youtu.be/6LhgXgnIcNo"), ("GitHub", "https://pages.github.coecis.cornell.edu/ece3140-spr2026/ab3235-svo8/")],
    ),
]

HOBBIES = [
    dict(id="poetry", title="Poetry", icon="quill",
         text="I write poems, enough of them that they became a book: <em>[book title]</em>.",
         link=("Read the Book", "#"), tint="peach"),
    dict(id="flute", title="Flute", icon="flute",
         text="[How long you’ve played, where you play, a favourite piece.]", link=None, tint="mint"),
    dict(id="keys", title="Keyboard", icon="keys",
         text="[What you like to play on keys: pieces, covers, your own stuff.]", link=None, tint="lavender"),
    dict(id="photo", title="Photography", icon="camera",
         text="I take a lot of photos. A few of them ended up on this site.", link=None, tint="sky"),
]

SKILLS = [
    ("Languages", "Python, Java, Kotlin, C/C++, Go, TypeScript, JavaScript, SQL, Swift, Rust, Bash"),
    ("Backend &amp; Data", "REST, gRPC, FastAPI, Flask, PostgreSQL, SQLite, Redis, Neo4j, BigQuery, Firebase"),
    ("ML", "PyTorch, TensorFlow / TFLite, CUDA, FAISS, Pinecone, Optuna"),
    ("Infra &amp; Tools", "AWS, GCP, Docker, Kubernetes, GitHub Actions, Linux, Git"),
]
EDU = "<em>Cornell University</em>, B.S. Computer Science (Honors) · Minor in ECE · GPA 3.85 · May 2028"

ICONS = {
    "quill": '<svg viewBox="0 0 32 32"><path d="M26 4C16 6 9 13 7 25M7 25l-2 3M26 4c-1 7-6 12-13 14M12 13h7M10 18h6"/></svg>',
    "flute": '<svg viewBox="0 0 32 32"><path d="M4 22L26 8l2 3L6 25z"/><circle cx="12" cy="18.3" r="1"/><circle cx="16" cy="15.8" r="1"/><circle cx="20" cy="13.3" r="1"/></svg>',
    "keys": '<svg viewBox="0 0 32 32"><rect x="3" y="8" width="26" height="16" rx="1.5"/><path d="M8.2 8v16M13.4 8v16M18.6 8v16M23.8 8v16"/><path d="M6.6 8v9h3.2V8M11.8 8v9h3.2V8M22.2 8v9h3.2V8" class="f"/></svg>',
    "camera": '<svg viewBox="0 0 32 32"><rect x="4" y="9" width="24" height="17" rx="2.5"/><path d="M11 9l2-3h6l2 3"/><circle cx="16" cy="17.5" r="5"/></svg>',
}
