import { Pressable, Text, StyleSheet } from 'react-native';
import { useSelectionStore } from '@/store/selectionStore';
import type { QFWord } from '@mushafi/shared-types';

interface Props {
  word: QFWord;
  surahNumber: number;
  ayahNumber: number;
}

export function WordToken({ word, surahNumber, ayahNumber }: Props) {
  const { selectedWords, toggleWord } = useSelectionStore();

  const isSelected = selectedWords.some(
    (w) => w.surahNumber === surahNumber && w.ayahNumber === ayahNumber && w.wordPosition === word.position
  );

  return (
    <Pressable
      onPress={() => toggleWord({ surahNumber, ayahNumber, wordPosition: word.position })}
      style={[styles.token, isSelected && styles.selected]}
    >
      <Text style={styles.text}>{word.text_uthmani}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  token: { paddingHorizontal: 2, paddingVertical: 4, borderRadius: 4 },
  selected: { backgroundColor: '#ddd6fe' },
  text: {
    fontFamily: 'KFGQPC-Hafs',
    fontSize: 22,
    writingDirection: 'rtl',
    textAlign: 'right',
    color: '#1c1917',
  },
});
