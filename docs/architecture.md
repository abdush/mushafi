# Mushafi — Architecture Document

## Overview

Mushafi is a Quran annotation app for students of hifz and tajweed.
The core interaction is: tap one or more words in an ayah → attach a categorized note → see colored highlights across the Quran → search and review notes by category.

The app is designed mobile-first (iOS + Android via Expo React Native) with a lightweight FastAPI backend that stores only user-generated annotation data. All Quran content (text, audio, tafseer, morphology) is fetched from the Quran Foundation API and cached locally.

---

## Monorepo Structure

```
mushafi/
├── CLAUDE.md                          ← Claude Code project briefing (always read first)
├── docker-compose.yml                 ← local dev: PostgreSQL + Redis + API
├── .env.example
├── README.md
│
├── apps/
│   ├── api/                           ← Python FastAPI backend
│   │   ├── CLAUDE.md                  ← backend-specific conventions
│   │   ├── pyproject.toml
│   │   ├── alembic.ini
│   │   ├── alembic/
│   │   │   └── versions/
│   │   ├── app/
│   │   │   ├── main.py                ← FastAPI app entry point
│   │   │   ├── core/
│   │   │   │   ├── config.py          ← settings via pydantic-settings
│   │   │   │   ├── database.py        ← async SQLAlchemy engine + session
│   │   │   │   ├── redis.py           ← Redis client
│   │   │   │   └── auth.py            ← JWT verification / OAuth2 helpers
│   │   │   ├── models/                ← SQLAlchemy ORM models
│   │   │   │   ├── user.py
│   │   │   │   ├── category.py
│   │   │   │   └── annotation.py
│   │   │   ├── schemas/               ← Pydantic request/response schemas
│   │   │   │   ├── user.py
│   │   │   │   ├── category.py
│   │   │   │   └── annotation.py
│   │   │   ├── routers/               ← one file per resource, HTTP only
│   │   │   │   ├── auth.py
│   │   │   │   ├── annotations.py
│   │   │   │   ├── categories.py
│   │   │   │   └── quran.py           ← proxy/cache layer for Quran Foundation API
│   │   │   ├── services/              ← business logic, no HTTP concerns here
│   │   │   │   ├── annotation_service.py
│   │   │   │   ├── category_service.py
│   │   │   │   └── quran_service.py   ← all calls to Quran Foundation API
│   │   │   └── utils/
│   │   │       └── cache.py           ← Redis cache decorators/helpers
│   │   └── tests/
│   │       ├── test_annotations.py
│   │       └── test_categories.py
│   │
│   └── mobile/                        ← Expo React Native (TypeScript)
│       ├── CLAUDE.md                  ← mobile-specific conventions
│       ├── app.json
│       ├── package.json
│       ├── tsconfig.json
│       ├── src/
│       │   ├── app/                   ← Expo Router file-based navigation
│       │   │   ├── (tabs)/
│       │   │   │   ├── index.tsx      ← Quran page view (main screen)
│       │   │   │   ├── notes.tsx      ← annotations list + search
│       │   │   │   └── settings.tsx
│       │   │   └── _layout.tsx
│       │   ├── components/
│       │   │   ├── VerseDisplay/
│       │   │   │   ├── VerseDisplay.tsx       ← renders one ayah, word by word
│       │   │   │   ├── WordToken.tsx          ← single tappable word with highlight
│       │   │   │   └── AyahNumber.tsx
│       │   │   ├── PageView/
│       │   │   │   ├── QuranPage.tsx          ← full page layout, all verses
│       │   │   │   └── PageNavigator.tsx
│       │   │   ├── Annotation/
│       │   │   │   ├── AnnotationSheet.tsx    ← bottom sheet: add/edit note
│       │   │   │   ├── CategoryPicker.tsx     ← nested category tree picker
│       │   │   │   ├── AnnotationBadge.tsx    ← colored dot on highlighted word
│       │   │   │   └── AnnotationCard.tsx     ← note card in list view
│       │   │   └── Audio/
│       │   │       ├── AudioPlayer.tsx        ← plays full ayah or word range
│       │   │       └── WordHighlighter.tsx    ← sync highlight to audio position
│       │   ├── hooks/
│       │   │   ├── useAnnotations.ts          ← React Query: fetch/mutate annotations
│       │   │   ├── useCategories.ts
│       │   │   ├── useQuranPage.ts            ← fetch page words from QF API
│       │   │   └── useQuranAudio.ts           ← fetch audio + word timestamps
│       │   ├── store/
│       │   │   ├── selectionStore.ts          ← Zustand: current word selection state
│       │   │   └── playerStore.ts             ← Zustand: audio playback state
│       │   ├── services/
│       │   │   └── api.ts                     ← typed Mushafi API client (axios)
│       │   ├── constants/
│       │   │   ├── categories.ts              ← default category seeds + colors
│       │   │   └── fonts.ts
│       │   └── types/
│       │       └── index.ts                   ← re-exports from shared-types
│       └── assets/
│           └── fonts/                         ← KFGQPC Hafs Uthmanic font files
│
└── packages/
    └── shared-types/                  ← TypeScript interfaces shared across apps
        ├── package.json
        └── src/
            ├── annotation.ts
            ├── category.ts
            ├── quran.ts
            └── index.ts
```

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Mobile App (Expo RN)                     │
│                                                              │
│  QuranPage → VerseDisplay → WordToken (tap to select)        │
│       ↓                                                      │
│  AnnotationSheet (category picker + note input)              │
│       ↓                                                      │
│  useAnnotations hook → Mushafi API                           │
│                                                              │
│  useQuranPage hook  → Mushafi API /quran/page/:n (cached)    │
│  useQuranAudio hook → Mushafi API /quran/audio (cached)      │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTPS
┌────────────────────────────▼─────────────────────────────────┐
│                   Mushafi API (FastAPI)                      │
│                                                              │
│  /api/v1/annotations  → annotation_service → PostgreSQL      │
│  /api/v1/categories   → category_service  → PostgreSQL       │
│  /api/v1/quran/*      → quran_service     → Redis cache      │
│                                                  ↓           │
└──────────────────────────────────────────────────┼───────────┘
                                                   │ on cache miss
                             ┌─────────────────────▼──────────┐
                             │    Quran Foundation API         │
                             │                                 │
                             │  Content: words, tafseer,       │
                             │           morphology, search    │
                             │  Audio:   recitations + word    │
                             │           timestamps (segments) │
                             │  Auth:    OAuth2 / OpenID       │
                             └─────────────────────────────────┘
```

---

## External APIs

### Quran Foundation API (primary)
Base URL: `https://api.qurancdn.com/api/qdc` (content) and `https://api.quran.foundation` (user/auth)
Documentation: https://api-docs.quran.foundation

Key endpoints used:

| Endpoint | Purpose |
|---|---|
| `GET /verses/by_page/:page` | All verses + words for a Mushaf page |
| `GET /verses/by_key/:key` | Single verse with word details |
| `GET /words/:word_key` | Word morphology, root, transliteration |
| `GET /tafsirs/:tafsir_id/by_ayah/:ayah_key` | Tafseer text |
| `GET /chapter_recitations/:reciter_id/:chapter` | Audio file + timestamps |
| `GET /audio_files/recitations/timestamp_range` | Word-range timestamps (ms) |

**Critical:** Audio endpoint with `segments=true` returns `[word_index, start_ms, end_ms]`
per word — enables playing only selected words without any audio processing.

### Tarteel AI (v2 — recitation checking)
- Real-time recitation error detection via streaming audio
- Integration deferred to post-MVP

---

## Key Architectural Decisions

### 1. We Never Store Quran Text
All Arabic text, translations, tafseer, and audio URLs are fetched from the Quran Foundation API. Our database contains only user-generated annotations. This avoids text accuracy liability and keeps our DB minimal.

### 2. Word Addressing via surah:ayah:position
Every word is universally addressed as `surah_number:ayah_number:word_position` (e.g. `2:255:3`). This is the Quran Foundation standard. Annotation records store `surah_number`, `ayah_number`, `word_start`, and `word_end` as plain integers — no string keys in the DB.

### 3. word_start and word_end Are Same-Ayah Only (MVP)
Cross-ayah word selection is deferred to v2. This simplifies the data model significantly. In practice, notes are almost always about a word or phrase within one ayah.

### 4. Categories Are a Self-Referencing Tree
`parent_id` references the same `categories` table. Depth is unlimited. Three global default categories are seeded at startup. Users can add their own at any nesting level. Global categories cannot be deleted.

### 5. Redis Cache for All External Data
`quran_service.py` caches every Quran Foundation API response in Redis with a 24-hour TTL. Cache key format: `qf:{endpoint_path}:{params_hash}`. This makes the app resilient to API rate limits and network issues.

### 6. Severity + is_resolved for Review Workflow
These two fields make the annotation system useful for structured review. A user can mark mistakes as resolved after correction, filter by severity, and track improvement over time — which is the primary workflow for a hifz student.

### 7. State Management Split
- **Zustand**: local, ephemeral UI state (current word selection, audio playback position)
- **React Query**: server state (annotations, categories, quran page data) with caching and background refresh
- No Redux — unnecessary complexity for this app

### 8. Authentication Strategy
MVP: Supabase Auth (email + Google login). Faster to set up than Quran Foundation OAuth2.
V2: Add Quran Foundation OAuth2 so users can link their Quran.com account and sync bookmarks bidirectionally.

---

## API Contract

All endpoints prefixed with `/api/v1/`. Authentication via Bearer JWT.

### Annotations
```
GET    /annotations                    list (filterable by surah, ayah, category, resolved)
GET    /annotations/:id                single annotation
POST   /annotations                    create
PATCH  /annotations/:id                update / resolve
DELETE /annotations/:id                delete
GET    /annotations/search?q=          full-text search on note_text
GET    /annotations/stats              count by category, resolution rate
```

### Categories
```
GET    /categories                     full tree (global defaults + user's)
POST   /categories                     create user category
PATCH  /categories/:id                 update label/color
DELETE /categories/:id                 delete (only user-owned, only if no annotations)
```

### Quran (proxy + cache)
```
GET    /quran/page/:page_number        words for a Mushaf page
GET    /quran/verse/:surah/:ayah       verse detail
GET    /quran/word/:surah/:ayah/:pos   word detail (meaning, root, morphology)
GET    /quran/audio/:chapter           audio URL + word timestamps for a chapter
GET    /quran/tafseer/:surah/:ayah     tafseer text (default: Ibn Kathir Arabic)
```

---

## Development Setup

### Prerequisites
- Docker + Docker Compose
- Python 3.12+
- Node.js 20+
- Expo CLI (`npm install -g expo-cli`)

### Local Dev
```bash
# Start infrastructure
docker-compose up -d          # PostgreSQL on 5432, Redis on 6379

# API
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head           # run migrations
python -m uvicorn app.main:app --reload

# Mobile
cd apps/mobile
npm install
npx expo start
```

### Environment Variables
See `.env.example` in project root. Key vars:
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string
- `SUPABASE_URL` + `SUPABASE_ANON_KEY` — auth
- `QURAN_FOUNDATION_API_KEY` — if required (check their docs)

---

## MVP Scope (v1)

- [x] Quran page view with word-by-word rendering
- [x] Tap to select one or more words within an ayah
- [x] Add annotation: category + subcategory + optional note text
- [x] Color-coded word highlighting on the page
- [x] Annotation list view with filter by category/subcategory
- [x] Full-text search across note_text
- [x] Mark annotation as resolved
- [x] Word meaning popup (from Quran Foundation)
- [x] Play audio for selected word range

## Deferred to v2

- [ ] Tarteel AI recitation checking integration
- [ ] Cross-ayah word selection
- [ ] Quran Foundation OAuth2 (Quran.com account linking)
- [ ] Offline mode (SQLite + sync)
- [ ] Annotation sharing between users
- [ ] Statistics dashboard and progress charts
- [ ] Spaced repetition review mode (Anki-style)