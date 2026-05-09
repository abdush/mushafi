# Mushafi — Data Model

## Guiding Principle

Our database stores **only user-generated data**. Quran text, translations, audio, and morphology are never persisted — they are fetched from the Quran Foundation API and cached in Redis.

---

## Entity Overview

```
User
 └── Category (tree, unlimited nesting)
 └── Annotation
      ├── anchored to: surah + ayah + word_start + word_end
      └── belongs to: Category
```

---

## Tables

### users

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| email | VARCHAR(255) | unique |
| display_name | VARCHAR(100) | |
| auth_provider | ENUM | `email`, `google`, `quran_foundation` |
| auth_provider_id | VARCHAR(255) | external user ID from provider |
| preferred_reciter_id | INTEGER | Quran Foundation reciter ID |
| preferred_tafseer_id | INTEGER | Quran Foundation tafseer ID |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

---

### categories

Self-referencing tree. Supports unlimited nesting via `parent_id`.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | NULL for global defaults |
| parent_id | UUID FK → categories | NULL = top-level |
| label_ar | VARCHAR(100) | Arabic label (required) |
| label_en | VARCHAR(100) | English label (optional) |
| color_hex | CHAR(7) | e.g. `#ef4444` |
| icon | VARCHAR(50) | emoji or icon name, optional |
| scope | ENUM | `global` or `user` |
| sort_order | INTEGER | display order within siblings |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

**Constraints:**
- `user_id` must be NULL when `scope = global`
- `user_id` must be set when `scope = user`
- `scope = global` rows cannot be deleted (enforced in service layer)

**Seeded global defaults:**

```
حفظ  (hifz)          color:#ef4444  scope:global
  ├── حذف كلمة        (skipped word)
  ├── إبدال كلمة      (wrong word)
  ├── زيادة كلمة      (added word)
  └── خطأ في الترتيب  (wrong order)

تجويد (tajweed)       color:#8b5cf6  scope:global
  ├── غنة
  ├── مد
  │    ├── مد واجب متصل
  │    ├── مد جائز منفصل
  │    └── مد لازم
  ├── إدغام
  ├── إخفاء
  ├── إقلاب
  └── قلقلة

وقف وابتداء (waqf)   color:#0d9488  scope:global
  ├── وقف لازم        ﻡ
  ├── وقف جائز        ج
  ├── وقف ممنوع       ﻻ
  └── وقف مرخص       ص
```

---

### annotations

Core table. Each row represents one note attached to a word or word range.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK → users | |
| category_id | UUID FK → categories | any depth in the tree |
| surah_number | SMALLINT | 1–114 |
| ayah_number | SMALLINT | 1–286 |
| word_start | SMALLINT | 1-based word position (Quran Foundation standard) |
| word_end | SMALLINT | same ayah as word_start (MVP constraint) |
| note_text | TEXT | free-form note, optional |
| severity | ENUM | `info`, `warning`, `critical` |
| is_resolved | BOOLEAN | default false — mark as fixed after practice |
| source | ENUM | `manual`, `tarteel_auto` |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

**Constraints:**
- `word_end >= word_start`
- `word_start >= 1`
- `surah_number` between 1 and 114
- One word can have multiple annotations (same or different categories) — no uniqueness constraint on the word address

**Indexes:**
```sql
-- Fast page/verse load: fetch all annotations for a page
CREATE INDEX idx_annotations_user_surah      ON annotations(user_id, surah_number);
CREATE INDEX idx_annotations_user_verse      ON annotations(user_id, surah_number, ayah_number);

-- Filter by category
CREATE INDEX idx_annotations_category        ON annotations(user_id, category_id);

-- Filter unresolved
CREATE INDEX idx_annotations_resolved        ON annotations(user_id, is_resolved);

-- Full-text search on notes
CREATE INDEX idx_annotations_note_fts        ON annotations USING gin(to_tsvector('arabic', note_text));
```

---

## Word Addressing Standard

Every Quran word is addressed as `surah_number : ayah_number : word_position`.

Examples:
- `1:1:1` → first word of Al-Fatiha (بِسْمِ)
- `2:255:1` → first word of Ayat Al-Kursi (اللَّهُ)
- `1:1:1 → 1:1:4` → all four words of the Basmala

This addressing scheme is the Quran Foundation / quran.com standard. Word positions are 1-based and stable — they will not change across API versions.

**In our DB we store as three integers**, not a string key:
```
surah_number = 2
ayah_number  = 255
word_start   = 1
word_end     = 3   (words 1, 2, 3 selected)
```

---

## Pydantic Schemas (API request/response)

### AnnotationCreate
```python
class AnnotationCreate(BaseModel):
    surah_number: int = Field(ge=1, le=114)
    ayah_number:  int = Field(ge=1)
    word_start:   int = Field(ge=1)
    word_end:     int = Field(ge=1)
    category_id:  UUID
    note_text:    str | None = None
    severity:     Severity = Severity.info

    @model_validator(mode='after')
    def word_end_gte_start(self):
        if self.word_end < self.word_start:
            raise ValueError('word_end must be >= word_start')
        return self
```

### AnnotationResponse
```python
class AnnotationResponse(BaseModel):
    id:           UUID
    surah_number: int
    ayah_number:  int
    word_start:   int
    word_end:     int
    category:     CategorySummary   # nested: id, label_ar, label_en, color_hex
    note_text:    str | None
    severity:     Severity
    is_resolved:  bool
    source:       Source
    created_at:   datetime
    updated_at:   datetime
```

### CategoryCreate
```python
class CategoryCreate(BaseModel):
    parent_id:  UUID | None = None
    label_ar:   str = Field(min_length=1, max_length=100)
    label_en:   str | None = Field(default=None, max_length=100)
    color_hex:  str = Field(pattern=r'^#[0-9a-fA-F]{6}$')
    icon:       str | None = None
    sort_order: int = 0
```

### CategoryTree (response)
```python
class CategoryNode(BaseModel):
    id:         UUID
    label_ar:   str
    label_en:   str | None
    color_hex:  str
    icon:       str | None
    scope:      Scope
    children:   list['CategoryNode'] = []   # recursive
    annotation_count: int                   # for UI badge
```

---

## TypeScript Shared Types (`packages/shared-types`)

```typescript
// quran.ts
export interface WordAddress {
  surahNumber: number;
  ayahNumber: number;
  wordPosition: number;  // 1-based
}

export interface WordSelection {
  surahNumber: number;
  ayahNumber: number;
  wordStart: number;
  wordEnd: number;
}

// Quran Foundation API word shape (subset we use)
export interface QFWord {
  id: number;
  position: number;
  text_uthmani: string;
  text_imlaei: string;
  transliteration: string;
  translation: string;
  char_type_name: 'word' | 'end' | 'pause' | 'sajdah' | 'rub-el-hizb';
}

// annotation.ts
export type Severity = 'info' | 'warning' | 'critical';
export type Source   = 'manual' | 'tarteel_auto';

export interface Annotation {
  id: string;
  surahNumber: number;
  ayahNumber: number;
  wordStart: number;
  wordEnd: number;
  category: CategorySummary;
  noteText: string | null;
  severity: Severity;
  isResolved: boolean;
  source: Source;
  createdAt: string;
  updatedAt: string;
}

export interface AnnotationCreate {
  surahNumber: number;
  ayahNumber: number;
  wordStart: number;
  wordEnd: number;
  categoryId: string;
  noteText?: string;
  severity?: Severity;
}

// category.ts
export type Scope = 'global' | 'user';

export interface CategoryNode {
  id: string;
  labelAr: string;
  labelEn: string | null;
  colorHex: string;
  icon: string | null;
  scope: Scope;
  children: CategoryNode[];
  annotationCount: number;
}

export interface CategorySummary {
  id: string;
  labelAr: string;
  labelEn: string | null;
  colorHex: string;
}
```

---

## SQLAlchemy Models

```python
# models/annotation.py
import enum, uuid
from sqlalchemy import Column, Integer, SmallInteger, Text, Boolean, DateTime, ForeignKey, Enum as SAEnum, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Severity(str, enum.Enum):
    info     = "info"
    warning  = "warning"
    critical = "critical"

class Source(str, enum.Enum):
    manual       = "manual"
    tarteel_auto = "tarteel_auto"

class Annotation(Base):
    __tablename__ = "annotations"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id      = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id  = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    surah_number = Column(SmallInteger, nullable=False)
    ayah_number  = Column(SmallInteger, nullable=False)
    word_start   = Column(SmallInteger, nullable=False)
    word_end     = Column(SmallInteger, nullable=False)
    note_text    = Column(Text, nullable=True)
    severity     = Column(SAEnum(Severity), nullable=False, default=Severity.info)
    is_resolved  = Column(Boolean, nullable=False, default=False)
    source       = Column(SAEnum(Source), nullable=False, default=Source.manual)
    created_at   = Column(DateTime(timezone=True), server_default="now()")
    updated_at   = Column(DateTime(timezone=True), server_default="now()", onupdate="now()")

    __table_args__ = (
        CheckConstraint("word_end >= word_start", name="ck_word_end_gte_start"),
        CheckConstraint("word_start >= 1",        name="ck_word_start_positive"),
        CheckConstraint("surah_number BETWEEN 1 AND 114", name="ck_valid_surah"),
    )

    user     = relationship("User",     back_populates="annotations")
    category = relationship("Category", back_populates="annotations")


# models/category.py
class Scope(str, enum.Enum):
    global_ = "global"
    user    = "user"

class Category(Base):
    __tablename__ = "categories"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    parent_id  = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    label_ar   = Column(String(100), nullable=False)
    label_en   = Column(String(100), nullable=True)
    color_hex  = Column(String(7), nullable=False)
    icon       = Column(String(50), nullable=True)
    scope      = Column(SAEnum(Scope), nullable=False, default=Scope.user)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default="now()")
    updated_at = Column(DateTime(timezone=True), server_default="now()", onupdate="now()")

    parent      = relationship("Category", remote_side=[id], back_populates="children")
    children    = relationship("Category", back_populates="parent", order_by=sort_order)
    annotations = relationship("Annotation", back_populates="category")
```

---

## Alembic Migration Strategy

- One migration file per logical change
- Never edit existing migration files once merged
- Migration naming: `{revision}_{short_description}.py`
- Always include `downgrade()` implementation

First migration creates: `users`, `categories`, `annotations`, all indexes, seeds global categories.

---

## Caching Strategy

### Redis Key Format
```
qf:page:{page_number}                        TTL: 24h
qf:verse:{surah}:{ayah}                      TTL: 24h
qf:word:{surah}:{ayah}:{position}            TTL: 24h
qf:audio:{chapter}:{reciter_id}:segments     TTL: 24h
qf:tafseer:{tafseer_id}:{surah}:{ayah}       TTL: 24h
```

### What Is NOT Cached
- Annotation reads (always fresh from PostgreSQL)
- Category tree (small, always fresh)
- User preferences

---

## Future Schema Extensions (v2, do not build yet)

```sql
-- For offline sync
ALTER TABLE annotations ADD COLUMN device_id VARCHAR(100);
ALTER TABLE annotations ADD COLUMN synced_at TIMESTAMPTZ;

-- For spaced repetition review
CREATE TABLE review_sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users,
    annotation_id UUID REFERENCES annotations,
    reviewed_at TIMESTAMPTZ,
    result ENUM('pass', 'fail', 'skip')
);

-- For sharing between users (e.g. teacher → student)
ALTER TABLE annotations ADD COLUMN shared_with UUID[] DEFAULT '{}';
```