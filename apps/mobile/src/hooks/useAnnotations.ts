import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { annotationsApi } from '@/services/api';
import type { AnnotationCreate, AnnotationUpdate } from '@mushafi/shared-types';

export function useAnnotations(params: Record<string, unknown>) {
  return useQuery({
    queryKey: ['annotations', params],
    queryFn: () => annotationsApi.list(params),
  });
}

export function useAnnotation(id: string) {
  return useQuery({
    queryKey: ['annotations', id],
    queryFn: () => annotationsApi.get(id),
    enabled: !!id,
  });
}

export function useCreateAnnotation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AnnotationCreate) => annotationsApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['annotations'] }),
  });
}

export function useUpdateAnnotation(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: AnnotationUpdate) => annotationsApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['annotations'] }),
  });
}

export function useDeleteAnnotation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => annotationsApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['annotations'] }),
  });
}
