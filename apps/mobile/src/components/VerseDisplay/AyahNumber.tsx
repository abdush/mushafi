import { View, Text, StyleSheet } from 'react-native';

interface Props {
  number: number;
}

export function AyahNumber({ number }: Props) {
  return (
    <View style={styles.badge}>
      <Text style={styles.text}>{number}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    width: 28,
    height: 28,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#8b5cf6',
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 4,
  },
  text: { fontSize: 11, color: '#8b5cf6', fontWeight: '600' },
});
