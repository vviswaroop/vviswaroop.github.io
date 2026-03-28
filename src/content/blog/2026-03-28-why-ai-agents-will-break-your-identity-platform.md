---
title: "Why AI Agents Will Break Your Identity Platform"
date: 2026-03-28
tags: [ai, identity, platform, oauth2, infrastructure, orchestration]
---

> **TL;DR:** When autonomous AI agents act on your behalf while you sleep, traditional user-centric identity boundaries break. OAuth2 and short-lived tokens expect humans at keyboards; autonomous agents require strict Sandboxing, M2M delegations, and Zanzibar-style relationship permissions. If your platform isn't ready, your AI is a massive compliance risk.

<p class="lead">We've spent a decade building robust identity systems optimized for human behavior. OAuth2, OIDC, short-lived access tokens, and interactive MFA redirects assumed a fundamental truth: a human is sitting at a browser, waiting for the webpage to load.</p>

But the industry just pivoted. The rise of Agentic AI—tools like OpenDevin, Cursor, Open Claw, and autonomous n8n workflows—means that software is now acting *as* the user, asynchronously, for hours at a time. The human has left the keyboard, but the system is still running.

Most enterprise Identity and Access Management (IAM) platforms, including managed giants like AWS Cognito, are conceptually blind to this shift. Here is why autonomous agents will break your identity architecture, and how platform engineers must respond.

## The Flawed "Human-in-the-Loop" Assumption

Traditional identity platforms are built around **interactive delegation**. A user logs in, authorizes an application (via OAuth2 scopes), gets a short-lived access token, and maybe a refresh token. When the token expires, the browser refreshes it, or prompts the human for biometric MFA.

**An AI Agent doesn't have a browser.**

Imagine an autonomous orchestration agent deployed to analyze your Jira tickets, write a design doc, query a production database for metrics, and push a PR to GitHub—all overnight.

If you use standard OAuth flows:
1. The agent's token expires midway through the 6-hour task.
2. The agent attempts to refresh the token but hits an MFA or session anomaly boundary.
3. The workflow dies.

## The "Permanent Waiter" Anti-Pattern

To fix the expiry problem, teams often make the easiest, and most dangerous, architectural choice: they issue the AI agent a **long-lived Personal Access Token (PAT)** or infinite refresh token.

This is the "Permanent Waiter" anti-pattern. You've just given a non-deterministic, LLM-driven black box permanent access to read your emails, push code, and query production data. 

> If an LLM hallucination or prompt injection attack causes the agent to act maliciously, a long-lived token means it can do immense damage before it is ever detected.

## The Identity Platform Solution for Agentic AI

To secure autonomous AI workflows, platform engineering teams must stop treating agents like users, and start treating them like **delegated infrastructure**.

### 1. Granular, Just-in-Time Scopes (Not Broad PATs)
Instead of giving an AI agent broad GitHub or AWS access, identity systems must support hyper-granular, Just-in-Time (JIT) provisioning. The orchestrator must request a short-lived token scoped *only* to the specific repo or S3 bucket the agent is working on in that exact moment.

### 2. Machine-to-Machine (M2M) with Human Context
The AI agent is a machine, but it acts *on behalf* of a human. We need advanced token exchange strategies (like RFC 8693) where the orchestrator acts as a middleman, exchanging a user's initial authorization for a highly constrained, backend M2M token that the agent actually uses to operate.

### 3. Relationship-Based Access Control (Zanzibar)
Role-Based Access Control (RBAC) fails with autonomous agents. An agent doesn't need the role of "Admin" or "Developer." It needs the permission to *read* document A because document A *belongs to* project B, which the user *owns*. 
This is where systems like **ORY Keto** (implementing Google's Zanzibar model) become critical. You can architect graph relationships that say: "This agent session is allowed to modify an asset only if the asset is related to the active workflow ID."

### 4. Zero-Trust Network Sandboxing
Identity is only half the battle. If your autonomous coding agent pulls down untrusted npm packages to execute a script, IAM won't save you. The agent's execution environment must be deployed to zero-trust, ephemeral Kubernetes sandboxes with egress strictly locked down via NetworkPolicies and Open Policy Agent (OPA).

## The Path Forward

Autonomous workflows are not going to slow down. The companies that succeed won't just be the ones building the smartest agents; they will be the ones that build the secure, scalable, and resilient platforms required to host them in production.

If you are a platform engineer, your mandate just expanded. The boundary has shifted from the frontend authentication wall to the orchestration sandbox. It's time to build the guardrails that make autonomous AI safe for the enterprise.
