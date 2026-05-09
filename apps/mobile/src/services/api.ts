import axios from 'axios';
import type { Annotation, AnnotationCreate, AnnotationUpdate, CategoryNode } from '@mushafi/shared-types';

const API_BASE = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

export const apiClient = axios.create({ baseURL: API_BASE });

let _token: string | null = null;

export function setAuthToken(token: string | null) {
  _token = token;
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common['Authorization'];
  }
}

export const annotationsApi = {
  list: (params?: Record<string, unknown>) =>
    apiClient.get<Annotation[]>('/annotations', { params }).then((r) => r.data),

  get: (id: string) =>
    apiClient.get<Annotation>(`/annotations/${id}`).then((r) => r.data),

  create: (data: AnnotationCreate) =>
    apiClient.post<Annotation>('/annotations', data).then((r) => r.data),

  update: (id: string, data: AnnotationUpdate) =>
    apiClient.patch<Annotation>(`/annotations/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    apiClient.delete(`/annotations/${id}`),

  search: (q: string) =>
    apiClient.get<Annotation[]>('/annotations/search', { params: { q } }).then((r) => r.data),
};

export const categoriesApi = {
  tree: () =>
    apiClient.get<CategoryNode[]>('/categories').then((r) => r.data),
};

export const quranApi = {
  page: (n: number) =>
    apiClient.get(`/quran/page/${n}`).then((r) => r.data),

  verse: (surah: number, ayah: number) =>
    apiClient.get(`/quran/verse/${surah}/${ayah}`).then((r) => r.data),

  word: (surah: number, ayah: number, pos: number) =>
    apiClient.get(`/quran/word/${surah}/${ayah}/${pos}`).then((r) => r.data),

  audio: (chapter: number, reciterId = 7) =>
    apiClient.get(`/quran/audio/${chapter}`, { params: { reciter_id: reciterId } }).then((r) => r.data),
};
