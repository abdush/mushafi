import { useRef, useCallback } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import BottomSheet, { BottomSheetView } from '@gorhom/bottom-sheet';
import { useSelectionStore } from '@/store/selectionStore';

export function AnnotationSheet() {
  const sheetRef = useRef<BottomSheet>(null);
  const { selectedWords } = useSelectionStore();

  const hasSelection = selectedWords.length > 0;

  return (
    <BottomSheet
      ref={sheetRef}
      index={hasSelection ? 0 : -1}
      snapPoints={['40%', '80%']}
      enablePanDownToClose
    >
      <BottomSheetView style={styles.content}>
        <Text style={styles.title}>Add Annotation</Text>
      </BottomSheetView>
    </BottomSheet>
  );
}

const styles = StyleSheet.create({
  content: { flex: 1, padding: 16 },
  title: { fontSize: 18, fontWeight: '700', marginBottom: 12 },
});
