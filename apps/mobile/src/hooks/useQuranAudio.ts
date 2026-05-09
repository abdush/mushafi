import { useQuery } from '@tanstack/react-query';
import { quranApi } from '@/services/api';

export function useQuranAudio(chapter: number, reciterId = 7) {
  return useQuery({
    queryKey: ['quran', 'audio', chapter, reciterId],
    queryFn: () => quranApi.audio(chapter, reciterId),
    staleTime: 1000 * 60 * 60 * 24,
  });
}
