# 16. Authority

Knowledge, authority, and compute are three independent axes: what exists in the one world, what a principal may do with which part of it, and how much work one operation may spend, resolved as an explicit effective scope before any cognition couples.

One knowledge world does not mean every principal has authority to use every part of it, and a cheaper request is never a dumber Laplace. Governance is not deletion of knowledge: a fact stays known and attributable while the current principal lacks authority to couple, derive, realize, export, or execute it. Standing and permission are distinct variables. This stage exists before the firmware and the forward program because the program resolves its authority boundary at its first operation, and forbidden state must not enter cognition and then be hidden at the end.

## Before this stage

[15. Web](Web.md): the world that authority is scoped over. [12. Attestations](Attestations.md): grants are themselves witnessed relations.

## Operations

### 16.1 Separate the three axes

- **In:** a request.
- **Do:** keep apart: knowledge, what canonical structures, observations, testimony, and calculations exist; authority, which parts of that world this principal may discover, inspect, search, couple, traverse, derive, realize, persist, export, execute, or delegate; compute, how deeply and broadly one operation may search the authorized world, [17. Envelope](Envelope.md). Commercial tiers change the envelope, not the amount of world Laplace is allowed to know. More compute never grants knowledge; less compute never means a knowledge-reduced model.
- **Out:** three inputs to the program, never one.
- **From:** `docs/CAPABILITIES.md` §One world, three independent boundaries; `docs/INVENTION.md` §16; `docs/INVENTIONS.md` #91, #108.

### 16.2 Declare knowledge packages

- **In:** the world of [15. Web](Web.md).
- **Do:** a knowledge package is a content-addressed authority manifest over the shared world, not a duplicated smaller model: a Grade 7 mathematics curriculum, a Formula 1 engineering corpus, an employer's private project, a department's procedures, a personal history, a temporary incident scope. A package may contain other packages. Inheritance follows explicit authority and package relations, never arbitrary semantic connectivity: a Formula 1 package includes its declared engineering subtree and does not grant missile knowledge because both connect through fluid dynamics. A package may recommend or ship a matching perf-cache profile of [7. Perfcaches](Perfcaches.md) operation 7.4 for deployment economics; the two objects stay distinct, removing a cache module revokes nothing, and revoking a grant rewrites no cache.
- **Out:** the packages this deployment can grant.
- **From:** `docs/guides/knowledge-authority.md` §Knowledge packages and §Knowledge package versus cache profile; `docs/INVENTIONS.md` #109.

### 16.3 Declare the capabilities

- **In:** the operations a principal can perform.
- **Do:** capabilities are separate from scope and separately grantable: DISCOVER, know that a scope or entity exists; INSPECT, retrieve explicit content; SEARCH, locate members; COUPLE, allow state to influence cognition; TRAVERSE, follow authorized relations; DERIVE, calculate new knowledge; REALIZE, disclose or render a result; PERSIST, save derived state; EXPORT, take state outside the current boundary; EXECUTE, cause an external action; DELEGATE, grant authority to another principal. A user may reason from private material but not export it; an analyst may discover a restricted scope but not inspect it; an agent may propose a deployment but not execute it. Tenant owner, admin, and member roles are workspace administration; knowledge authority is a richer layer over the substrate.
- **Out:** the capability mask vocabulary.
- **From:** `docs/guides/knowledge-authority.md` §Capabilities; `docs/INVENTIONS.md` #110.

### 16.4 Resolve the effective scope

- **In:** the principal, and the request.
- **Do:** the effective operation boundary is the intersection of the tenant and world boundary, the principal's identity, its role and relationship authority, its knowledge-package grants, the active caller-selected scope, its capability grants, and kernel, organization, and user governance. The boundary is part of execution state and of every receipt. Tenant scope is authorization and isolation; it is not semantic source trust, and participant, model, tool, corpus, analyzer, and feedback sources retain distinct source identities inside a tenant.
- **Out:** one effective scope for this operation.
- **From:** `docs/guides/knowledge-authority.md` §Effective authority; `docs/specs/37_Substrate_Operation_ISA.md` §Authority / knowledge-scope contract; `docs/specs/34_Conversational_Provenance.md` §Identity hierarchy.

### 16.5 Enforce before coupling, and again at the act

- **In:** the scope of 16.4.
- **Do:** authority is enforced at the point where the capability matters: RESOLVE binds the principal, grants, and policy; COUPLE admits authorized cognition inputs only, so that a forbidden source never influences a result that is then merely redacted; DERIVE checks calculation authority; SELECT checks act eligibility; REALIZE checks disclosure authority; PERSIST checks write authority; EXPORT checks boundary crossing; EXECUTE checks external action. Permission to couple does not imply permission to export or execute. Unauthorized cached records, from a mapped perf-cache, cannot enter COUPLE either.
- **Out:** the operations of [20. Forward](Forward.md) each carrying their own check.
- **From:** `docs/guides/knowledge-authority.md` §Enforcement must precede redaction; `docs/specs/36_Laplace_Forward_Pass.md` §COUPLE and §SELECT.

### 16.6 Dispose explicitly

- **In:** the request, the evidence, the effective authority, the governance.
- **Do:** the decision is allow, deny, abstain, or require stronger authority, and it is receipted with the authority or policy root that made it. Laplace can therefore distinguish unknown, unsupported, ambiguous, resource-exhausted, known but not authorized to couple, authorized to couple but not realize, authorized to inspect but not export, and authorized to propose but not execute. Saying that a secret exists can leak information, so even disclosure that restricted knowledge exists may require DISCOVER. A permission decision is not a popularity vote and is never smuggled into canonical identity.
- **Out:** the disposition, in the receipt.
- **From:** `docs/CAPABILITIES.md` §Governance does not erase knowledge; `docs/guides/knowledge-authority.md` §Honest abstention; `docs/INVENTIONS.md` #111.

### 16.7 Separate belief, risk, and action

- **In:** any act with consequences.
- **Do:** "What do I believe?" is standing; "What could go wrong?" is the evidence about consequences, itself knowledge; "What am I authorized to risk?" is authority. They are three separate questions, and the second never answers the third.
- **Out:** three separate inputs to STEER and SELECT.
- **From:** `docs/INVENTOR_RECORD.md` §Gödel engine, OODA, personality firmware, 2026-08-17.

### 16.8 Run Red Spear, Blue Shield, White Judge over the same model

- **In:** the deployment.
- **Do:** Red Spear performs authorized adversarial exploration: privilege and scope escalation, cross-tenant leakage, confused-deputy paths, stale or transitive grants, inference leakage, restricted derivation, export and execute bypasses. Blue Shield enforces effective authority at the actual cognition and action boundaries of 16.5. White Judge is explicit, deterministic adjudication over policy, authority, provenance, and evidence with WHY and WHY_NOT receipts; it is not a hidden model that votes on Red versus Blue outputs.
- **Out:** a security posture over the same explicit world.
- **From:** `docs/CAPABILITIES.md` §Red Spear, Blue Shield, White Judge; `docs/INVENTIONS.md` #112.

### 16.9 Bind entitlement as an external witness

- **In:** a support provider such as Patreon.
- **Do:** the provider does not become Laplace. It is an external witness that says this account is currently entitled to this membership tier, and Laplace applies its own versioned entitlement policy to that fact: support provider → verified entitlement → Laplace privileges. Payment does not become knowledge, ownership, governance, or authority.
- **Out:** the principal's entitlement, as a witnessed fact the policy reads.
- **From:** `docs/INVENTOR_RECORD.md` §Product, Patreon post 2, 2026-08-26.

## What this stage leaves behind

For every principal, an effective scope and a capability mask that the forward program binds at its first operation and re-checks at every act, and a personal effective mind composed of the shared world, licensed and institutional grants, private knowledge, witnessed experience, governance and firmware, the active scope, and the compute envelope, without training a model per person.

## Without this stage

Every request sees the whole world, restricted knowledge is either deleted or leaked, a cheaper tier has to be a dumber model, and no abstention can say why.
