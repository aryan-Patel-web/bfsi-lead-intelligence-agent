# 🏦 BFSI Lead Intelligence & CRM Automation Agent

An **agentic AI pipeline** built with **LangGraph** that automates lead research, qualification, and CRM updates — adapted specifically for **BFSI (Banking, Financial Services & Insurance)** use cases like lending and insurance lead qualification.

This project extends an open-source multi-CRM sales outreach automation framework into a domain-specific agent that mimics real enterprise workflows: structured data extraction (like underwriting form autofill), automated CRM/LOS-style writebacks, and RAG-grounded lead scoring.

> 🎓 Built by **Aryan Patel**, B.Tech CSE, **Indian Institute of Information Technology (IIIT) Manipur** — Batch of 2027

---


## 🧠 What This Project Does

Instead of a human manually researching, qualifying, and following up with every lead, this agent does it end-to-end:

1. **Fetches new leads** from a connected CRM
2. **Researches** each lead automatically (profile data, company info, context)
3. **Extracts structured fields** from unstructured lead conversations (similar to how a bank might auto-fill an underwriting form)
4. **Scores and qualifies** each lead using an LLM + RAG-grounded criteria
5. **Generates personalized outreach material** — reports, emails, and call-prep scripts
6. **Writes results back to the CRM** automatically, with follow-up scheduling for unqualified/pending leads

Everything runs as a single **stateful LangGraph pipeline** with 14+ nodes and conditional routing — no manual handoffs between steps.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔗 **Multi-CRM Integration** | Works with HubSpot, Airtable, Google Sheets, or any custom CRM via a standardized schema |
| 🧩 **Agentic LangGraph Workflow** | Stateful, multi-node graph with conditional branching (qualified vs. not qualified, more leads vs. done) |
| 📋 **Structured Field Extraction** | Pydantic-validated parsing of unstructured lead data into schema-bound fields — mirrors underwriting/PD-form autofill |
| 📊 **RAG-Grounded Lead Scoring** | Retrieves similar past case studies to ground qualification decisions in real context, not guesswork |
| 🔄 **Automated CRM Writebacks** | Lead status, reports, and next steps are written back to the CRM automatically |
| ✉️ **Personalized Outreach Generation** | Auto-generates tailored emails and interview/call-prep scripts per lead |
| 🗂️ **Local + Cloud Report Storage** | Reports saved locally and synced to Google Docs for team visibility |

---

## 🏗️ Architecture

```
Fetch Leads → Research (LinkedIn / Web / News) → Structured Extraction
        → RAG-Grounded Scoring → [Qualified?] 
              ├── Yes → Generate Outreach Materials → Update CRM
              └── No  → Save Report → Update CRM
        → Loop back until no leads remain
```

Built on **LangGraph's** `StateGraph`, so every step is a discrete, testable node with clear inputs/outputs — easy to extend or swap out individual pieces (e.g. change the CRM, change the scoring logic) without touching the rest of the pipeline.

---

## 🛠️ Tech Stack

- **LangChain** & **LangGraph** — agent orchestration and workflow graph
- **Pydantic** — structured, validated data extraction
- **Google Gemini** (Flash/Pro) — LLM + embeddings (swappable with OpenAI/Groq)
- **RAG** — case-study retrieval for grounded decision-making
- **Python 3.9+**

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/aryan-patel-web/bfsi-lead-intelligence-agent.git
cd bfsi-lead-intelligence-agent

# Set up environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# open .env and add your keys

# Run
python main.py
```

You'll need API keys for your chosen LLM provider (Gemini/OpenAI/Groq), your CRM of choice, and a search API — full details in `.env.example`.

---

## 📁 Project Structure

```
├── main.py                  # Entry point
├── src/
│   ├── graph.py              # LangGraph pipeline definition
│   ├── nodes.py               # All node logic (research, scoring, outreach, CRM update)
│   ├── state.py                # Shared graph state schema
│   ├── structured_outputs.py    # Pydantic models for structured extraction
│   └── prompts.py                # LLM prompts
├── data/                     # Sample lead/case-study data
├── reports/                  # Generated sample reports
└── docs/                     # Workflow + customization guides
```

---

## 🗺️ Roadmap — Top 5 Planned Improvements

1. **BFSI-specific field schema** — extend `structured_outputs.py` to extract loan amount, product type, and KYC status instead of generic marketing fields, closer to a real lending/insurance intake form
2. **Compliance scoring node** — add a graph node that flags missing regulatory disclosures before an outreach action is allowed to execute
3. **Automated follow-up scheduler** — new node to auto-flag and re-queue leads with no activity after N days, mimicking real CRM reminder workflows
4. **Voice input support** — integrate speech-to-text (e.g. Faster-Whisper) so lead notes can be captured hands-free during calls
5. **Multi-agent handoff** — split research, scoring, and outreach into separate specialized sub-agents coordinated by a supervisor node, for better modularity and easier testing

---



## 👤 Author

**Aryan Patel**
B.Tech CSE, Indian Institute of Information Technology (IIIT) Manipur — Batch of 2027
📧 patelaryan77462@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/aryan-patel-97396524b) · [GitHub](https://github.com/aryan-patel-web) · [Portfolio](https://portfolio-aryan-pateldev.vercel.app)

## 📄 License

This project follows the license of the original repository. See the original repo for details.
