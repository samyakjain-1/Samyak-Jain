# MarketAI - Design and Reasoning Explanation

This document explains the design choices, agent reasoning processes, and technical implementation details of the MarketAI system.

## 1. Agent Planning Style

MarketAI employs a **hybrid hierarchical and multi-agent planning style**.

- **Hierarchical Control**: A central **Orchestrator** acts as the top-level planner. It follows a predefined graph of tasks, ensuring a structured and predictable workflow. This is more reliable for a hackathon than a fully autonomous ReAct or BabyAGI loop.
- **Multi-Agent Collaboration**: The Orchestrator delegates specific sub-tasks to specialized agents. Each agent is an expert in its domain (e.g., research, contradiction). This modular design makes the system easier to build, test, and extend.

The flow is as follows:
1.  The **Orchestrator** receives the initial hypothesis.
2.  It calls the **HypothesisAgent** to structure the input.
3.  It then calls the **ResearchAgent** and **ContradictionAgent** in parallel to gather data.
4.  Finally, it passes all collected evidence to the **SynthesisAgent** to create the final report.

## 2. Memory Usage

Memory is implemented through two mechanisms, fulfilling the `memory.py` concept:

- **Short-Term Memory**: During a single analysis run, the state (structured hypothesis, research findings, etc.) is held in memory by the Orchestrator and passed between agents as arguments.
- **Long-Term Memory (MongoDB)**:
    - The `src/database/crud.py` module provides functions to interact with MongoDB.
    - Every completed analysis (the final report from the SynthesisAgent) is saved to a `reports` collection.
    - This allows for historical review of past analyses and could be used in the future to fine-tune agents or identify trends.

## 3. Tool Integration

- **Gemini API**: This is the core tool for all agent reasoning. Each agent uses a prompt designed to leverage Gemini's capabilities for its specific task (e.g., structuring text, summarizing articles, identifying risks).
- **External Data Tools (`src/tools/`)**:
    - Agents do not directly call external APIs. Instead, they use pre-defined tools.
    - For example, the `ResearchAgent` would use a `web_search_tool` that is responsible for the underlying logic of fetching data from a news source. This separation of concerns makes the system more robust and secure.

## 4. Known Limitations

- **Tool Reliability**: The system's effectiveness is highly dependent on the quality of the data returned by its tools. Biased news sources or inaccurate financial data will lead to skewed results.
- **Static Planning**: The current Orchestrator follows a fixed plan. It cannot dynamically change its strategy based on initial findings. For example, if the HypothesisAgent fails to structure the query, the process stops instead of asking the user for clarification.
- **No User Interaction Loop**: The system performs a one-shot analysis. There is no mechanism for a user to ask follow-up questions or provide feedback to refine the results.
