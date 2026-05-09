# Mushafi — Claude Code Project Briefing

> Read this fully before touching any file. Read docs/architecture.md and docs/data-model.md for full detail.

---

## What This Is

A Quran annotation app for students of hifz (memorization) and tajweed.

**Core interaction:** tap one or more words in an ayah → attach a categorized note → see color-coded highlights across the full Quran → search and review notes by category.

**Who uses it:** Quran students who currently write notes in physical notebooks — mistakes in memorization, tajweed errors, waqf marks. This app replaces that notebook with structured, searchable, color-coded annotations directly on the Quran page.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL, Redis |
| Mobile | TypeScript, Expo SDK 51+, React Native, Expo Router, Zustand, React Query |
| Shared types | TypeScript package (`packages/shared-types`) |
| Auth | Supabase Auth (email + Google login) |
| Infra (local) | Docker Compose (PostgreSQL + Redis) |

---

## Our Database Stores ONLY

1. **User** — account info + preferences (preferred reciter, tafseer)
2. **Category** — self-referencing tree (unlimited nesting), global defaults + user-defined
3. **Annotation** — surah_number, ayah_number, word_start, word_end, category_id, note_text, severity, is_resolved, source

**We never store Quran text, audio, or translations.** Those come from the Quran Foundation API.

---

## Primary External API: Quran Foundation

All Quran content is fetched from the Quran Foundation API and cached in Redis (24h TTL).

- **Base:** `https://api.qurancdn.com/api/qdc`
- **Docs:** https://api-docs.quran.foundation
- **All external calls go through `quran_service.py` only** — never call the QF API directly from a router or component

Key capability: audio endpoint with `?segments=true` returns `[word_index, start_ms, end_ms]` per word. This enables playing only the selected word range without any audio processing on our side.

---

## Word Addressing

Every word is addressed as `surah_number:ayah_number:word_position` (e.g. `2:255:3`).
This is the Quran Foundation standard. **Do not invent custom word IDs.**

In the DB we store as three plain integers: `surah_number`, `ayah_number`, `word_start`, `word_end`.
`word_start` and `word_end` are always within the same ayah (MVP constraint).

---

## Default Categories (seeded in DB)

```
حفظ  (hifz)         — color: #ef4444  — memorization errors
  ├── حذف كلمة, إبدال كلمة, زيادة كلمة, خطأ في الترتيب

تجويد (tajweed)      — color: #8b5cf6  — tajweed errors
  ├── غنة, مد (with children), إدغام, إخفاء, إقلاب, قلقلة

وقف وابتداء (waqf)  — color: #0d9488  — stopping/starting rules
  ├── وقف لازم, وقف جائز, وقف ممنوع, وقف مرخص
```

Global categories (scope=global) cannot be deleted. Users add their own freely.

---

## Critical Conventions

### Backend
- Use **async** SQLAlchemy everywhere — never sync sessions
- Routers handle HTTP only — all business logic in `services/`
- All Quran Foundation calls in `quran_service.py` only, with Redis caching
- Use Pydantic v2 models for all request/response schemas
- Every endpoint requires authentication (JWT from Supabase)
- Write tests for all service layer functions

### Mobile
- Arabic text uses **KFGQPC Hafs Uthmanic** font (loaded via expo-font). Never use system Arabic fonts.
- RTL layout for all Arabic text — set `writingDirection: 'rtl'` and `textAlign: 'right'`
- Word selection state lives in **Zustand** (`selectionStore.ts`)
- Server data (annotations, categories, quran pages) via **React Query** hooks in `src/hooks/`
- Never call the API directly from components — always through hooks
- Bottom sheet for annotation input (use `@gorhom/bottom-sheet`)

### General
- All money/user data stays in our DB. Quran content never touches our DB.
- `is_resolved` field is important — it lets students mark mistakes as corrected
- `severity` field (info/warning/critical) enables prioritized review
- Offline mode is v2 — don't design for it in MVP

---

## What NOT to Do

- Do not store Arabic Quran text in our PostgreSQL database
- Do not build custom auth — use Supabase Auth
- Do not create your own word position IDs — use Quran Foundation's scheme
- Do not call the Quran Foundation API from routers or React components directly
- Do not use system fonts for Arabic text rendering
- Do not add v2 features (Tarteel AI, offline mode, cross-ayah selection, sharing) in MVP

---

## MVP Feature Scope

- [ ] Quran page view, word-by-word rendering with Uthmanic font
- [ ] Tap to select one or more words within an ayah
- [ ] Add annotation: pick category (nested tree) + optional note + severity
- [ ] Color-coded word highlighting on page (one color per category)
- [ ] Annotation list with filter by category/subcategory + search
- [ ] Mark annotation as resolved
- [ ] Word meaning popup (from Quran Foundation word endpoint)
- [ ] Play audio for selected word range (using QF segments timestamps)

---

## Reference Files

- `docs/architecture.md` — full system diagram, folder structure, API contract
- `docs/data-model.md` — all tables, indexes, schemas, SQLAlchemy models, TypeScript types