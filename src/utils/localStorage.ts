import { Message, Conversation, Draft } from '@/types';

const STORAGE_KEYS = {
  MESSAGES: 'adam_messages',
  CONVERSATIONS: 'adam_conversations',
  DRAFTS: 'adam_drafts',
  USER_PREFS: 'adam_user_prefs',
  SYNC_QUEUE: 'adam_sync_queue',
} as const;

export const LocalStorage = {
  // Messages
  saveMessages: (conversationId: string, messages: Message[]) => {
    try {
      const allMessages = LocalStorage.getAllMessages();
      allMessages[conversationId] = messages;
      localStorage.setItem(STORAGE_KEYS.MESSAGES, JSON.stringify(allMessages));
    } catch (error) {
      console.error('Failed to save messages to localStorage:', error);
    }
  },

  getMessages: (conversationId: string): Message[] => {
    try {
      const allMessages = LocalStorage.getAllMessages();
      return allMessages[conversationId] || [];
    } catch (error) {
      console.error('Failed to get messages from localStorage:', error);
      return [];
    }
  },

  getAllMessages: (): Record<string, Message[]> => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.MESSAGES);
      return data ? JSON.parse(data) : {};
    } catch (error) {
      console.error('Failed to get all messages from localStorage:', error);
      return {};
    }
  },

  // Conversations
  saveConversations: (conversations: Conversation[]) => {
    try {
      localStorage.setItem(STORAGE_KEYS.CONVERSATIONS, JSON.stringify(conversations));
    } catch (error) {
      console.error('Failed to save conversations to localStorage:', error);
    }
  },

  getConversations: (): Conversation[] => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.CONVERSATIONS);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Failed to get conversations from localStorage:', error);
      return [];
    }
  },

  // Drafts
  saveDraft: (draft: Draft) => {
    try {
      const drafts = LocalStorage.getAllDrafts();
      drafts[draft.conversationId] = draft;
      localStorage.setItem(STORAGE_KEYS.DRAFTS, JSON.stringify(drafts));
    } catch (error) {
      console.error('Failed to save draft to localStorage:', error);
    }
  },

  getDraft: (conversationId: string): Draft | null => {
    try {
      const drafts = LocalStorage.getAllDrafts();
      return drafts[conversationId] || null;
    } catch (error) {
      console.error('Failed to get draft from localStorage:', error);
      return null;
    }
  },

  getAllDrafts: (): Record<string, Draft> => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.DRAFTS);
      return data ? JSON.parse(data) : {};
    } catch (error) {
      console.error('Failed to get all drafts from localStorage:', error);
      return {};
    }
  },

  deleteDraft: (conversationId: string) => {
    try {
      const drafts = LocalStorage.getAllDrafts();
      delete drafts[conversationId];
      localStorage.setItem(STORAGE_KEYS.DRAFTS, JSON.stringify(drafts));
    } catch (error) {
      console.error('Failed to delete draft from localStorage:', error);
    }
  },

  // User preferences
  saveUserPrefs: (prefs: Record<string, unknown>) => {
    try {
      localStorage.setItem(STORAGE_KEYS.USER_PREFS, JSON.stringify(prefs));
    } catch (error) {
      console.error('Failed to save user preferences to localStorage:', error);
    }
  },

  getUserPrefs: (): Record<string, unknown> => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.USER_PREFS);
      return data ? JSON.parse(data) : {};
    } catch (error) {
      console.error('Failed to get user preferences from localStorage:', error);
      return {};
    }
  },

  // Sync queue for offline changes
  addToSyncQueue: (item: unknown) => {
    try {
      const queue = LocalStorage.getSyncQueue();
      queue.push(item);
      localStorage.setItem(STORAGE_KEYS.SYNC_QUEUE, JSON.stringify(queue));
    } catch (error) {
      console.error('Failed to add item to sync queue:', error);
    }
  },

  getSyncQueue: (): unknown[] => {
    try {
      const data = localStorage.getItem(STORAGE_KEYS.SYNC_QUEUE);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('Failed to get sync queue:', error);
      return [];
    }
  },

  clearSyncQueue: () => {
    try {
      localStorage.setItem(STORAGE_KEYS.SYNC_QUEUE, JSON.stringify([]));
    } catch (error) {
      console.error('Failed to clear sync queue:', error);
    }
  },

  // Clear all data
  clearAll: () => {
    try {
      Object.values(STORAGE_KEYS).forEach(key => {
        localStorage.removeItem(key);
      });
    } catch (error) {
      console.error('Failed to clear localStorage:', error);
    }
  },
};
