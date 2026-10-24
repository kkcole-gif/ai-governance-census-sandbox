# User Guide: AI Governance Census of US Colleges and Universities

Draft, October 24, 2026. This guide explains what the dataset records, how to read it, and how to cite or correct it. A separate methods page documents the sampling frame, the search protocol, and the coding procedure.

## 1. What the census records

The census records the documents through which US colleges and universities govern the use of artificial intelligence by students, faculty, and staff. The sample of 334 institutions comes from the 2025 Carnegie Classifications (seed 20261023). Every R1 institution is included, and the other strata are drawn at random (see the README for the stratum table).

The unit of record is the document, and documents nest within institutions. One institution carries anywhere from no documents to more than twenty, because AI rules at a single university sit in provost memos, honor codes, teaching center pages, IT standards, library guides, license announcements, and school policies, and these documents often disagree with one another. The dataset keeps every such document as a separate row so a reader sees where each rule lives, who issued it, and whom it addresses.

## 2. What counts as a document

A document enters the inventory when it passes all four tests.

1. Institutional authorship. A university office, committee, senate, school, library, teaching center, IT unit, student conduct office, student government, or system office issued it. An individual instructor's syllabus or blog does not qualify. The issuing office is read from the document itself, never from the hosting domain.
2. Governance function. The document tells readers what to do, what is permitted or required, or what the institution has decided. FAQs, syllabus statement templates, decision trees, and task force reports with recommendations qualify. News stories, webinars, and research publications do not. Where a news item reports guidance, the census traces the reported guidance to its source document and records the source.
3. AI as object. The document addresses the use of AI tools, whatever term it uses (generative AI, artificial intelligence, a named product). An integrity code with no mention of AI fails this test, and the institution log records it as an absence, because the absence is itself a finding.
4. Public availability. The document is reachable without a login. Documents identified behind a login are recorded with the status Located behind login and do not enter reported figures.

Each document is also coded Standalone (AI is its principal subject) or Embedded (an AI clause inside a general instrument such as an honor code, catalog policy, handbook, or acceptable use policy).

## 3. Status: what has and has not been read

Every row carries one status. Only rows marked Verified enter reported figures.

| Status | Meaning |
| --- | --- |
| Verified | Title, issuing office, date, and quoted passage confirmed against the source document. |
| Found | A searcher located and read the document. It awaits verification. |
| Flag | A searcher located the document, but one of the four tests or a field value is in doubt. The Notes field states the doubt. |
| Located behind login | The document exists, but reading it requires institutional credentials. |
| Not reachable | The document exists, but the site blocked reading it. |
| Dead link on recheck | The document was verified once and was unreachable on a later check. |
| Excluded (news) | A news item reporting guidance. It is kept so the trace to the source document stays visible, and it never enters counts. |

Unverified rows stay in the data so a reader sees what has been searched and what remains open.

## 4. Institution-level counts

Institution figures are reported as three nested counts, always named:

1. Institutions with any qualifying document.
2. Institutions with at least one standalone document.
3. Institutions with a formal policy or regulation naming AI.

Institutions governed only by a system-office document (a state system policy with no campus instrument) are counted separately within the third count, because a system mandate and a campus policy are different institutional facts.

The institution log records, for every drawn institution, the search date, the result (Documents found, No AI governance document located, Announced with no document, or Located but not retrievable), and the absences checked. An institution with no qualifying document stays in the data with its log entry.

## 5. Fields in the inventory

| Field | What it records |
| --- | --- |
| UNITID | IPEDS identifier from the Carnegie file |
| Institution | Carnegie name of the institution |
| Stratum | Sampling stratum (1 R1 census through 8 existing corpus) |
| Document title | Title as the document gives it, with a descriptive title in parentheses where none is given |
| Issuing office | The issuing office, from a controlled list, with Other (named) for anything outside it |
| Document type | One of twelve types, from 1 Executive communication to 12 Strategic initiative |
| Boundary case | Yes where the document sits at the edge of a test, with the reason in Notes |
| Standalone or embedded | See section 2 |
| Date issued | Earliest date the document carries |
| Date basis | How the date was established: stated, file path, page metadata, inferred, or undated |
| Date last revised | Latest revision date, where one is given |
| Wave | Wave 1 (issued spring to fall 2023), Wave 2 (issued or revised 2024 onward), Both, or Undetermined |
| Post-July-2026 | Yes where issued or revised after July 2026 |
| AI term used | The terms the document uses for AI |
| Contradiction with another document | Any conflict between this document and another at the same institution, named specifically |
| URL | Address at retrieval |
| Format | HTML, PDF, DOCX, and so on |
| Language | Language of the document |
| Key Framing Language | One sentence quoted from the document |
| Quote source | How the quotation was obtained; "Fetch (verify)" marks a quotation not yet checked against the source |
| Named frameworks | Frameworks, laws, or standards the document cites |
| Vendor named | AI products or vendors the document names |
| Retrieval date | Date the document was read |
| Status | See section 3 |
| Found by | The search step locating it |
| Policy stance (open) | A short description of what the document permits, requires, or prohibits |
| Notes | Anything a reader needs to interpret the row |
| Batch | The search batch producing the row |

The Contradiction field deserves particular attention. Universities often state different default rules for AI use across their own documents (a provost policy permitting use by default while a school catalog prohibits it, for example). The census records each such conflict at the row level so the conflicts are countable.

## 6. The specification scale

Verified documents are scored on three levels of AI literacy, each rated High, Medium, or Low.

- Conceptual: how far the document describes the system itself (what AI is, how training and output relate, error properties).
- Structural: how far it specifies conditions in place before any user arrives (training data, ownership and vendor control, license terms, retention, whether user data trains the model, labor and environmental costs).
- Operative: how far it equips a reader to decide, in a situation, whether to act, withhold, or refuse, and to answer for the decision.

A document addressed to the person who decides, with stated grounds, is eligible for High on the operative level. A document telling its reader someone else decides stays at Medium. Each scored document also records its primary and secondary addressee (Students, Instructors, Staff, Administrators and units, or Institution-wide) and, where operative is High, its grounds (Compliance, Learning, Accuracy or access, or Both). The codebook in this folder gives the full rules.

## 7. How to cite

Cite the version you used through its Zenodo DOI, which appears on the repository page once version 1.0 is released. Each release receives its own DOI. A concept DOI always resolves to the latest version. The CITATION.cff file gives the current citation in machine-readable form.

The CC BY 4.0 license covers the compilation, coding, and documentation. Quoted passages remain the work of their issuing institutions and appear in short excerpt for research and criticism.

## 8. Corrections and missing documents

Institutions revise their AI documents often. To report a correction, a newer version, a broken link, or a document the census missed, use the [reporting form](https://docs.google.com/forms/d/e/1FAIpQLSfK8B4oqRNt_kNkRTaDm8G2Kt-vkDXZmajS4jcLUX75kF_O6w/viewform). For other questions, write to kkcole2@ncsu.edu. Each report is checked against the source document before the data changes, and changes appear in the next release.
