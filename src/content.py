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
    dict(logo="TA", logo_img="logos/cornell.svg", role="Teaching Assistant", org="Cornell University · CS 5780: Introduction to Machine Learning",
         when="Fall 2026", where="Ithaca, NY", now=True,
         text="Teaching assistant for CS 5780, Cornell’s introduction to machine learning.",
         built=[
             "Hold weekly office hours to help students work through machine learning concepts and assignments.",
             "Grade homework and exams, about 10 hours a week in total.",
         ], built_label="What I do",
         tags=["Machine Learning", "Office Hours", "Grading"]),
    dict(logo="CMU", logo_img="logos/cmu.png", logo_tile=True, venue="Submitting to CVPR’27", role="ML Research Intern", org="Carnegie Mellon University · Semantic Signals Lab", link="https://semanticsignals.com/",
         when="Jun 2026 – Aug 2026", where="Pittsburgh, PA", now=False,
         text="Research on memory for AI glasses: helping an assistant answer questions like “where did I leave my medicine?” from hours of first-person video.",
         built=[
             "Built a gaze-guided visual memory for long egocentric video Q&amp;A: where the wearer looks decides which objects get tracked and described by a vision-language model.",
             "Engineered cross-session identity tracking with DINOv2 embeddings and Sinkhorn optimal transport across 10+ hours of video.",
             "Wrote a CUDA/PyTorch GPU deduplication engine that matches the CPU results exactly, handling 3,700+ targets in 283 seconds.",
         ],
         tags=["Python", "PyTorch", "CUDA", "DINOv2", "Sinkhorn Optimal Transport", "Computer Vision"]),
    dict(logo="ICTA", role="Co-Founder", org="I Can’t Tell Anyone",
         when="Summer 2026 – Present", where="", now=True,  # EDIT: add a location if you want one
         text="A privacy-first AI social platform for honest conversations, with AI moderation that catches harmful messages as they’re sent.",
         built=[
             "Built real-time WebSocket infrastructure supporting 5,000+ concurrent data streams.",
             "Brought AI safety inference under 25 ms by serving Llama 3.2 on NVIDIA Triton.",
             "Shipped the product end to end with a Next.js frontend and FastAPI backend.",
         ],
         tags=["Next.js", "FastAPI", "WebSockets", "PyTorch", "NVIDIA Triton", "Llama 3.2"]),
    dict(logo="C", role="Founder &amp; ML Engineer", org="Cognify",
         when="Aug 2025 – Present", where="Ithaca, NY", now=True,
         text="A hands-free brain-computer interface: EEG signals in, commands out, no hands needed.",
         built=[
             "Designed an SSVEP classifier from Conv-LSTM + attention ensembles, reaching 95.3% accuracy with 40% faster training.",
             "Combined EEGNet and temporal CNNs into a motor-imagery model, raising accuracy to 81.25% (+6%).",
             "Set up MLOps with Optuna, Docker and Kubernetes, cutting model iteration time in half.",
         ],
         tags=["Python", "PyTorch", "EEGNet", "Conv-LSTM", "Docker", "Kubernetes", "Optuna"]),
    dict(logo="Sci-Fi", logo_img="logos/cornell.svg", venue="Submitted to CHI’27 (FaceSign)", role="Machine Learning Intern", org="Cornell University · Sci-Fi Lab", link="https://www.scifilab.org/",
         when="Jun 2025 – Aug 2025", where="Ithaca, NY", now=False,
         text="Gesture and facial-expression recognition for wearables, from sound and motion sensors instead of cameras.",
         built=[
             "Built a PyTorch Conformer-CTC model fusing 4-channel acoustic and 6-axis IMU data across 35 gesture classes.",
             "Trained on 6K sequences with cross-user pretraining, 5-fold personalization and multitask learning.",
             "Reached 98.9% gesture accuracy and 97.4% facial-expression macro-F1, up to 24.4% above CTC baselines.",
         ],
         tags=["Python", "PyTorch", "Conformer-CTC", "Multimodal Learning", "Acoustic Sensing", "IMU"]),
    dict(logo="INFO", logo_img="logos/cornell.svg", role="Course Developer", org="Cornell University · INFO 3450: Human-Computer Interaction Design",
         when="Jan 2025 – Jun 2025", where="Ithaca, NY", now=False,
         text="Helped build Cornell’s INFO 3450 course on Human-Computer Interaction Design, taken by ~100 students.",
         built=[
             "Co-authored HTML/CSS/JavaScript coding assignments with starter code, reference solutions, and grading rubrics.",
             "Benchmarked 30+ AI tools and 15+ peer courses to design 8+ Human–AI Interaction and UI/UX modules.",
         ], built_label="What I did",
         tags=["HTML", "CSS", "JavaScript", "UI/UX", "Human–AI Interaction", "Curriculum Design"]),
    dict(logo="cult", logo_img="logos/cultfit.png", logo_tile=True, role="Software Engineer Intern", org="Cult.fit · Android &amp; Backend",
         when="May 2024 – Jul 2024", where="Bengaluru, India", now=False,  # EDIT: confirm location
         text="Android and backend engineering for a fitness app used by 150K people a month.",
         built=[
             "Shipped Kotlin/Java Health Connect features that sync wearables across 6+ devices.",
             "Built multi-threaded coroutine pipelines with retries and circuit breakers, processing 500K+ daily events at under 100 ms p95.",
             "Cut SQLite latency 60% with WAL tuning, and ran Firebase–BigQuery A/B tests across 50K users that drove 40% adoption.",
         ],
         tags=["Kotlin", "Java", "Android", "Health Connect", "SQLite", "Coroutines", "Firebase", "BigQuery"]),
]

# ── LEADERSHIP & SERVICE ─────────────────────────────────────────────────────
#  Same fields as EXPERIENCE ("when"/"where" can be "" to hide that line).
LEADERSHIP = [
    dict(logo="XR", logo_img="logos/cuxr.png", logo_tile=True, role="BCI Sub-team Lead", org="Cornell Extended Reality Project Team",
         when="Jan 2025 – Present", where="Ithaca, NY", now=True,
         text="Lead a team of six: GitHub Actions CI, code review, and sprint planning, which cut integration bugs by 40%. See the BCI project above.",
         tags=["Leadership", "CI/CD", "Python"]),
    dict(logo="IEEE", role="Corporate E-Board", org="Cornell IEEE",
         when="Jan 2025 – Jan 2026", where="Ithaca, NY", now=False,
         text="Secured partnerships with ~150 companies, including Marvell Technology, to organize Cornell IEEE corporate events.",
         tags=["Partnerships", "Events"]),
    dict(logo="CHI", role="External Reviewer", org="ACM CHI 2026", when="", where="", now=False,
         text="Reviewing submissions in sensing and interaction systems.",
         tags=["Peer Review", "HCI"]),
    dict(logo="ACSU", role="Invited Panelist", org="ACSU Undergraduate Research Panel", when="", where="Ithaca, NY", now=False,
         text="Discussing undergraduate research experiences and pathways.",
         tags=["Mentorship", "Research"]),
]

# ── HONORS & AWARDS ──────────────────────────────────────────────────────────
HONORS = [  # big = the headline figure (it counts up on screen); label = the small line under it
    dict(big="#1", label="All India Rank", title="Meritorious Student Scholarship", org="Government of India",
         text="Awarded $1,500 after achieving <strong>All India Rank 1</strong> in the national secondary school examinations."),
    dict(big="$100K", label="per year", title="Foreign Student Scholarship", org="Cornell University",
         text="About $100,000 a year in institutional support."),
    dict(big="$7,000", label="research stipend", title="Bowers Undergraduate Research Experience (BURE) Scholarship", org="Cornell University",
         text="Selected for continued support through the BURE Academic Year Expansion Program."),
    dict(big="$6,000", label="summer grant", title="Summer Experiential Grant", org="Cornell University",
         text="Awarded to support summer research in 2026."),
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
#    text      one line: what the project is
#    built     2–3 short bullets of what you built, shown under a "What I built" toggle
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
        text="AR glasses that let Deaf, hard-of-hearing and hearing people hold a live conversation: speech shows up as captions, and replies can be picked from AI suggestions or signed, then spoken aloud.",
        built=[
            "Engineered a 7-task asynchronous AR pipeline using Whisper ASR, GPT-4o-mini and MediaPipe, with under 1 s end-to-end latency.",
            "Deployed a personalized TensorFlow Lite gesture model trained on 5K+ poses, with 95%+ accuracy after under 5 minutes of calibration.",
            "Voiced replies with Azure TTS, so the hearing person hears an answer in real time.",
        ],
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
        text="A social platform built for honest conversations, with AI that screens for harmful messages in real time.",
        built=[
            "Built real-time WebSocket infrastructure supporting 5,000+ data streams.",
            "Cut AI safety inference under 25 ms with ONNX INT8 quantization served on NVIDIA Triton.",
        ],
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
        text="An iPhone keyboard that learns where each person actually taps, with no calibration step.",
        built=[
            "Built a C++ online probabilistic model that filters noisy touches and keeps updating a 2D Gaussian for every key from real typing.",
            "Reduced input errors by 28%.",
            "Evaluated it in an iOS study app that compares a classic fixed keyboard against the adaptive one, logging every touch, timing and correction.",
        ],
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
        text="Smart glasses that read sign language gestures and facial expressions from sound and motion, no camera needed.",
        built=[
            "Built a multimodal Conformer-CTC model fusing 4-channel acoustic and 6-axis IMU signals across 35 gesture classes.",
            "Trained on 6K sequences with cross-user pretraining, per-user personalization and multitask learning.",
            "Reached 98.9% gesture accuracy and 97.4% facial-expression F1, up to 24.4% above CTC baselines.",
        ],
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
        text="Turns dense legal documents into podcast-style conversations you can actually follow.",
        built=[
            "Built a multi-agent RAG pipeline in LangGraph, with Pinecone vector search over the source document.",
            "Reduced hallucinations by 35%.",
            "Cut LLM token costs by 98.5%.",
        ],
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
        text="Navigate VR with your brain: a Muse 2 EEG headband turns imagined left/right movements into turns on a Meta Quest, no controllers.",
        built=[
            "Built a real-time 256 Hz EEG inference pipeline on FFT spectral features, reaching 82% accuracy across 20+ users.",
            "Streamed predictions over WebSockets into Unity to steer the headset, and detected intentional blinks at 88.7% accuracy.",
            "Lead a team of six, with GitHub Actions CI, code review and sprint planning that cut integration bugs by 40%.",
        ],
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
        text="A research tool from Cornell’s DAIL Lab that maps a learner’s skills as a roadmap, so they can see where they are and plan what to learn next.",
        built=[
            "Built an interactive React/TypeScript/D3 skill-roadmap interface that visualizes personalized learning graphs in real time.",
            "Implemented FAISS/Pinecone vector search in a Python/Node.js backend that generates 100+ adaptive learning nodes in Neo4j.",
        ],
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
        text="A drum battle with no drums: two players swing motion-sensing boards like drumsticks, and strikes, flicks and snaps in the air become snare, hi-hat and crash hits scored against a song.",
        built=[
            "Split the board firmware into six concurrent processes (sample, detect, classify, score, UART, feedback), with earliest-deadline-first scheduling for the real-time stages.",
            "Sampled the IMU every 10 ms on hardware timers, then filtered, detected and classified each hit.",
            "Timestamped every hit on a 1 ms board clock and streamed it over UART, so the laptop plays the sound and scores it live.",
        ],
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
