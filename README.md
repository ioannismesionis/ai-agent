# AI Agent Journey

This repository tracks my work through Google/Kaggle's 5‑day AI Agents intensive and captures the capstone concept I'm building along the way.

- **Course hub:** https://www.kaggle.com/competitions/agents-intensive-capstone-project  
- **Goal:** design, evaluate, and deploy an AI concierge that guides people toward the right job track by asking smart questions, researching paths, and summarizing tradeoffs.

---

## Project vision – Job Track Concierge

| Step | Notes |
| --- | --- |
| Select a track | The agent acts like a concierge/coach that narrows job paths based on user goals. |
| Problem & solution | Job hunting is noisy; the agent reduces decision friction by interviewing the user, researching opportunities, and proposing directions. |
| Publish code | Source of truth lives in this GitHub repo so each experiment and notebook is reproducible. |
| Value proposition | Saves research time, surfaces actionable recommendations, and keeps a traceable conversation history for follow-up iterations. |
| Demo video | TBD – planned once a multi-agent prototype exists. |

Planned features:
- Multi-agent orchestration (concierge, researcher, critic loops)
- Tooling for job market search, resume parsing, and calculation
- Sessions + long-term memory so the agent remembers preferences across chats
- Evaluation harness plus deployment pathway (Vertex AI Agent Engine)

---

## Course labs & takeaways

| Day | Notebook | Key concepts digested |
| --- | --- | --- |
| 1A | `labs/day1/day-1a-from-prompt-to-action.ipynb` | Gemini setup, basic `Agent` + `InMemoryRunner`, `adk web` debugging workflow |
| 1B | `labs/day1/day-1b-agent-architectures.ipynb` | Sequential, parallel, and loop orchestration patterns for multi-agent teams |
| 2A | `labs/day2/day-2a-agent-tools.ipynb` | Designing reliable custom tools, chaining to code execution sub-agents, tooling taxonomy |
| 2B | `labs/day2/day-2b-agent-tools-best-practices.ipynb` | MCP integrations, long-running operations, pause/resume workflows, event handling |
| 3A | `labs/day3/day-3a-agent-sessions.ipynb` | Session services (in-memory + SQLite), context compaction, stateful tool patterns |
| 3B | `labs/day3/day-3b-agent-memory.ipynb` | Memory services, manual vs automatic ingestion, reactive/proactive retrieval, consolidation |
| 4A | `labs/day4/day-4a-agent-observability.ipynb` | ADK web traces, DEBUG logging, observability plugins, production logging strategies |
| 4B | `labs/day4/day-4b-agent-evaluation.ipynb` | Interactive eval cases, CLI regression suites, evaluation metrics, user simulation hooks |
| 5A | `labs/day5/day-5a-agent2agent-communication.ipynb` | Agent2Agent protocol, exposing services via `to_a2a`, consuming remote agents |
| 5B | `labs/day5/day-5b-agent-deployment.ipynb` | Packaging agents, configuring `.agent_engine_config.json`, deploying/testing on Vertex AI Agent Engine |

Each notebook builds toward the concierge agent by covering tooling, memory, observability, evaluation, collaboration, and deployment.

---

## Implementation checklist

- **Multi-agent system**
  - [ ] LLM-powered root agent orchestrator
  - [ ] Parallel researchers for labor-market data
  - [ ] Sequential writing/editing loops for plan generation
  - [ ] Loop agent for critique/refinement cycles

- **Tools**
  - [ ] MCP connectors (e.g., search, GitHub, Slack)
  - [ ] Custom Python tools (job matching logic, resume parsing)
  - [ ] Built-ins such as Google Search + Code Execution
  - [ ] OpenAPI integrations and long-running approval flows

- **Sessions & Memory**
  - [ ] Durable session service (SQLite/managed DB)
  - [ ] Long-term memory (Memory Bank or managed service)
  - [ ] Context compaction + explicit state tooling

- **Observability & Evaluation**
  - [ ] `LoggingPlugin` and custom callbacks
  - [ ] Regression eval sets via `adk eval`
  - [ ] User simulation scenarios for stress testing

- **Deployment**
  - [ ] Agent packaged for Vertex AI Agent Engine
  - [ ] Post-deployment validation scripts
  - [ ] Cleanup + cost safeguards

---

## Next steps
1. Translate notebook prototypes into reusable Python modules under `main.py` or a dedicated package.
2. Implement the job-track concierge multi-agent workflow with real tools and memory services.
3. Stand up evaluation suites + observability plugins, then package for deployment. 

---

## Project Pitch

### Why this matters
Choosing a career path has become a noisy, high-stakes decision: job titles shift quarterly, each role requires different skill investments, and misalignment costs both time and morale. Traditional career sites dump static lists that quickly feel overwhelming. Learners in the *AI Agent* track need a demonstrably agentic solution that goes beyond static recommendations and instead collaborates with users to uncover their “why,” explore markets, and act on next steps.

### What we’re building
**Job Track Concierge** is a multi-agent system that interviews the user, researches labor-market data, matches preferences against real openings, and iteratively refines a personalized plan. The core experience is an interactive session where the agent asks clarifying questions, runs research tools, summarizes tradeoffs, and logs preferences to long-term memory so conversations build on each other. The output is an actionable roadmap: target roles, required skills, timelines, and curated resources.

### Solution architecture (agent-first)
1. **Concierge Orchestrator (LLM Agent):** Guides the conversation, decides which specialized agents or tools to invoke, and ensures every step ties back to the user’s goals.  
2. **Parallel Research Agents:** Each focuses on a domain (AI/ML, product, data, design) and uses Google Search, MCP endpoints, and job APIs to surface current opportunities and skill trends.  
3. **Sequential Planning Pipeline:** Outline → Plan Writer → Critique/Loop agents refine the recommendation packet until it meets quality criteria, leveraging loop-based refinements for clarity.  
4. **Tooling Layer:** Custom resume parser, cost calculator, and MCP connectors (Everything server for quick prototypes, plus OpenAPI integrations for job boards). Long-running approval flows manage any costly actions (e.g., scheduling demo interviews).  
5. **Sessions & Memory:** Durable session service stores the conversation thread; Memory service captures stable preferences (location, salary ceiling, values) for instant recall across sessions. Context compaction keeps prompts efficient.  
6. **Observability & Evaluation:** LoggingPlugin + custom callbacks capture traces, while `adk eval` regression suites and user-simulation scenarios guard against regressions as new tools or agents are introduced.  
7. **Deployment Path:** Packaged as an ADK app, deployable to Vertex AI Agent Engine with monitoring hooks and cleanup scripts, ensuring a production-ready experience.

### Innovation & value
- **Agent-native UX:** Instead of static questionnaires, the concierge co-creates the plan through live inquiry, adaptive research, and memory-driven follow-ups.  
- **Multi-agent rigor:** Parallel researchers plus loop critics keep insights fresh and balanced, going beyond a single LLM answer.  
- **Trust through observability:** Every recommendation is traceable via sessions, events, and evaluation artifacts—critical for high-stakes career guidance.  
- **Scalable delivery:** The Vertex Agent Engine deployment ensures low-latency access while MCP/OpenAPI tools make it easy to plug in new data sources.

### Storytelling the journey
- **Day 1–2:** Graduated from single-agent prompts to multi-agent orchestration with custom tools and code-execution subagents.  
- **Day 3:** Added persistent sessions, state tooling, and long-term memory so the concierge can remember users between visits.  
- **Day 4:** Layered observability and evaluation to catch regressions before users do.  
- **Day 5:** Built the collaboration (A2A) and deployment muscles needed to expose the concierge as a reliable service.  
- **Now:** Translating these lab learnings into a cohesive concierge experience, validating each milestone with regression tests, and prepping a polished demo.

This pitch demonstrates the *why* (career guidance needs adaptive intelligence) and the *what* (a multi-agent concierge) while keeping agents central to every architectural decision. It also outlines the roadmap from concept to deployment, showing clear communication of vision, innovation, and execution.
