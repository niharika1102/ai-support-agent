# AI Support Agent — Tool Calling & Agents

A small hands-on project for understanding how **LLM tool calling and AI agents** work.

The project implements a simple customer-support agent that can dynamically choose between two tools:

- Calculator
- FAQ lookup

The same idea is implemented first **manually using the Gemini SDK** and then using **LangChain**, making it possible to understand what an agent framework actually abstracts.

---

## 🎯 Purpose

This project was built as a learning exercise to understand:

- LLM tool calling
- Tool definitions and schemas
- Function/tool execution
- Tool results
- Agent loops
- Multiple tools
- Dynamic tool selection
- LangChain tool abstractions
- LangChain agent runtime
- Difference between an LLM, tools, and an agent framework

This is intentionally a small project with no UI, database, authentication, or deployment.

---

# 🧠 What I Learned

## 1. Tool Calling

An LLM cannot directly execute Python functions.

Instead, the application provides the model with descriptions of available tools.

For example:

```text
calculator(expression)
faq_lookup(topic)