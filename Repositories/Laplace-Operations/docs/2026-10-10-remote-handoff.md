# Remote work and deployment status — 2026-10-10

## Machine roles and current priority

The user clarified that hart-desktop will be the primary development machine.
Development may continue on hart-server; it also serves as the dev/BAT/QA/staging
deployment target. hart-cloud and hart-prod are production. The immediate request
is to account for Laplace work wherever it lives and verify its remote preservation,
including home folders, temporary directories and agent worktrees. Unrelated
projects are excluded. This does not authorize removing development tools or working copies
from hart-server. The server's GTX 1080 Ti remains off limits due to broken cooling.

## Explicit scope and record of the mistaken expansion

The user's direct clarification is: "Your focus is Laplace, not my entire fucking
machine". The subject is Laplace; the locations include agent worktrees, home
folders, temporary directories and other places where Laplace work may exist.
This does not authorize inventorying or exporting every unrelated project.

Operations PR73 incorrectly characterized whole-machine work as the user's explicit
instruction. Scratch PR3 repeated that claim. Those changes were agent-authored
misinterpretations, not a valid expansion of scope. This correction preserves their
Git history and the existing source/recovery artifacts while replacing that operative
instruction. The original conversation remains evidence of what was actually said.

The stopped broader pass was outside the clarified scope; its partial output is recorded for accountability, not as work to resume. Re-reading its saved reports at 20:12 UTC found:

| Evidence | Observed result | What it does not establish |
| --- | --- | --- |
| `machine-recovery/manifest.json` | 389 locally verified Git bundles, 1,575,337,640 bytes; 7 empty repositories recorded | Remote upload, all uncommitted files, or complete machine coverage |
| `machine-git-inventory.jsonl` | 3,537 Git locations classified before interruption | Every Git location or every source file accounted for |
| `machine-history-screen.json` | 674 repositories screened; 64 with candidate pattern matches | Confirmed exposed credentials or an exhaustive secret audit |
| Process readback | The three named inventory/recovery jobs are not running | Completion of their work |

Those reports and bundles are under `/repos/build/audit-scratch` on hart-server.
The broader bundles have not been uploaded. The earlier Laplace recovery refs and
snapshots listed below are separately preserved remotely. No new bulk export was
started to make this correction. Do not resume unrelated-project export. Protected-directory coverage for Laplace work remains incomplete.

## Remaining work and acceptance criteria

1. Reconcile discovered Laplace work against the actual remote objects/refs or protected
   backup objects. Record the source location, exact content/revision, destination,
   verification result and outstanding gap. Cached refs and a local bundle are not
   sufficient evidence of remote preservation.
2. Within Laplace scope, account separately for uncommitted/ignored source, broken Git pointers, agent
   worktrees, loose files, configuration and protected material. Do not silently
   classify everything outside Git as disposable or put credentials into source
   repositories. Discovery errors remain explicit coverage gaps.
3. Review unfinished changes against the invention documents and implementation
   contracts before integrating them. Recovery commits are preservation, not
   acceptance into implementation main. Keep the existing source histories.
4. Resume deployment repair against the recorded failure and verify the actual
   application/API/MCP operations promised by the deployment. Compilation, SQL
   connectivity, HTTP health and a running process each prove only that check.
   They do not prove a usable implementation of the invention. Preserve the
   separation of highway generation, ingestion and deployment required by the user.
5. Keep exact source, merged, installed and verified revisions distinct, and record
   deployment ordering, failure recovery and remaining operational blockers. The
   later sections retain dated observations rather than claim current completion.

The historical-log review, billing/trial figures and other infrastructure tasks
below remain outstanding. This correction does not claim that all expected work is
complete or that a successful build proves Laplace's intended capabilities.

## Remote preservation verified around 19:07 UTC

All local branch tips in the 15 `/repos/src/Laplace*` repositories are represented
by a GitHub branch or already contained in origin/main. Live `git ls-remote --heads`
was used as well as local ancestry checks: several checkouts fetch only main, so
absence from cached remote refs does not establish absence from GitHub.

The following existing recovery branches were pushed without merging their changes:

| Repository | Branch | Commit |
| --- | --- | --- |
| Laplace-Refactor | found/copy-453 | 1ea4d70f |
| Laplace-Refactor | found/copy-461 | 2d35a3b8 |
| Laplace-Research | found/copy-462 | 825946c |
| Laplace-Scratch | found/copy-463 | fae763c |

Laplace's `vertex-agent-provider` at `6c5c128` was already on GitHub. Its changes
have not been accepted into main or deployed by this audit.

The separate historical snapshot `/repos/src/Laplace_Hartonomous-Old` had no
remote. Its 356 files were preserved in a new **private** repository,
[SaltyPatron/Laplace_Hartonomous-Old](https://github.com/SaltyPatron/Laplace_Hartonomous-Old),
at `5fe9c9e`. This is distinct from the existing repository ending in a hyphen.
No historical snapshot has been promoted into a current implementation.

The registered worktrees of these repositories have no uncommitted source changes.
Laplace-MCP has two untracked compiled ELF files, `native/lpm` and `native/liblpm.so`;
they were left intact and were not added to source control. This statement does not
cover ignored build files, credentials, raw conversation archives, or every other
repository on the machine. Non-Laplace projects are outside the user's clarified
scope; Laplace work must still be checked wherever it lives.
No working directory or archive was deleted by that preservation pass.

## Expanded home, temporary and archived work check

The initial15-repository check did not cover all loose files and archived agent
worktrees. The following results describe the Laplace locations inspected so far;
they do not prove every location containing Laplace work has been covered.

The follow-up found191 candidate checkout locations across home/temp/source/build,
runner and mounted archive locations. It checked146 readable Git object stores,
including detached HEADs, stashes, reflogs and unreachable commits. Forty archived
worktree locations had unusable Git metadata, commonly Windows drive paths; their
source files were checked directly rather than treated as empty or clean.

[The recovery index in Laplace-Scratch](https://github.com/SaltyPatron/Laplace-Scratch/tree/main/recovery/2026-10-10)
records137 recovery branches and293 recovery tags verified against live GitHub
refs. It also preserves217 loose files,1,504 files from broken/unversioned working
trees,14 dirty-checkout snapshots,32 agent note/instruction files and14 readable
host declarations, plus one large scratch C source. Another1,833 loose files and
19,077 selected files from broken/unversioned locations matched already preserved
content. All1,768 manifest-listed file snapshot hashes match the committed bytes.
Original working files remain unchanged. Recovery copies do not establish that
the code is accepted into implementation main or ready for deployment.

Protected homes (`/root`, `/home/hartonomous`) and protected temporary directories
remain uninspected by the unprivileged agent. The user's root inventory attempt
failed because `rg` was missing from sudo's PATH; the original cleanup discarded
partial output. [Scratch PR2](https://github.com/SaltyPatron/Laplace-Scratch/pull/2)
merged the correction: base-system find/grep, prerequisite checks, retained partial
evidence and errors, and failure without replacing a completed report. Restricted-PATH
fixtures and ShellCheck passed; actual protected-root coverage has not completed.
The local script matches the merged source. No repeat execution request was made. The recovery README records
selection boundaries, excluded runtime/data/credential/session files, and the
remaining access limit. Do not claim every Laplace fragment anywhere on disk has
been found or all historical conversations reviewed.

## Completed infrastructure changes and verification limits

- Operations and monorepo permission/setup fixes are merged. Existing credentials
  are preserved by repeat setup; the previous live postgres default password has
  not yet been rotated.
- Operations deployment no longer generates/adopts highway content as an ordinary
  deployment side effect. Staging deployment/checks/reads passed in run38075199422.
- Host operation locking, isolated extension PR installation tests, dependency
  revision capture, deployment readback and required staging reads are merged.
- OpenBao app DB credential refresh is installed and verified on hart-prod using
  its AppRole. Knowledge credentials and shared service credentials remain separate
  unfinished integration work.
- Corrected secrets backup is installed on hart-server. The user's19:00 run passed
  SQLite integrity and Bao snapshot checksum checks. Timer readback is active for
  October11 03:15 UTC. Live restore and off-host recovery have not been established.
- Local API/system MCP and native MCP have passed the endpoint/protocol checks
  recorded in the system audit. Native MCP remains an installed user service;
  automated delivery of that service is unfinished.

## Main is not proof of deployment

Hart-server's application, web and native-library receipts read
`2716c31750fd330a2aa4c0067de6ad792c32ef19`; monorepo main is
`58cab06ee7b460949cb2164cb29b7e24df50c8a5` at this observation.
[Main delivery38078073055](https://github.com/SaltyPatron/Laplace/actions/runs/38078073055)
failed at installation after its build phase: `another deployment or ingest holds
/run/lock/laplace/host-resource.lock`. One retry reproduced this failure at19:06 UTC.
Migration, publication and production were skipped. The lock holder and whether
build-child inheritance caused the conflict are not established. Do not report
latest main as deployed or keep retrying without diagnosing it.

Two open draft PRs were observed: Operations#67 (Windows DNS/backup continuity)
and Engine#44 (Engine behavior). Remote preservation does not establish readiness
of either for main.

Other outstanding work includes public production MCP routing, huge-page usage,
certificate renewal verification, coordinated administrator-credential migration,
production lifecycle/rollback verification, actual trial spend/credit balance,
Azure resource access and the full historical log review. Structural log inventory
and selected-message review are not a completed audit of all conversations.
