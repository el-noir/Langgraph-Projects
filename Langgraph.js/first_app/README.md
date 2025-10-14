# Agent App

This monorepo contains example LangGraph agent apps (web + agents).

Environment
-----------

The dev CLI expects a `.env` file at the project root (see `langgraph.json`).
Create one by copying the provided example:

```bash
cd first_app
cp .env.example .env
```

Fill in any API keys or connection strings required by your agents (for example `NEXT_PUBLIC_LANGSMITH_API_KEY`, `MONGODB_URI`, etc.).

The `.env.example` contains common variables used across the workspace.

