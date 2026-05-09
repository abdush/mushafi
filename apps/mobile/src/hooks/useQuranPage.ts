import { useQuery } from '@tanstack/react-query';
import { quranApi } from '@/services/api';

export function useQuranPage(pageNumber: number) {
  return useQuery({
    queryKey: ['quran', 'page', pageNumber],
    queryFn: () => quranApi.page(pageNumber),
    staleTime: 1000 * 60 * 60 * 24,
  });
}
