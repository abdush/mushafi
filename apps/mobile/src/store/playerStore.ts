import { create } from 'zustand';

interface PlayerState {
  isPlaying: boolean;
  currentWordIndex: number | null;
  chapterNumber: number | null;
  setPlaying: (playing: boolean) => void;
  setCurrentWordIndex: (index: number | null) => void;
  loadChapter: (chapter: number) => void;
  stop: () => void;
}

export const usePlayerStore = create<PlayerState>((set) => ({
  isPlaying: false,
  currentWordIndex: null,
  chapterNumber: null,
  setPlaying: (playing) => set({ isPlaying: playing }),
  setCurrentWordIndex: (index) => set({ currentWordIndex: index }),
  loadChapter: (chapter) => set({ chapterNumber: chapter, isPlaying: false, currentWordIndex: null }),
  stop: () => set({ isPlaying: false, currentWordIndex: null }),
}));
