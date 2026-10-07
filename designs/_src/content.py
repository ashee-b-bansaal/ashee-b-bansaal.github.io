# Shared content for all three designs. Edit here, re-run build.py.

NAME = "Ashee B Bansaal"
EMAIL = "ab3235@cornell.edu"
GITHUB = "https://github.com/ashee-b-bansaal"
LINKEDIN = "https://linkedin.com/in/ashee-b-bansaal"
TAGLINE = "Software &amp; ML Engineering · CS @ Cornell"

ABOUT_HEAD = "I’m Ashee, a CS junior at Cornell. I build software, and the machine learning systems that run inside it."
ABOUT = [
    "The parts of ML I like best are really systems problems: getting a model to answer inside a latency budget, making training runs reproducible, rewriting the slow step in CUDA. Before any of that I shipped Android and backend features to 150K monthly users at Cult.fit, which is where I learned to care about p95s, retries, and what happens when a device goes offline mid-sync.",
    "I study Computer Science (Honors, ML/AI track) with a minor in ECE, and I’m TAing Machine Learning this fall. Away from a keyboard (the typing kind), I write poetry, play flute and keyboard (the musical kind), and take a lot of photos.",
]
SEEKING = "Looking for <strong>Summer 2027</strong> software engineering and ML engineering internships."

# Lines from your own poems, used as small epigraphs. Replace these.
EPIGRAPHS = {
    "about": "[a line from one of your poems]",
    "experience": "[another line from your poetry book]",
    "projects": "[a line about building things]",
    "hobbies": "[a line from your book]",
}

EXPERIENCE = [
    dict(logo="CMU", role="ML Research Intern", org="Carnegie Mellon University · Semantic Signal Lab",
         when="Jun 2026 – Aug 2026", where="Pittsburgh, PA", now=False,
         text="Built a GPU embedding-deduplication engine in CUDA/PyTorch that matched the CPU reference exactly on 3,700+ targets in 283&nbsp;s. Also built the vector-embedding retrieval layer for a long-video memory system and a cross-session identity tracker (DINOv2 + Sinkhorn) over 10+ hours of footage.",
         tags=["PyTorch", "CUDA", "Vector search", "DINOv2"]),
    dict(logo="C", role="Founder &amp; ML Engineer", org="Cognify",
         when="Aug 2025 – Present", where="Ithaca, NY", now=True,
         text="Building a hands-free control interface driven by EEG. Real-time classifier ensemble at 93% accuracy; containerized training and deployment with Docker, Kubernetes, and Optuna sweeps, cutting an experiment cycle from five days to two.",
         tags=["PyTorch", "Docker", "Kubernetes", "Optuna"]),
    dict(logo="Sci-Fi", role="Machine Learning Intern", org="Cornell University · Sci-Fi Lab",
         when="Jun 2025 – Aug 2025", where="Ithaca, NY", now=False,
         text="Built a PyTorch Conformer-CTC training pipeline over 6K+ multimodal sequences, plus the evaluation tooling and cross-user / 5-fold personalization setup. Reached 98.9% accuracy on 35 classes; multitask learning beat the baseline by 24%.",
         tags=["PyTorch", "Conformer", "Eval tooling"]),
    dict(logo="cult", role="Software Engineer Intern", org="Cult.fit · Android &amp; Backend",
         when="May 2024 – Jul 2024", where="Bengaluru, India", now=False,  # EDIT: confirm location
         text="Shipped Health Connect sync to a 150K-MAU Android app across 6+ wearable sources. Built coroutine pipelines with circuit breakers and retries handling 500K+ events/day at &lt;100&nbsp;ms p95, cut SQLite latency 60% with WAL, and ran Firebase → BigQuery A/B tests across 50K users.",
         tags=["Kotlin", "Java", "Coroutines", "SQLite", "BigQuery"]),
    dict(logo="XR", role="BCI Sub-team Lead", org="Cornell Extended Reality Project Team",
         when="Jan 2025 – Present", where="Ithaca, NY", now=True,
         text="Lead a team of six: GitHub Actions CI, code review, and sprint planning, which cut integration bugs by 40%. See the BCI project below.",
         tags=["Leadership", "CI/CD", "Python"]),
]

# kind = which generative figure the fractal design draws for this card
PROJECTS = [
    dict(id="cognify", name="Cognify", tagline="Hands-free control, from brainwaves",
         ctx="Founder &amp; ML engineer · Aug 2025 – now",
         text="A brain-computer interface you drive by looking at flickering targets. I built the real-time classifier (Conv-LSTM attention ensembles), an EEGNet + temporal CNN pipeline for motor imagery, and a containerized training setup on Kubernetes with Optuna sweeps.",
         chips=["PyTorch", "EEGNet", "Docker", "Kubernetes", "Optuna"],
         stats=[("93%", "real-time SSVEP accuracy"), ("5→2", "days per experiment cycle")],
         links=[("GitHub", "#")], kind="dragon", tint="lavender", photo="photos/cognify.jpg"),
    dict(id="xr-bci", name="Cornell XR · BCI", tagline="Live EEG inference for extended reality",
         ctx="Sub-team lead · Cornell XR · Jan 2025 – now",
         text="Our sub-team streams EEG at 256&nbsp;Hz into a real-time inference pipeline built on FFT spectral features, so XR experiences can respond to the person wearing the headset. I lead six engineers and set up our CI, code review, and sprint process.",
         chips=["Python", "FFT features", "Streaming", "GitHub Actions"],
         stats=[("82%", "accuracy across 20+ users"), ("−40%", "integration bugs after CI")],
         links=[("GitHub", "#")], kind="sierpinski", tint="mint", photo="photos/xr.jpg"),
    dict(id="sos", name="Select-or-Sign", tagline="Conversation help in AR, in under a second",
         ctx="Cornell Sci-Fi Lab · Aug 2025 – Jul 2026",
         text="An AR communication interface that orchestrates seven async tasks (Whisper speech recognition, GPT-4o, MediaPipe hand tracking) inside a one-second budget, with a personalized on-device TFLite gesture model trained on 5K+ poses.",
         chips=["Python asyncio", "Whisper", "GPT-4o", "MediaPipe", "TFLite"],
         stats=[("&lt;1s", "end-to-end latency"), ("95%+", "gesture accuracy, &lt;5 min calibration")],
         links=[("Paper (soon)", "#")], kind="koch", tint="sky", photo="photos/sos.jpg"),
    dict(id="calibratype", name="CalibraType", tagline="A keyboard that learns your thumbs",
         ctx="Cornell Sci-Fi Lab · May 2025 – now",
         text="An online probabilistic model in C++ that keeps a 2D Gaussian per key and updates it from noisy real-world touches, so the keyboard adapts to you with no calibration step.",
         chips=["C++", "Online learning", "Mobile input"],
         stats=[("−28%", "input error"), ("0", "calibration steps")],
         links=[("Paper (soon)", "#")], kind="fern", tint="peach", photo="photos/calibratype.jpg"),
    dict(id="spatial", name="Spatial Moves", tagline="Learning paths, drawn as graphs",
         ctx="Cornell DAIL Lab · Jan – Jul 2025",
         text="A personalized learning platform. I built the React/TypeScript/D3 interface for interactive skill graphs and the Python/Node vector-search services over FAISS, Pinecone, and Neo4j that generate each student’s adaptive path.",
         chips=["React", "TypeScript", "D3", "Node", "FAISS", "Neo4j"],
         stats=[("100+", "adaptive learning nodes"), ("3", "vector &amp; graph stores")],
         links=[("GitHub", "#")], kind="tree", tint="rose", photo="photos/spatial.jpg"),
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
