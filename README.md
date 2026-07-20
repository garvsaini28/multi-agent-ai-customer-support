# 🤖 Multi-Agent AI Customer Support System

An intelligent AI-powered customer support system built using **FastAPI, React, MongoDB Atlas, Google Gemini, and Machine Learning**.

The system uses a **Multi-Agent Architecture** to automatically understand customer queries and route them to the appropriate specialized AI agent.

---

## 🚀 Overview

Traditional customer support systems usually rely on a single chatbot that handles every type of query.

This project takes a different approach.

It uses:

- 🤖 Multiple specialized AI agents
- 🧠 Machine Learning-based intent classification
- 🔀 Intelligent query routing
- 👤 User authentication
- 💬 Persistent chat sessions
- 🗄️ MongoDB Atlas database
- ⚡ FastAPI backend
- ⚛️ React frontend
- ✨ Google Gemini AI

The system analyzes every user query and decides which specialized agent should handle it.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      React UI       │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Router Agent     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌───────────────┐
       │ Order Agent│   │Refund Agent│   │Technical Agent│
       └─────┬──────┘   └─────┬──────┘   └───────┬───────┘
             │                │                  │
             └────────────────┼──────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │    Google Gemini    │
                    │      AI Model       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    MongoDB Atlas    │
                    │ Users + Chats + Data│
                    └─────────────────────┘
