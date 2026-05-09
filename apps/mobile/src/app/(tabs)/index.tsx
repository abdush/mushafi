import { View, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { QuranPage } from '@/components/PageView/QuranPage';
import { AnnotationSheet } from '@/components/Annotation/AnnotationSheet';

export default function QuranScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.page}>
        <QuranPage pageNumber={1} />
      </View>
      <AnnotationSheet />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fafaf9' },
  page: { flex: 1 },
});
