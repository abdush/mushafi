"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-09
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("display_name", sa.String(100), nullable=True),
        sa.Column("auth_provider", sa.Enum("email", "google", "quran_foundation", name="authprovider"), nullable=False, server_default="email"),
        sa.Column("auth_provider_id", sa.String(255), nullable=True),
        sa.Column("preferred_reciter_id", sa.Integer, nullable=True),
        sa.Column("preferred_tafseer_id", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("label_ar", sa.String(100), nullable=False),
        sa.Column("label_en", sa.String(100), nullable=True),
        sa.Column("color_hex", sa.String(7), nullable=False),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("scope", sa.Enum("global", "user", name="scope"), nullable=False, server_default="user"),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "annotations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("categories.id"), nullable=False),
        sa.Column("surah_number", sa.SmallInteger, nullable=False),
        sa.Column("ayah_number", sa.SmallInteger, nullable=False),
        sa.Column("word_start", sa.SmallInteger, nullable=False),
        sa.Column("word_end", sa.SmallInteger, nullable=False),
        sa.Column("note_text", sa.Text, nullable=True),
        sa.Column("severity", sa.Enum("info", "warning", "critical", name="severity"), nullable=False, server_default="info"),
        sa.Column("is_resolved", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("source", sa.Enum("manual", "tarteel_auto", name="source"), nullable=False, server_default="manual"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.CheckConstraint("word_end >= word_start", name="ck_word_end_gte_start"),
        sa.CheckConstraint("word_start >= 1", name="ck_word_start_positive"),
        sa.CheckConstraint("surah_number BETWEEN 1 AND 114", name="ck_valid_surah"),
    )

    op.create_index("idx_annotations_user_surah",  "annotations", ["user_id", "surah_number"])
    op.create_index("idx_annotations_user_verse",  "annotations", ["user_id", "surah_number", "ayah_number"])
    op.create_index("idx_annotations_category",    "annotations", ["user_id", "category_id"])
    op.create_index("idx_annotations_resolved",    "annotations", ["user_id", "is_resolved"])

    # Seed global categories
    op.execute("""
    WITH hifz AS (
        INSERT INTO categories (id, label_ar, label_en, color_hex, scope, sort_order)
        VALUES (gen_random_uuid(), 'حفظ', 'Hifz', '#ef4444', 'global', 0)
        RETURNING id
    ),
    tajweed AS (
        INSERT INTO categories (id, label_ar, label_en, color_hex, scope, sort_order)
        VALUES (gen_random_uuid(), 'تجويد', 'Tajweed', '#8b5cf6', 'global', 1)
        RETURNING id
    ),
    waqf AS (
        INSERT INTO categories (id, label_ar, label_en, color_hex, scope, sort_order)
        VALUES (gen_random_uuid(), 'وقف وابتداء', 'Waqf', '#0d9488', 'global', 2)
        RETURNING id
    )
    INSERT INTO categories (id, label_ar, color_hex, scope, parent_id, sort_order)
    SELECT gen_random_uuid(), child.label, child.color, 'global', child.parent_id, child.ord
    FROM (
        SELECT 'حذف كلمة' AS label, '#ef4444' AS color, (SELECT id FROM hifz) AS parent_id, 0 AS ord
        UNION ALL SELECT 'إبدال كلمة',  '#ef4444', (SELECT id FROM hifz),    1
        UNION ALL SELECT 'زيادة كلمة',  '#ef4444', (SELECT id FROM hifz),    2
        UNION ALL SELECT 'خطأ في الترتيب','#ef4444',(SELECT id FROM hifz),   3
        UNION ALL SELECT 'غنة',          '#8b5cf6', (SELECT id FROM tajweed), 0
        UNION ALL SELECT 'إدغام',        '#8b5cf6', (SELECT id FROM tajweed), 1
        UNION ALL SELECT 'إخفاء',        '#8b5cf6', (SELECT id FROM tajweed), 2
        UNION ALL SELECT 'إقلاب',        '#8b5cf6', (SELECT id FROM tajweed), 3
        UNION ALL SELECT 'قلقلة',        '#8b5cf6', (SELECT id FROM tajweed), 4
        UNION ALL SELECT 'وقف لازم',     '#0d9488', (SELECT id FROM waqf),    0
        UNION ALL SELECT 'وقف جائز',     '#0d9488', (SELECT id FROM waqf),    1
        UNION ALL SELECT 'وقف ممنوع',    '#0d9488', (SELECT id FROM waqf),    2
        UNION ALL SELECT 'وقف مرخص',     '#0d9488', (SELECT id FROM waqf),    3
    ) child;
    """)


def downgrade() -> None:
    op.drop_table("annotations")
    op.drop_table("categories")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS authprovider")
    op.execute("DROP TYPE IF EXISTS scope")
    op.execute("DROP TYPE IF EXISTS severity")
    op.execute("DROP TYPE IF EXISTS source")
