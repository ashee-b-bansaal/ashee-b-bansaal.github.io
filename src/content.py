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
    "leadership": "Leading &amp; giving back",
    "honors": "Honors &amp; awards",
    "hobbies": "When I’m not coding",
    "skills": "Toolbox",
}

# Lines from your own poems, used as small epigraphs. Replace these.
EPIGRAPHS = {  # add a line from your poems here to show it under that section's heading, e.g. "hobbies": "…"
}

EXPERIENCE = [
    dict(logo="ICTA", role="Co-Founder", org="I Can’t Tell Anyone",
         when="Summer 2026 – Present", where="", now=True,  # EDIT: add a location if you want one
         text="Co-founded a privacy-first AI social platform built for meaningful conversations and fewer harmful interactions. Built real-time WebSocket infrastructure supporting 5,000+ data streams and brought AI safety inference under 25 ms.",
         tags=["Next.js", "FastAPI", "WebSockets", "PyTorch", "NVIDIA Triton", "Llama 3.2"]),
    dict(logo="TA", logo_img="logos/cornell.svg", role="Teaching Assistant", org="Cornell University · CS 5780: Introduction to Machine Learning",
         when="Fall 2026", where="Ithaca, NY", now=True,
         text="Hold weekly office hours to help students work through machine learning concepts and assignments, and grade homework and exams. About 10 hours a week.",
         tags=["Machine Learning", "Office Hours", "Grading"]),
    dict(logo="CMU", logo_img="logos/cmu.png", logo_tile=True, venue="Submitting to CVPR’27", role="ML Research Intern", org="Carnegie Mellon University · Semantic Signals Lab", link="https://semanticsignals.com/",
         when="Jun 2026 – Aug 2026", where="Pittsburgh, PA", now=False,
         text="Developed AI visual memory systems for tracking objects across long-form video. Built DINOv2-based identity matching and CUDA/PyTorch GPU pipelines, processing 3,700+ targets in 283 seconds.",
         tags=["Python", "PyTorch", "CUDA", "DINOv2", "Sinkhorn Optimal Transport", "Computer Vision"]),
    dict(logo="C", role="Founder &amp; ML Engineer", org="Cognify",
         when="Aug 2025 – Present", where="Ithaca, NY", now=True,
         text="Building a hands-free brain-computer interface powered by EEG signals. Developed Conv-LSTM attention models achieving 93% classification accuracy and reduced model iteration time from 5 to 2 days.",
         tags=["Python", "PyTorch", "EEGNet", "Conv-LSTM", "Docker", "Kubernetes", "Optuna"]),
    dict(logo="Sci-Fi", logo_img="logos/cornell.svg", venue="Submitted to CHI’27 (FaceSign)", role="Machine Learning Intern", org="Cornell University · Sci-Fi Lab", link="https://www.scifilab.org/",
         when="Jun 2025 – Aug 2025", where="Ithaca, NY", now=False,
         text="Developed multimodal deep learning models for wearable gesture recognition. Trained Conformer-CTC models on 6,000+ sequences, achieving 98.9% gesture accuracy.",
         tags=["Python", "PyTorch", "Conformer-CTC", "Multimodal Learning", "Acoustic Sensing", "IMU"]),
    dict(logo="INFO", logo_img="logos/cornell.svg", role="Course Developer", org="Cornell University · INFO 3450: Human-Computer Interaction Design",
         when="Jan 2025 – Jun 2025", where="Ithaca, NY", now=False,
         text="Co-authored HTML/CSS/JavaScript coding assignments with starter code, reference solutions, and grading rubrics. Benchmarked 30+ AI tools and 15+ peer courses to design 8+ Human–AI Interaction and UI/UX modules for ~100 students.",
         tags=["HTML", "CSS", "JavaScript", "UI/UX", "Human–AI Interaction", "Curriculum Design"]),
    dict(logo="cult", logo_img="logos/cultfit.png", logo_tile=True, role="Software Engineer Intern", org="Cult.fit · Android &amp; Backend",
         when="May 2024 – Jul 2024", where="Bengaluru, India", now=False,  # EDIT: confirm location
         text="Developed wearable integrations and backend systems for a fitness app with 150K monthly users. Built fault-tolerant pipelines processing 500K+ daily events and reduced database query latency by 60%.",
         tags=["Kotlin", "Java", "Android", "Health Connect", "SQLite", "Coroutines", "Firebase", "BigQuery"]),
]

# ── LEADERSHIP & SERVICE ─────────────────────────────────────────────────────
#  Same fields as EXPERIENCE. SERVICE is the short list underneath.
LEADERSHIP = [
    dict(logo="XR", logo_img="logos/cuxr.png", logo_tile=True, role="BCI Sub-team Lead", org="Cornell Extended Reality Project Team",
         when="Jan 2025 – Present", where="Ithaca, NY", now=True,
         text="Lead a team of six: GitHub Actions CI, code review, and sprint planning, which cut integration bugs by 40%. See the BCI project above.",
         tags=["Leadership", "CI/CD", "Python"]),
    dict(logo="IEEE", role="Corporate E-Board", org="IEEE · Cornell University",
         when="Jan 2025 – Jan 2026", where="Ithaca, NY", now=False,
         text="",  # EDIT: one line on what you did, e.g. sponsors you brought in or events you ran
         tags=[]),
]

SERVICE = [  # (role, what it involved)
    ("External Reviewer, CHI 2026", "Reviewing submissions in sensing and interaction systems."),
    ("Invited Panelist, ACSU Undergraduate Research Panel", "Discussing undergraduate research experiences and pathways."),
]

# ── HONORS & AWARDS ──────────────────────────────────────────────────────────
HONORS = [  # amount = the big figure on the card
    dict(title="Bowers Undergraduate Research Experience (BURE) Scholarship", org="Cornell University", amount="$7,000",
         text="Research stipend, plus continued support through the BURE Academic Year Expansion Program."),
    dict(title="Summer Experiential Grant", org="Cornell University", amount="$6,000",
         text="Awarded to support summer research in 2026."),
    dict(title="Foreign Student Scholarship", org="Cornell University", amount="~$100K / yr",
         text="Institutional support of about $100,000 per year."),
    dict(title="Meritorious Student Scholarship", org="Government of India", amount="$1,500",
         text="Awarded for achieving <strong>All India Rank 1</strong> in the national secondary school examinations."),
]

# ── PROJECTS ─────────────────────────────────────────────────────────────────
#  Shown as cards, 3 per row, in this order. To add a project, copy one whole
#  dict(...) block, paste it where you want it, and change the text.
#
#    name      the big title
#    subtitle  one line under the title
#    venue     e.g. "Submitted to CHI’27" ("" = none)
#    link      where the title and image go when clicked ("" = not clickable)
#    image     a screenshot / photo in photos/  ("" = coloured placeholder)
#    fit       "contain" shows the whole image (best for app screenshots),
#              "cover" fills the box and crops (best for photos)
#    focus     with "cover": which part to keep, e.g. "50% 20%" = keep the top
#    text      the paragraph
#    tags      the skill chips, e.g. ["Python", "PyTorch"]
#    details   extra lines under the tags, as ("Label", "value") pairs, e.g. ("Team", "…")
#    buttons   small link buttons at the bottom, as ("Label", "url") pairs
PROJECTS = [
    dict(
        name="Select-or-Sign",
        venue="Submitting to CSCW’27",
        subtitle="AI-Powered AR Communication Interface",
        link="#",
        image="photos/ar-cafe-conversation-interface.png",
        fit="cover", focus="75% 62%",
        text="An AR interface enabling real-time communication between Deaf, hard-of-hearing, and hearing users. Built a 7-task asynchronous AI pipeline with sub-second latency and 95%+ gesture recognition accuracy.",
        tags=["Python", "Asyncio", "TensorFlow Lite", "On-Device ML", "MediaPipe", "Computer Vision", "Whisper ASR", "GPT-4o-mini", "Azure TTS", "Real-Time Systems"],
        details=[("Team", "Co-built with another developer")],
        buttons=[("GitHub", "https://github.com/ashee-b-bansaal/Select-or-Sign-AI-powered-AR-glass-interface-.git"), ("Poster", "https://yourimageshare.com/ib/TU3qqC6SM9.png"), ("Demo Video", "https://youtu.be/lZsJfs5ApfI?si=pSJ_sRxYps5A_zno")],
    ),
    dict(
        name="I Can’t Tell Anyone",
        venue="",
        subtitle="Privacy-First AI Social Platform",
        link="#",
        image="photos/i-cant-tell-anyone.jpg",
        fit="cover",
        text="A social platform designed to encourage meaningful conversations and reduce harmful interactions. Built a real-time WebSocket infrastructure supporting 5,000+ data streams and optimized AI safety inference to under 25 ms.",
        tags=["React", "Next.js", "Python", "FastAPI", "WebSockets", "PyTorch", "ONNX", "INT8 Quantization", "NVIDIA Triton", "LLM Inference", "Llama 3.2", "Docker"],
        details=[("Team", "Co-built with another developer")],
        buttons=[("Demo Video", "https://youtu.be/d6EKJWPPSjk")],
        focus="50% 50%",
    ),
    dict(
        name="CalibraType",
        venue="Submitting to IUI’27",
        subtitle="Real-world Adaptive Mobile Keyboard",
        link="#",
        image="photos/calibratype.jpg",
        fit="cover",
        text="An iOS keyboard that automatically adapts to how users type. Built a C++ probabilistic learning engine that continuously adjusts touch predictions, reducing typing errors by 28%.",
        tags=["C++", "Swift", "iOS", "UIKit", "Online Learning", "Probabilistic Modeling", "On-Device ML"],
        details=[("Team", "Co-building with 2 other developers")],
        buttons=[("GitHub", "https://github.com/JimmyChen02/ios-typing-data-collector")],
        focus="50% 50%",
    ),
    dict(
        name="FaceSign",
        venue="Submitted to CHI’27",
        subtitle="Multimodal AR Sign Language Recognition",
        link="https://kommodo.ai/i/aLtOEzaXE31cF5kimyjV",
        image="photos/facesign.jpg",
        fit="cover",
        text="A smart-glasses system that recognizes sign language gestures and facial expressions. Developed a multimodal Conformer-CTC model combining acoustic and motion sensors, achieving 98.9% gesture accuracy and 97.4% facial-expression F1.",
        tags=["Python", "PyTorch", "Conformer-CTC", "CNNs", "Multimodal Learning", "Multitask Learning", "Sensor Fusion", "Signal Processing", "Acoustic Sensing", "IMU"],
        details=[],
        buttons=[("Demo Video", "https://youtu.be/iAjPd3CNK30"), ("Concept", "https://yourimageshare.com/ib/ulscpG3rD8.png")],
        focus="50% 50%",
    ),
    dict(
        name="Legal Eagle",
        venue="",
        subtitle="Multi-Agent Legal Podcast Generator",
        link="#",
        image="photos/legal-eagle.jpg",
        fit="cover",
        text="An AI platform that transforms complex legal documents into conversational podcasts. Built a multi-agent RAG pipeline that reduced hallucinations by 35% and LLM token costs by 98.5%.",
        tags=["Python", "LangGraph", "Multi-Agent Systems", "RAG", "Pinecone", "Vector Search", "LLMs", "LLM Evaluation", "Redis", "JavaScript"],
        details=[("Team", "Co-built with another developer")],
        buttons=[("Demo Video", "https://youtu.be/ReSZEn3ARvg")],
        focus="50% 50%",
    ),
    dict(
        name="VR-BCI Navigation (CUXR)",
        venue="",
        subtitle="Live EEG inference for extended reality",
        link="#",
        image="photos/cuxr-bci.jpg",
        fit="cover", focus="50% 22%",
        text="Our sub-team streams EEG at 256 Hz into a real-time inference pipeline built on FFT spectral features (82% accuracy across 20+ users), so XR experiences can respond to the person wearing the headset. I lead six engineers and set up our CI, code review, and sprint process, which cut integration bugs by 40%.",
        tags=["Python", "scikit-learn", "PyTorch", "EEGNet", "SciPy", "NumPy", "Signal Processing", "Common Spatial Patterns (CSP)", "Real-Time ML Inference", "WebSockets", "Unity", "Meta Quest", "GitHub Actions"],
        details=[("Team", "Sub-team lead · 6 engineers")],
        buttons=[("GitHub", "https://github.com/CUXR/BCI-VR-Navigation.git"), ("Demo Video 1", "https://www.youtube.com/watch?v=tk2hOVV74W4"), ("Demo Video 2", "https://www.youtube.com/watch?v=xWrw_kHVDX8")],
    ),
    dict(
        name="Spatial Moves",
        venue="",
        subtitle="Interactive Personalized Learning Graphs",
        link="#",
        image="photos/spatial-moves.jpg",
        fit="cover",
        text="A web platform that visualizes personalized learning paths as interactive knowledge graphs. Built React/D3.js visualizations and vector-search services supporting 100+ adaptive learning nodes.",
        tags=["React", "TypeScript", "D3.js", "Node.js", "Python", "FAISS", "Pinecone", "Vector Search", "Neo4j", "Graph Databases", "Data Visualization"],
        details=[],
        buttons=[("GitHub", "#")],
        focus="50% 50%",
    ),
    dict(
        name="AirDrum Duel",
        venue="",
        subtitle="Real-Time Embedded Rhythm Game",
        link="https://pages.github.coecis.cornell.edu/ece3140-spr2026/ab3235-svo8/",
        image="photos/airdrum-duel.jpg",
        fit="cover",
        text="A two-player rhythm game that turns mid-air gestures into virtual drum beats using motion-sensing microcontrollers. Built a 6-stage concurrent embedded pipeline with IMU gesture classification, earliest-deadline-first scheduling, and 10 ms sensor sampling for responsive gameplay.",
        tags=["Embedded C", "ARM Assembly", "ARM Cortex-M0+", "FRDM-KL46Z", "Real-Time Scheduling (EDF)", "Concurrency", "Interrupt Handling", "IMU Sensors", "UART", "Hardware Timers"],
        details=[("Team", "Co-built with another developer")],
        buttons=[("Demo Video", "https://youtu.be/6LhgXgnIcNo"), ("GitHub", "https://pages.github.coecis.cornell.edu/ece3140-spr2026/ab3235-svo8/")],
        focus="0% 0%",
    ),
]

HOBBIES = [  # note = the little hand-written sticker on the card
    dict(id="poetry", title="Poetry", icon="quill", note="100 poems, one book",
         text="I write poems, enough of them that they became a book: <em>Silent Voices, Loud Whispers</em>, 100 poems for the journey within.",
         link=("Read the Book", "https://www.amazon.com/dp/8119483065"), tint="peach"),
    dict(id="music", title="Music", icon="drum", note="5-year classical degree in keys",
         text="I play keyboard, flute and guitar, and this summer I picked up the drums. Keyboard is where it all started: I studied it classically for five years and hold a degree in it.", link=None, tint="mint"),
    dict(id="photo", title="Photography", icon="camera", note="always carrying a camera",
         text="I take a lot of photos. A few of them ended up on this site.", link=None, tint="sky"),
]

SKILLS = [  # (group name, [skills]); each skill shows as a chip with its logo (logos live in icons/)
    ("Languages", ["Python", "C", "C++", "Java", "Go", "Kotlin", "Swift", "JavaScript", "TypeScript", "SQL", "Rust", "Solidity", "Ruby", "R", "MATLAB", "Bash", "HTML", "CSS"]),
    ("AI / ML", ["PyTorch", "TensorFlow", "Keras", "CUDA", "NVIDIA Triton", "scikit-learn", "Hugging Face", "LangChain", "LangGraph", "OpenCV", "Pandas", "NumPy", "Matplotlib"]),
    ("Web & Backend", ["React", "Next.js", "Node.js", "Express", "Tailwind", "FastAPI", "Flask", "Django", "Spring Boot", "REST", "gRPC", "Selenium"]),
    ("Data & Databases", ["PostgreSQL", "MySQL", "SQLite", "SQL Server", "MongoDB", "Redis", "Neo4j", "Supabase", "Firebase", "BigQuery", "Snowflake", "DuckDB", "Kafka"]),
    ("Cloud & DevOps", ["AWS", "GCP", "Azure", "Docker", "Kubernetes", "Linux", "Git", "GitHub Actions", "Grafana", "ROS"]),
    ("Everyday Tools", ["Claude Code", "Cursor", "Postman", "Pytest", "Jira", "Trello", "Excel"]),
]
EDU = "<em>Cornell University</em>, B.S. Computer Science (Honors) · Minor in ECE · GPA 3.85 · May 2028"

ICONS = {
    "quill": '<svg viewBox="0 0 32 32"><path d="M26 4C16 6 9 13 7 25M7 25l-2 3M26 4c-1 7-6 12-13 14M12 13h7M10 18h6"/></svg>',
    "flute": '<svg viewBox="0 0 32 32"><path d="M4 22L26 8l2 3L6 25z"/><circle cx="12" cy="18.3" r="1"/><circle cx="16" cy="15.8" r="1"/><circle cx="20" cy="13.3" r="1"/></svg>',
    "keys": '<svg viewBox="0 0 32 32"><rect x="3" y="8" width="26" height="16" rx="1.5"/><path d="M8.2 8v16M13.4 8v16M18.6 8v16M23.8 8v16"/><path d="M6.6 8v9h3.2V8M11.8 8v9h3.2V8M22.2 8v9h3.2V8" class="f"/></svg>',
    "drum": '<svg viewBox="0 0 32 32"><ellipse cx="16" cy="13" rx="11" ry="4"/><path d="M5 13v8c0 2.2 4.9 4 11 4s11-1.8 11-4v-8M9 16.5l3 7.5M23 16.5l-3 7.5M16 17v8"/><path d="M22 4l-6 7M26 6l-8 6"/></svg>',
    "guitar": '<svg viewBox="0 0 32 32"><path d="M19 13l8-8M25 3l4 4"/><path d="M17.5 11.5c-2-1-4.5-.6-5.6 1.2-.6 1-1.8 1.4-3 1.6C6 14.7 4 16.8 4 19.8 4 24.9 7.1 28 12.2 28c3 0 5.1-2 5.5-4.9.2-1.2.6-2.4 1.6-3 1.8-1.1 2.2-3.6 1.2-5.6"/><circle cx="12.5" cy="19.5" r="2"/><path d="M9 21l3 3"/></svg>',
    "camera": '<svg viewBox="0 0 32 32"><rect x="4" y="9" width="24" height="17" rx="2.5"/><path d="M11 9l2-3h6l2 3"/><circle cx="16" cy="17.5" r="5"/></svg>',
}
