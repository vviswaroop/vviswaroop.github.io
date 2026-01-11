---
layout: post
title: "Observability on AWS at Scale: Six Years of Lessons from OpenSearch, EKS, and Production Reality"
description: "What broke, what survived, and what I would design differently after six years running observability across EC2, ECS, EKS, and OpenSearch."
tags: [developer, observability, aws, opensearch, eks, logging, metrics, tracing]
categories: [developer]
excerpt: "Observability became a platform, not plumbing. Here are the lessons from OpenSearch and EKS at scale: retention discipline, schema-first logging, ownership, and designing for deletion."
author: "Viswaroop Vadlamudi"
reading_time: 9
---

> **TL;DR:** Observability at scale is a platform problem. What survives is schema discipline, ownership, and cost-aware retention. What breaks is everything you assumed would be "set and forget."

<p class="lead">Over six years, I watched observability evolve from "nice dashboards" to a hard dependency for running the business. It doesn't behave like a tool. It behaves like a platform: it grows, it breaks, it demands ownership, and it becomes one of your most expensive systems if you're not intentional.</p>

This isn't a tutorial or a tool comparison. It's a reflection on operating observability in production across EC2, ECS, and large EKS platforms, primarily around Elasticsearch and later Amazon OpenSearch. These lessons were learned during incidents, cost reviews, and postmortems where observability itself became part of the problem.

## Phase 1: The early Elasticsearch days (where most teams start)

Like many teams, we started simple:
Applications shipped logs -> Logstash -> Elasticsearch -> Kibana.

At low scale, this worked surprisingly well. Search felt instant. Dashboards were easy to build. You could grep production without SSHing into servers. For a while, it felt like observability was "solved."

Then traffic grew.

What started breaking wasn't Elasticsearch itself, it was our assumptions:

- Indices multiplied quickly, often one per service per environment per day.
- Mappings drifted because every team logged differently.
- Shards were over-allocated, underutilized, or both.
- During incidents, the cluster slowed down exactly when we needed it most.

The biggest lesson from this phase was simple but uncomfortable: observability systems scale faster than the teams managing them. Logs grow with traffic, features, and teams, often exponentially. If you don't design guardrails early, you inherit operational debt that compounds quietly.

## Phase 2: Managed OpenSearch, less ops, more responsibility

Moving to managed OpenSearch reduced some undifferentiated heavy lifting, but it didn't reduce accountability. If anything, it forced us to confront design decisions we previously ignored.

Index lifecycle management became unavoidable. Hot-warm-cold tiering wasn't an optimization anymore, it was a requirement. Retention policies turned into business conversations, not technical ones.

One critical realization during this phase was this:

Retention is a product decision.

Keeping logs forever feels safe, but it comes with real cost and operational impact. Query performance degrades. Snapshots grow. Restore times stretch from minutes to hours. "We might need it someday" is not a strategy.

We learned to design for deletion first:

- Short hot retention for active debugging
- Warm for near-term analysis
- Cold for compliance and rare forensics
- Snapshots with clear expectations around restore time

OpenSearch made this possible, but only if data was modeled correctly. Poor schemas and inconsistent fields didn't just reduce signal, they actively slowed down incident response. No amount of compute fixes bad data.

## Phase 3: Kubernetes and EKS, observability gets hard

Kubernetes changed everything.

Logs were no longer tied to hosts. Pods were ephemeral. Nodes came and went. Services scaled horizontally by default. Cardinality exploded, sometimes invisibly.

This is where observability stopped being a tooling problem and became a platform engineering problem.

Some realities became clear very quickly:

- Centralized logging pipelines need strong backpressure controls.
- Cardinality from labels and dimensions can destroy metrics systems.
- Sidecars increase visibility but also expand blast radius.
- Not all data deserves the same retention or priority.

In EKS environments, we had to think about observability as part of cluster design:

- Per-cluster vs centralized pipelines
- Throttling and drop strategies during load
- Clear ownership by namespace, service, and team

The hardest part wasn't technical, it was cultural. Without ownership, observability devolves into a passive archive of past failures. Dashboards rot. Alerts get ignored. Signal-to-noise collapses.

## Logs, metrics, and traces: clear separation of concerns

One of the most important lessons I've learned is that logs, metrics, and traces solve different problems, and mixing them leads to confusion.

- Logs are for forensics. They answer "what happened?"
- Metrics are for alerting and trends. They answer "is this healthy?"
- Traces are for understanding behavior. They answer "why is this slow or broken?"

Anti-patterns show up when these boundaries blur:

- Alerting directly on logs
- Collecting metrics without clear consumers
- Tracing everything without a sampling strategy

Observability only works when each signal has a purpose and an owner.

## What actually worked long-term

Across teams, clusters, and architectures, a few principles consistently held up:

- Schema-first logging: strict, predictable structures over free-form text.
- Ownership baked into data: every log and metric tied to a team or service.
- GitOps for observability: dashboards, alerts, and pipelines treated as versioned artifacts.
- Cost visibility by default: teams could see what their observability usage cost.
- Designing for deletion: aggressive retention with intentional rehydration paths.

The systems that aged well weren't the most complex, they were the most intentional.

## The cultural lessons (the hardest ones)

Technology wasn't the hardest part. People and process were.

- Dashboards without owners decay.
- Alerts without SLOs become noise.
- Metrics without decisions attached are wasted.
- Platform teams must think like product teams.

Observability platforms need roadmaps, standards, and feedback loops, just like any other internal product.

## What I'd do differently today

If I were starting over:

- I'd enforce schemas from day one.
- I'd make cost attribution non-optional.
- I'd collect less data, but with higher quality.
- I'd invest earlier in developer trust and adoption.

More tools wouldn't have helped. Discipline would have.

## Closing thoughts

Observability is not about seeing everything. It's about seeing the right things quickly, without collapsing under your own data.

Tools will change. Architectures will evolve. What stays constant is the need for clarity, ownership, and restraint.

The best observability systems aren't the most sophisticated. They're the ones teams can afford, technically, operationally, and culturally, to run years later.
