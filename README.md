# Mushafi

A Quran annotation app for students of hifz (memorization) and tajweed.

Tap words in an ayah → attach a categorized note → see color-coded highlights across the Quran → search and review by category.

---

## Project Structure

```
mushafi/
├── apps/
│   ├── api/          Python 3.12 · FastAPI · SQLAlchemy (async) · PostgreSQL · Redis
│   └── mobile/       TypeScript · Expo SDK 51 · React Native · Expo Router
├── packages/
│   └── shared-types/ TypeScript interfaces shared between API and mobile
└── docker-compose.yml
```

The API stores **only user-generated annotations**. All Quran text, audio, and translations are fetched from the [Quran Foundation API](https://api-docs.quran.foundation) and cached in Redis.

---

## Requirements

| Tool | Version |
|---|---|
| Docker + Docker Compose | any recent |
| Python | 3.12+ |
| Node.js | 20+ |
| Expo CLI | `npm install -g expo-cli` |

---

## Before You Start

### 1. Environment variables

```bash
cp .env.example .env
```

Fill in the three Supabase values — create a free project at [supabase.com](https://supabase.com):

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=...
SUPABASE_JWT_SECRET=...   # Settings → API → JWT Secret
```

### 2. Quran font

Download **KFGQPC Hafs Uthmanic** (the `.otf` file) and place it at:

```
apps/mobile/assets/fonts/KFGQPCHafsOTFPrint.otf
```

Font source: [qurancomplex.gov.sa](https://qurancomplex.gov.sa) or search "KFGQPC Hafs Uthmani OTF".

---

## Running the App

### Start infrastructure (PostgreSQL + Redis)

```bash
docker-compose up -d
```

### API

```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head          # creates tables + seeds global categories
uvicorn app.main:app --reload
```

API is now at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Mobile

```bash
cd apps/mobile
npm install
EXPO_PUBLIC_API_URL=http://localhost:8000/api/v1 npx expo start
```

Scan the QR code with [Expo Go](https://expo.dev/go) on your phone, or press `i` / `a` to open in a simulator.

---

## Running Tests

```bash
cd apps/api
pytest
```

---

## Key Conventions

- All Quran Foundation API calls go through `apps/api/app/services/quran_service.py` only — never call it from a router or component directly.
- Arabic text in the mobile app must use the `KFGQPC-Hafs` font family and `writingDirection: 'rtl'`.
- Word selection state lives in Zustand (`selectionStore`). Server data (annotations, categories, page content) goes through React Query hooks in `src/hooks/`.

See `CLAUDE.md`, `apps/api/CLAUDE.md`, and `apps/mobile/CLAUDE.md` for full conventions.
