import { View, Text, FlatList, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAnnotations } from '@/hooks/useAnnotations';
import { AnnotationCard } from '@/components/Annotation/AnnotationCard';

export default function NotesScreen() {
  const { data: annotations = [], isLoading } = useAnnotations({});

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.heading}>My Notes</Text>
      <FlatList
        data={annotations}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => <AnnotationCard annotation={item} />}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafaf9', paddingHorizontal: 16 },
  heading: { fontSize: 22, fontWeight: '700', marginVertical: 16 },
});
