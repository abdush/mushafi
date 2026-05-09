import { View, Text, StyleSheet, Pressable } from 'react-native';
import type { Annotation } from '@mushafi/shared-types';

interface Props {
  annotation: Annotation;
  onPress?: () => void;
}

const SEVERITY_COLOR: Record<string, string> = {
  info: '#0d9488',
  warning: '#f59e0b',
  critical: '#ef4444',
};

export function AnnotationCard({ annotation, onPress }: Props) {
  return (
    <Pressable onPress={onPress} style={styles.card}>
      <View style={[styles.dot, { backgroundColor: annotation.category.colorHex }]} />
      <View style={styles.body}>
        <Text style={styles.ref}>
          {annotation.surahNumber}:{annotation.ayahNumber} · words {annotation.wordStart}–{annotation.wordEnd}
        </Text>
        <Text style={styles.category}>{annotation.category.labelAr}</Text>
        {annotation.noteText ? <Text style={styles.note}>{annotation.noteText}</Text> : null}
      </View>
      <View style={[styles.severity, { backgroundColor: SEVERITY_COLOR[annotation.severity] }]} />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  dot: { width: 12, height: 12, borderRadius: 6, marginRight: 10 },
  body: { flex: 1 },
  ref: { fontSize: 12, color: '#78716c', marginBottom: 2 },
  category: { fontSize: 15, fontWeight: '600', textAlign: 'right', writingDirection: 'rtl' },
  note: { fontSize: 13, color: '#44403c', marginTop: 4 },
  severity: { width: 4, height: '100%', borderRadius: 2, marginLeft: 8 },
});
