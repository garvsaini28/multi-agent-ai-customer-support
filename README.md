# 🤖 Multi-Agent AI Customer Support System

An intelligent AI-powered customer support system built using **FastAPI, React, MongoDB, Google Gemini, Machine Learning, and a Multi-Agent Architecture**.

The system automatically understands customer queries, classifies their intent, and routes them to the most suitable specialized AI agent such as:

- 📦 Order Support Agent
- 💰 Refund Support Agent
- 🛠️ Technical Support Agent
- 🤖 General AI Support

The application also provides secure authentication, persistent chat history, session management, user profiles, and an interactive modern chat interface.

---

## 🚀 Project Overview

Traditional customer support systems usually rely on a single chatbot or predefined rules.

This project follows a **Multi-Agent AI Architecture** where different types of customer queries are intelligently routed to specialized agents.

### Example:

```text
User Query
    │
    ▼
Intent Detection
    │
    ▼
┌─────────────────────────┐
│   Router Agent          │
└─────────────────────────┘
    │
    ├── Order Query
    │       │
    │       ▼
    │   Order Agent
    │
    ├── Refund Query
    │       │
    │       ▼
    │   Refund Agent
    │
    ├── Technical Query
    │       │
    │       ▼
    │ Technical Support Agent
    │
    └── General Query
            │
            ▼
       Gemini AI
