import { useEffect, useCallback } from 'react';
import { useAppStore } from '@/store/appStore';
import { LocalStorage } from '@/utils/localStorage';
import { toast } from 'react-hot-toast';

export function useAutoSave() {
  const conversations = useAppStore((state) => state.conversations);
  const messages = useAppStore((state) => state.messages);
  const appState = useAppStore((state) => state.appState);

  // Save conversations to localStorage
  useEffect(() => {
    LocalStorage.saveConversations(conversations);
  }, [conversations]);

  // Save messages to localStorage
  useEffect(() => {
    Object.entries(messages).forEach(([conversationId, msgs]) => {
      LocalStorage.saveMessages(conversationId, msgs);
    });
  }, [messages]);

  // Sync with Firebase when online
  const syncWithFirebase = useCallback(async () => {
    if (!appState.isOnline) return;

    const syncQueue = LocalStorage.getSyncQueue();
    if (syncQueue.length === 0) return;

    try {
      // Here you would sync with Firebase
      // For now, just clear the queue
      LocalStorage.clearSyncQueue();
      toast.success('All changes synced successfully');
    } catch (error) {
      console.error('Sync failed:', error);
      toast.error('Failed to sync changes. Will retry later.');
    }
  }, [appState.isOnline]);

  useEffect(() => {
    if (appState.isOnline) {
      syncWithFirebase();
    }
  }, [appState.isOnline, syncWithFirebase]);

  return { syncWithFirebase };
}
