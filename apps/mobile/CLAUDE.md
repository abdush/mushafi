# apps/mobile — Mobile Conventions

- Arabic text must use `fontFamily: 'KFGQPC-Hafs'` — never system Arabic fonts
- All Arabic text: `writingDirection: 'rtl'` and `textAlign: 'right'`
- Word selection state lives in `store/selectionStore.ts` (Zustand)
- Server data (annotations, categories, quran pages) via React Query hooks in `src/hooks/`
- Never call API directly from components — always through hooks
- Bottom sheet for annotation input uses `@gorhom/bottom-sheet`
- No v2 features: no offline mode, no cross-ayah selection, no Tarteel AI
