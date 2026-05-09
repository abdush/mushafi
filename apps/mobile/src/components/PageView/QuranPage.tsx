import { ScrollView, StyleSheet } from 'react-native';
import { useQuranPage } from '@/hooks/useQuranPage';
import { VerseDisplay } from '@/components/VerseDisplay/VerseDisplay';

interface Props {
  pageNumber: number;
}

export function QuranPage({ pageNumber }: Props) {
  const { data } = useQuranPage(pageNumber);
  const verses = data?.verses ?? [];

  return (
    <ScrollView style={styles.scroll} contentContainerStyle={styles.content}>
      {verses.map((verse: any) => (
        <VerseDisplay key={verse.verse_key} verse={verse} />
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scroll: { flex: 1 },
  content: { padding: 16 },
});
