---
layout: post
title: "Ingress vs Gateway API on GKE: What Actually Changes in Production"
description: "What changes in ownership, policy, and scale when you move from Ingress to Gateway API on GKE, and when you should not migrate yet."
tags: [developer, kubernetes, gke, ingress, gateway-api, networking, platform]
categories: [infrastructure, platform, kubernetes]
excerpt: "Gateway API on GKE is not just a new abstraction. It changes ownership boundaries, policy enforcement, and how teams share infrastructure at scale."
author: "Viswaroop Vadlamudi"
reading_time: 6
---

> **TL;DR:** Gateway API on GKE is not a drop-in replacement for Ingress. It redefines ownership boundaries and makes platform control explicit. If your cluster is a shared platform, that shift is the point.

<p class="lead">For years, Kubernetes Ingress was the default way teams exposed services. It worked well, especially on managed platforms like Google Kubernetes Engine where Ingress is deeply integrated with Google Cloud's global HTTP(S) Load Balancer.</p>

As clusters evolved from single-team playgrounds into shared platforms, the cracks in Ingress became impossible to ignore. Gateway API is not just a newer abstraction. On GKE, it fundamentally changes how ownership, control, and scale are handled.

This is not a rehash of docs. It is a production-level look at what actually changes when you move from Ingress to Gateway API on GKE, and when you should not.

## Why Ingress becomes a bottleneck at scale

Ingress was designed to be intentionally simple:

- One resource
- Basic routing
- Controller-specific behavior

That simplicity becomes a liability once:

- Multiple teams share the cluster
- Platform teams own infrastructure
- Security teams need policy boundaries

In real GKE environments, Ingress often turns into:

- Annotation sprawl
- Controller-specific hacks
- Poor separation of responsibility

Ingress works, until it becomes the only place everyone tries to solve their problem.

## How Ingress actually works on GKE

On GKE, Ingress is not just Kubernetes.

Under the hood:

- Ingress provisions a Google Cloud HTTP(S) Load Balancer
- Services are attached via NEGs
- Advanced features rely on BackendConfig, FrontendConfig, and annotations

This gives you powerful capabilities:

- Global load balancing
- Managed TLS
- Tight GCP integration

But it comes at a cost. GKE Ingress is powerful, but it is no longer portable Kubernetes. Every advanced behavior pulls you deeper into GKE-specific constructs, making governance and multi-team ownership harder.

## The core design problem with Ingress

Ingress collapses too many concerns into one resource:

| Concern | Who wants control |
|---------|-------------------|
| Load balancer lifecycle | Platform team |
| TLS and certs | Security or platform |
| Routing rules | App teams |
| Policy and limits | Platform |

Ingress has no native way to express this separation. Everything lives together, or not at all.

## Gateway API: A contract, not a controller

Gateway API introduces something Ingress never had: clear ownership boundaries.

It breaks networking into layered APIs:

- GatewayClass implemented by the platform
- Gateway owned by infra and platform teams
- HTTPRoute owned by application teams

This is not accidental. It is a deliberate response to how Kubernetes is actually used today. Gateway API does not replace Ingress, it fixes its original blind spots.

## Gateway API on GKE: What is really implemented

GKE's Gateway API implementation is first-class, not experimental glue.

Key characteristics:

- Native Google Cloud Load Balancer integration
- Managed TLS without annotation overload
- Cross-namespace routing with explicit permissions
- Alignment with platform ownership models

On GKE, Gateway API feels like Ingress rewritten with platform engineering in mind.

## Ownership model: Where Gateway API shines

With Ingress:

- App teams define infrastructure implicitly
- Platform teams reactively police configs
- Security is enforced after the fact

With Gateway API:

- Platform teams own Gateway
- App teams own HTTPRoute
- Security and policy are built into the model

This separation alone eliminates entire classes of operational friction.

## Migration reality: Ingress to Gateway API

This is not a kubectl apply migration.

Easy:

- Host-based routing
- Path routing
- TLS termination

Hard:

- Replacing annotation-based features
- Updating automation
- Educating teams on new boundaries

Gateway API is not a drop-in replacement. It is a platform decision. If you do not change how teams collaborate, you will not see the benefits.

## When you should not migrate yet

Ingress is still perfectly valid if:

- You run single-team clusters
- Routing needs are simple
- You do not need strict governance

Ingress is fine until you need structure. Gateway API shines when complexity is unavoidable.

## Strategic take: Why Gateway API matters long-term

Gateway API aligns Kubernetes networking with:

- Platform engineering
- Multi-tenant clusters
- Explicit contracts
- Future L4 and L7 convergence

On GKE specifically, it represents Google acknowledging a reality many teams already live in: clusters are platforms, not apps.

Gateway API does not just modernize routing, it formalizes how teams share infrastructure.

## Final thought

If you are building or operating a shared GKE platform today, Gateway API is not a nice to have. It is the model Ingress never grew into.
