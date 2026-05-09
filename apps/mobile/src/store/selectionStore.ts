import { create } from 'zustand';
import type { WordAddress } from '@mushafi/shared-types';

interface SelectionState {
  selectedWords: WordAddress[];
  toggleWord: (word: WordAddress) => void;
  clearSelection: () => void;
}

export const useSelectionStore = create<SelectionState>((set) => ({
  selectedWords: [],

  toggleWord: (word) =>
    set((state) => {
      const exists = state.selectedWords.some(
        (w) =>
          w.surahNumber === word.surahNumber &&
          w.ayahNumber === word.ayahNumber &&
          w.wordPosition === word.wordPosition
      );
      return {
        selectedWords: exists
          ? state.selectedWords.filter(
              (w) =>
                !(
                  w.surahNumber === word.surahNumber &&
                  w.ayahNumber === word.ayahNumber &&
                  w.wordPosition === word.wordPosition
                )
            )
          : [...state.selectedWords, word],
      };
    }),

  clearSelection: () => set({ selectedWords: [] }),
}));
