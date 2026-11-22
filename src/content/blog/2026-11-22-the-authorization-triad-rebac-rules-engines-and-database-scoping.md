---
title: "The Authorization Triad: Why Real Systems Can’t Pick Just One"
date: 2026-11-22
tags: ["Identity", "Platform", "Architecture"]
description: "How relationship engines (ReBAC), rules engines (ABAC), and database scoping collide at scale — and why production systems must compose them."
---

> **TL;DR:** Vendor pitches promise that a single authorization tool—Zanzibar, OPA, or Postgres RLS—can solve the entire problem. In production, forcing one paradigm outside its sweet spot leads to tuple explosion, graph exhaustion, or unpaginated query timeouts. High-performing systems don't pick one; they layer them across the request lifecycle.

<p class="lead">Every engineering team starts authorization with the simplest thing that works: a <code>role</code> column in the <code>users</code> table and a <code>WHERE tenant_id = ?</code> filter in their SQL queries. It is fast, predictable, and leverages relational indexes.</p>

Then the product grows:
- **Enterprise customers demand custom roles:** *"Our IT group needs administrative access, but Billing should only view invoices."*
- **Hierarchical resource sharing enters:** *"Folders inherit access from parent workspaces, but sub-documents can have external collaborators."*
- **Dynamic compliance rules arrive:** *"Managers can approve expenses, but only under \$10,000, during working hours, and never for their own submissions."*
- **Distributed microservices decouple data:** *"Authorization must happen at the edge or across 12 downstream services without opening 12 direct database connections."*

At this inflection point, teams go shopping for an "Authorization Solution." The industry splits into three loud camps:

1. **The Relationship Camp (ReBAC / Zanzibar):** *"Decouple everything into relationship tuples. Everything is a graph."*
2. **The Policy Camp (ABAC / Rules Engines):** *"Decouple policy from application code. Write declarative rules in OPA Rego or AWS Cedar."*
3. **The Data Camp (Row-Level Security / SQL Scoping):** *"Centralize enforcement inside PostgreSQL RLS or SQL query wrappers."*

The trap is believing that any single one of these can solve the whole puzzle. At scale, **forcing one tool outside its native domain causes catastrophic latency, memory bloat, or security leaks.**

---

## The Three Paradigms: Anatomy & Sweet Spots

| Dimension | 1. Authz Engine (ReBAC / Zanzibar) | 2. Rules Engine (ABAC / Policy-as-Code) | 3. Database Scoping (Data Tier / RLS) |
| :--- | :--- | :--- | :--- |
| **Primary Question** | *"Does Subject $S$ have Relation $R$ to Object $O$?"* | *"Given this context payload, does policy evaluate to allow/deny?"* | *"Which 20 rows out of 500,000 can $S$ see, sorted by date?"* |
| **Data Structure** | Directed Graph / Sparse Relation Tuples | Abstract Syntax Trees (ASTs) & Booleans | B-Trees, Compound Indexes, Relational Tables |
| **Evaluation Model** | Recursive graph traversal, set expansion | Pure functional in-memory evaluation | Relational Query Planner, Index Scans, Joins |
| **Exemplars** | Google Zanzibar, Ory Keto, SpiceDB, OpenFGA | Open Policy Agent (OPA), AWS Cedar, CEL | Postgres RLS, Partitioned Schemas |
| **Sweet Spot** | Deep hierarchies, group membership, delegated sharing | Business rules, numeric thresholds, temporal constraints | Bulk reads, paginated listings, analytical aggregations |

---

## Where Each Fails at Scale

### 1. The ReBAC "Tuple Explosion" (Dynamic Context)
Zanzibar is built for structural, relatively stable relationships: `user:alice` is `member` of `group:platform`.

When teams try to model dynamic business rules in Zanzibar, disaster strikes:
- *"User can only view the medical record if they are on the hospital Wi-Fi."*
- *"Approver cannot approve if the expense amount exceeds \$5,000."*
- *"Temporary access expires after 30 minutes of inactivity."*

If you try to write dynamic IP ranges, amounts, or timestamps as relation tuples, your tuple database explodes by orders of magnitude. Every user interaction causes a write-storm to the tuple store, and distributed graph caches thrash continuously.

> **Rule of thumb:** *ReBAC is for structural topology. Never put transient, temporal, or numerical thresholds into a tuple store.*

---

### 2. The Rules Engine "Graph Exhaustion"
Rules engines like OPA or Cedar are remarkably fast at pure boolean evaluations:

```text
allow {
    input.action == "view"
    input.resource.type == "document"
    input.user.department == input.resource.department
    input.request.risk_score < 40
}
```

However, a rules engine **has no native understanding of your relational or hierarchical graph**. 

What happens when the policy becomes:
> *"Allow if Alice is in a team that was assigned to a workspace whose parent organization has granted read rights to this project"?*

To evaluate that, the rules engine either:
1. **Requires the caller to pre-fetch the entire organizational graph** and inject it into the `input` JSON payload. Request payloads inflate to megabytes, and network serialization destroys latency.
2. **Makes HTTP/gRPC calls from inside the policy.** This violates the core design of policy engines, introducing unpredictable network waterfall latencies (turning a 1ms decision into 80ms).

> **Rule of thumb:** *Rules engines are computational, not storage engines. They should evaluate decisions, not traverse deep relational graphs.*

---

### 3. The Fatal "Search & List" Dilemma
This is the single biggest architectural crisis in authorization at scale.

Point checks are straightforward:
```text
GET /documents/42
→ Is Alice allowed to view Document 42?
→ Check(Alice, view, doc:42) → ALLOW (2ms)
```

Listing and paginating is entirely different:
```text
GET /documents?page=1&sort=updated_at_desc
→ Return 20 documents that Alice is allowed to see.
```

There are three common ways naive teams attempt this, and all three fail:

* **Approach A: Post-Filter in Memory.**  
  Fetch 20 documents from the database, loop through them, and call `check()` on each one.  
  *Why it breaks:* If Alice only has access to 2 of those 20 documents, the response returns 2 items instead of 20. Pagination, infinite scrolling, and item counts (`Total: 1,420`) break completely.

* **Approach B: ReBAC `ListObjects` + SQL `WHERE IN`.**  
  Ask the ReBAC engine: `list_objects(user:alice, relation:viewer, type:document)`.  
  *Why it breaks:* In an enterprise organization, Alice might have access to 85,000 documents via shared team folders. Zanzibar returns 85,000 IDs. Passing 85,000 parameters to `SELECT * FROM documents WHERE id IN ($1, ... $85000) LIMIT 20` brings the database query planner to a complete halt.

* **Approach C: Replicating Permissions into the Database.**  
  Syncing Zanzibar permissions or OPA rules directly into columns or auxiliary tables in the primary database.  
  *Why it breaks:* Distributed consistency. As soon as you have two sources of truth, synchronization lag creates security holes. Revoking an employee's access in the identity platform doesn't immediately reflect in the database index, leading to ghost access.

---

## The Production Blueprint: Tiered Request Pipeline

High-scale platforms do not pick one paradigm. They **tier** them across the request lifecycle:

```text
[ Incoming Request ]
         │
         ▼
[ Stage 1: Edge & Invariants (Rules Engine / ABAC) ]
  • Validate JWT claims, tenant active status, rate limits, device posture
  • Decision: ALLOW / DENY (< 1ms)
         │
         ├─── Mutating Action (POST / PUT / DELETE)
         │         ▼
         │   [ Stage 2A: Point Enforcement (ReBAC + Domain Rules) ]
         │   • ReBAC: Does Subject have 'editor' on Target Resource? (Graph check)
         │   • Domain Rule: Does mutation violate state machine or business limits?
         │   • Write to Database
         │
         └─── Bulk Read / Search (GET /items?page=1)
                   ▼
             [ Stage 2B: Query Pushdown (Scope Compiler) ]
             • Resolve coarse access tokens (e.g. user's active workspace IDs)
             • Compile into parameterized SQL AST:
                 WHERE tenant_id = :tenant_id
                   AND (visibility = 'public' OR workspace_id IN (:workspaces))
             • Database executes indexed scan, sorting, and LIMIT/OFFSET
```

### Stage 1: Edge Invariant Checks (Rules Engine)
Evaluates ephemeral, coarse-grained perimeter conditions before hitting business services:
- Is the tenant account active or delinquent?
- Is the caller attempting an admin operation from an unmanaged device?
- Does the JWT carry the required OAuth2 scopes?
*Latency:* $< 1$ms, zero database calls, evaluated in-memory at the gateway.

### Stage 2A: Point Mutations (ReBAC + Domain Rules)
For any point action (`PUT /documents/42`, `POST /transfers`):
- **ReBAC check:** Does `user:alice` have `editor` relation on `doc:42`? (Traverses team/folder graph).
- **Rules check:** Does the payload satisfy business invariants? (e.g., Is document locked? Is transfer amount within daily cap?).
*Latency:* Fast because point checks have bounded graph depth and are aggressively cached.

### Stage 2B: The Search/List Solution (The Scope Compiler)
To solve the list dilemma without $N+1$ checks or giant `IN` clauses, mature architectures compile coarse authorization scopes into the query itself:
- **Tenant Partitioning:** Hard boundary at `tenant_id` (always first in compound indexes).
- **Hierarchical Ancestor Tokens:** Rather than asking for millions of individual leaf object IDs, objects store a coarse ancestor boundary (e.g. `workspace_id` or `folder_path`). The query planner only checks:
  ```sql
  SELECT id, title, updated_at
  FROM documents
  WHERE tenant_id = :tenant_id
    AND (visibility = 'public' 
         OR workspace_id IN (:user_accessible_workspaces))
  ORDER BY updated_at DESC
  LIMIT 20 OFFSET 0;
  ```
- Because a user belongs to dozens of workspaces rather than millions of documents, the `IN` list is small ($< 50$), query plans stay in index range scans, and pagination is deterministic.

---

## Architectural Checklist for Practitioners

1. **Don't put timestamps, weather, or wallet balances into Zanzibar tuples.** Use ReBAC strictly for identity-to-resource topology.
2. **Don't query foreign databases inside OPA rules.** Pass contextual data in the input payload, or evaluate policy at the boundary where data is already available.
3. **Never separate your list queries from your authorization model.** If your authorization architecture cannot explain how a paginated table of 100,000 items is rendered in $< 50$ms, the architecture is incomplete.
4. **Treat database scoping as a first-class tier.** Use compiled query filters or RLS for bulk reads, and use ReBAC/ABAC engines for point reads and state mutations.
