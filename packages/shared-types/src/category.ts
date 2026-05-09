export type Scope = 'global' | 'user';

export interface CategorySummary {
  id: string;
  labelAr: string;
  labelEn: string | null;
  colorHex: string;
}

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

export interface CategoryCreate {
  parentId?: string;
  labelAr: string;
  labelEn?: string;
  colorHex: string;
  icon?: string;
  sortOrder?: number;
}
