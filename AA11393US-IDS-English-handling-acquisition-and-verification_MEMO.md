# AA11393US — English-Language Handling of Foreign IDS References: Acquisition and Verification Memo

> **CURRENT-STATE MEMORANDUM · 8 AUGUST 2026 · NOT FOR FILING**
>
> This memorandum records the current English-language handling artifacts obtained for the
> foreign IDS references B1, B5, B6, and B10, their acquisition provenance, the governing
> registration records, and the procedure an auditor may follow to re-verify correctness
> independently. It does not constitute an IDS, a filing, a translation certification, or a
> legal opinion; filing compliance and materiality determinations remain for US counsel.

## 1. Purpose and design note

This document exists so that an auditor can verify that the machine translations and
English-family copies added on 8 August 2026 are (a) what they claim to be, (b) coherently
declared in the governing registries, and (c) reproducible from primary sources. It states
only current operative evidence and owners; it retains no revision history, in accordance
with the repository live-status-only discipline in [`AGENTS.md`](AGENTS.md). The canonical
records of current state are the per-package `source-manifest.json` files and
`structured_source/registry/content.json`; this memo derives from and cross-references them
and does not establish a second source of truth.

The relevant public-rule context is 37 CFR 1.98(a) and MPEP § 609.04(a); the USPTO does not
verify machine-translation accuracy ("There is no requirement for the translation to be
verified, including reliable machine translations"), and consideration of an IDS turns on
compliance with 37 CFR 1.97, 1.98, and 1.33, not on translation quality.

## 2. Current artifact inventory

All listed raw digests are copied from the canonical `source-manifest.json` entries; an
auditor recomputes them from the bytes on disk and must obtain the same values. `fileId`
identifies the file entry in `structured_source/registry/content.json`.

| Package | Artifact (relative path) | Role | Size (bytes) | RAW SHA-256 (sha256/raw) | Registry fileId |
| --- | --- | --- | ---: | --- | --- |
| B1 | [`prior-art/B1/convenience/B1_CN117278762A_English-machine-translation_Espacenet_2026-08-08.pdf`](prior-art/B1/convenience/B1_CN117278762A_English-machine-translation_Espacenet_2026-08-08.pdf) | non-authoritative English machine translation | 309859 | `67d4cdb4b870cbb1b54de4e4fe50e4796a05157b6baa6b0bc982c7c56f4c833d` | `file-b33a996459ca68a96045fa5e` |
| B5 | [`prior-art/B5/convenience/B5_CN202455480U_English-machine-translation_Espacenet_2026-08-08.pdf`](prior-art/B5/convenience/B5_CN202455480U_English-machine-translation_Espacenet_2026-08-08.pdf) | non-authoritative English machine translation | 77343 | `cb8dbcd2d3a19d06224f3ef53357f03dfc3269391b3e39898b0d9740f085b67d` | `file-67dd17fdcd389ece01bbe3ec` |
| B6 | [`prior-art/B6/convenience/B6_US20050175224A1_English-language-equivalent.pdf`](prior-art/B6/convenience/B6_US20050175224A1_English-language-equivalent.pdf) | English-language family-member copy (US 2005/0175224 A1) | 1799413 | `4b3e8447445655571bbc22a270ffff5a25bac191bb97fdefd7e400d08c75e73a` | `file-39315e5b0e99ad6e42916cde` |
| B6 | [`prior-art/B6/convenience/B6_US7382905B2_English-language-family-grant.pdf`](prior-art/B6/convenience/B6_US7382905B2_English-language-family-grant.pdf) | English-language family-member copy (US 7,382,905 B2) | 1858754 | `9ea4f1ed440011e57e425b5096366328433916fb8e27c5f1ebd494fab4a14430` | `file-3e509f8bd785ffd050f8c15b` |
| B10 | [`prior-art/B10/convenience/B10_KR20240168593A_English-machine-translation_Espacenet_2026-08-08.pdf`](prior-art/B10/convenience/B10_KR20240168593A_English-machine-translation_Espacenet_2026-08-08.pdf) | non-authoritative English machine translation | 110474 | `f527fd0f197d652eac99d8495dc344163ae0407a76f919fd62e1b3b4b18faa0e` | `file-460df53fa96a0c66561c9fac` |
| B10 | [`prior-art/B10/convenience/B10_US20240397167A1_English-language-family-member.pdf`](prior-art/B10/convenience/B10_US20240397167A1_English-language-family-member.pdf) | English-language family-member copy (US 2024/0397167 A1) | 478412 | `d008fa8cad9444c4674a695c6313589768be004cdb497601d341cbf560585513` | `file-d8cbfe88011cc571f68c2399` |

Each entry is also declared with role `non-authoritative-text-aid` in the `convenienceDerivatives`
array of the corresponding package manifest — [`B1`](prior-art/B1/source-manifest.json),
[`B5`](prior-art/B5/source-manifest.json), [`B6`](prior-art/B6/source-manifest.json), and
[`B10`](prior-art/B10/source-manifest.json) — and as a `convenience-derivative` file entry
referenced by that package's `convenienceFiles` in the content registry. The single permitted
derivative role is enforced by `structured_source/verify.py` (role check
`non-authoritative-text-aid`).

## 3. Acquisition provenance

Retrieval date for every artifact: 8 August 2026. All machine translations were extracted
programmatically from the English-language machine-translation display on the EPO Espacenet
publication page (the display carries Espacenet's own notice: "The wording below is an
initial machine translation of the original publication"), reformatted into a readable PDF
without editorial changes, and carry a cover note stating that the document is not
represented as a certified or authoritative translation and that the original publication
is submitted separately.

| Artifact | Source | Retrieval evidence in the artifact itself |
| --- | --- | --- |
| B1 CN 117278762 A MT | `https://worldwide.espacenet.com/patent/search/family/089200232/publication/CN117278762A` | Cover note + title page + 30-page text (abstract, description, claims) |
| B5 CN 202455480 U MT | `https://worldwide.espacenet.com/patent/search/family/046871301/publication/CN202455480U` | Cover note + 4-page text (abstract, description, both claims) |
| B10 KR 2024-0168593 A MT | `https://worldwide.espacenet.com/patent/search/family/093564491/publication/KR20240168593A` | Cover note + 7-page text via Espacenet Global-Dossier translation |
| B6 US 2005/0175224 A1 | official USPTO publication scan via Google Patents `patentimages`, URL `https://patentimages.storage.googleapis.com/13/5a/c4/fd3282f72725b9/US20050175224A1.pdf` | 21-page official PDF; identity spot-checked on title, front-page figure, and abstract against the stored CN transcription |
| B6 US 7,382,905 B2 | official USPTO publication scan, URL `https://patentimages.storage.googleapis.com/4b/65/fe/68d0bcac41c32a/US7382905.pdf` | 22-page official PDF; first page reads "US 7,382,905 B2 / Venkatesan et al. / DESYNCHRONIZED FINGERPRINTING METHOD AND SYSTEM FOR DIGITAL MULTIMEDIA DATA" |
| B10 US 2024/0397167 A1 | official USPTO publication scan, URL `https://patentimages.storage.googleapis.com/dc/f4/1a/97e2a1f8c0364a/US20240397167A1.pdf` | 9-page official PDF; Google Patents title "Object attribute-based watermarking method for preventing leakage of digital content" |

Verification performed at acquisition: page count and file-type checks (`pdfinfo`, `file`),
first-/last-page text extraction (`pdftotext`) for identity confirmation, and — for the
machine translations — byte-for-byte agreement with the Espacenet display at retrieval
time. Formal equivalence between the CN family members and the US family copies remains a
counsel determination (see § 6).

## 4. Discovery recorded during acquisition

Espacenet bibliographic data for B10 list US 2024/0397167 A1 and US 12,598,365 B2 in the
same family ("Published as"), which the [IDS reference list](US/common/ids/AA11393US-US_IDS-reference-list_DRAFT.md)
did not previously record (it noted only a possible CN family member). Because an
English-language family member is readily available, 37 CFR 1.98(a)(3)(ii) makes its
submission effectively required if the KR publication is cited; the US application copy was
therefore added. The IDS reference list row for B10 is an open update (owner: applicant,
for counsel review).

## 5. Independent auditor verification procedure

1. **Byte identity.** Recompute the RAW SHA-256 of each artifact in § 2 with
   `shasum -a 256 <path>` (or equivalent) and confirm the value matches the listed digest,
   the digest in the package `source-manifest.json` entry, and the `size`.
2. **Registration coherence.** Confirm each artifact path appears in
   `structured_source/registry/content.json` `files` with the `fileId` above and role
   `convenience-derivative`, and that its `fileId` is listed in the `convenienceFiles` array
   of the matching package (`us-prior-art-b1`, `us-prior-art-b5`, `us-prior-art-b6`,
   `us-prior-art-b10`).
3. **Aggregate gate.** Run, from the repository root:
   `uv --no-cache --offline run --locked --no-sync python -m navigator validate-current`
   and confirm `status: "passed"`. A pass is ephemeral technical status; it does not verify
   translation content.
4. **Translation spot-check.** Open each machine-translation PDF and compare the abstract,
   description, and claims against the live English display on the Espacenet publication
   page listed in § 3 (Espacenet regenerates the same machine translation).
5. **Official-copy spot-check.** Confirm each US scan in § 3 is the document identified by
   its publication number on Google Patents or the USPTO patent search system.
6. **Content-completeness check.** Confirm each machine-translation PDF covers abstract,
   description, and claims, and that each reference's original non-English PDF remains
   stored as the package's `storedSource` (B1, B5, B6, B10 source-manifest entries), because
   37 CFR 1.98(a)(2) requires the legible copy of the foreign document in addition to any
   translation.

## 6. Open gates and owners (operative status)

| Gate | Owner | Status and next action |
| --- | --- | --- |
| Concise explanations of relevance for B1, B5, B10 (and prudentially B6) | US counsel | Not yet drafted; counsel-approved text required before IDS assembly |
| B6 family-member selection (grant CN 100583750 C vs pre-grant CN 1655500 A) and formal equivalence of the US copies | US counsel | Open; the stored US scans support either selection for the disclosure |
| B10 IDS list update with US family members; decide citation set (KR and/or US members) | Applicant with US counsel | Open |
| PCT/DO/EO/903 national-stage check for B1, and print-on-face (PTO/SB/08) decision | US counsel | Open; ISR-route consideration does not print cited references on the patent face |
| Final PTO/SB/08 assembly, timing under 37 CFR 1.97, signature under 1.33(b) | US counsel | Open; not part of this memo |

## 7. Boundaries

- The machine translations are non-authoritative aids; nothing in this memo represents them
  as certified or as official translations, and the artifacts themselves carry that label.
- This memo does not assert that the USPTO will "accept" any translation: acceptance of an
  IDS is determined by 37 CFR 1.97/1.98/1.33 compliance of the submission as a whole.
- The aggregate validation boundary from the repository [README](README.md) applies: human
  review of source evidence and substantive analysis remains authoritative.