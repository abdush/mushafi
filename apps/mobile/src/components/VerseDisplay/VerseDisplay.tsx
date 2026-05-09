import { View, StyleSheet } from 'react-native';
import { WordToken } from './WordToken';
import { AyahNumber } from './AyahNumber';
import type { QFWord } from '@mushafi/shared-types';

interface Props {
  verse: {
    verse_key: string;
    verse_number: number;
    words: QFWord[];
  };
}

export function VerseDisplay({ verse }: Props) {
  const [surah, ayah] = verse.verse_key.split(':').map(Number);

  return (
    <View style={styles.row}>
      <AyahNumber number={verse.verse_number} />
      <View style={styles.words}>
        {verse.words
          .filter((w) => w.char_type_name === 'word')
          .map((word) => (
            <WordToken
              key={word.id}
              word={word}
              surahNumber={surah}
              ayahNumber={ayah}
            />
          ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row-reverse', flexWrap: 'wrap', alignItems: 'center', marginBottom: 8 },
  words: { flexDirection: 'row-reverse', flexWrap: 'wrap', flex: 1 },
});
