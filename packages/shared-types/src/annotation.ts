import type { CategorySummary } from './category';

export type Severity = 'info' | 'warning' | 'critical';
export type Source = 'manual' | 'tarteel_auto';

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

export interface AnnotationUpdate {
  categoryId?: string;
  noteText?: string;
  severity?: Severity;
  isResolved?: boolean;
}
