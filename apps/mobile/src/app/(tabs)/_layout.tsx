import { Tabs } from 'expo-router';

export default function TabsLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#8b5cf6' }}>
      <Tabs.Screen name="index"    options={{ title: 'Quran' }} />
      <Tabs.Screen name="notes"    options={{ title: 'Notes' }} />
      <Tabs.Screen name="settings" options={{ title: 'Settings' }} />
    </Tabs>
  );
}
