# Laplace-MCP

Laplace-MCP is a separate repository, `SaltyPatron/Laplace-MCP`, at `/repos/src/Laplace-MCP`. It is an HTTP service in front of the built engine and the loaded database. It is not one of the five repositories this Reference otherwise documents, and it does not add commands to `laplace`.

The process maps tier 0 and names an entity with `lp_text_parts`. The caller sends the text or an ID it already holds. The process holds `LAPLACE_CONNINFO` and calls the installed functions. The contract and the measurements are in that repository's `docs/API.md`.

What the process serves: `POST /v1/embeddings` (the entity, not a float vector), `POST /v1/search` (`laplace_containers` and `laplace_claims` on one ID), `POST /v1/forward` (`laplace_forward`), `POST /v1/shape` (`laplace_frechet4d` on linestrings of stored `entity.coord`), `POST /v1/ingest` (`laplace ingest` on an absolute path). nginx `laplace-managed` proxies `POST /mcp` to the same bodies with an `op` field. `GET /v1/surface` lists this.

Measured on the loaded database while that service was being stood up: `Sherlock Holmes` is `d91895c654f33a108a63bb64f10ca69f`, named in under a millisecond once tier 0 is mapped. Search of that ID returned six containers and three claims (part of speech, the Open English WordNet lexical entry, the sense). The container function alone executed in 3.96 ms. Containers and claims together took 244 ms in `psql` and about 205–255 ms on the service. Fréchet of the phrase against itself was 0. Fréchet against `Holmes` was 0.221. Ingest of one 43-byte text file exited 0 in 0.2 s and the file trunk came back as a container of those exact bytes.

The engine's other commands, and the reads specified past them (translate, degrees, pull, turn, gaps, DTW, EDR, Fréchet with skipped vertices, the forward stages), are not routes of this service yet. `laplace_fills` is the parent walk inside `laplace fills`, so the service does not expose that function as the continuation report.
