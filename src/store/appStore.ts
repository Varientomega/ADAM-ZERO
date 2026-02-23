import { create } from 'zustand';
import { Message, Conversation, User, AppState } from '@/types';

interface AppStore {
  // State
  user: User | null;
  conversations: Conversation[];
  currentConversationId: string | null;
  messages: Record<string, Message[]>;
  appState: AppState;
  
  // Actions
  setUser: (user: User | null) => void;
  setConversations: (conversations: Conversation[]) => void;
  addConversation: (conversation: Conversation) => void;
  updateConversation: (id: string, updates: Partial<Conversation>) => void;
  deleteConversation: (id: string) => void;
  setCurrentConversationId: (id: string | null) => void;
  setMessages: (conversationId: string, messages: Message[]) => void;
  addMessage: (conversationId: string, message: Message) => void;
  updateMessage: (conversationId: string, messageId: string, updates: Partial<Message>) => void;
  deleteMessage: (conversationId: string, messageId: string) => void;
  setAppState: (state: Partial<AppState>) => void;
  reset: () => void;
}

const initialState = {
  user: null,
  conversations: [],
  currentConversationId: null,
  messages: {},
  appState: {
    isOnline: true,
    isSyncing: false,
    pendingChanges: 0,
  },
};

export const useAppStore = create<AppStore>((set) => ({
  ...initialState,

  setUser: (user) => set({ user }),

  setConversations: (conversations) => set({ conversations }),

  addConversation: (conversation) =>
    set((state) => ({
      conversations: [conversation, ...state.conversations],
    })),

  updateConversation: (id, updates) =>
    set((state) => ({
      conversations: state.conversations.map((conv) =>
        conv.id === id ? { ...conv, ...updates } : conv
      ),
    })),

  deleteConversation: (id) =>
    set((state) => ({
      conversations: state.conversations.filter((conv) => conv.id !== id),
      currentConversationId:
        state.currentConversationId === id ? null : state.currentConversationId,
    })),

  setCurrentConversationId: (id) => set({ currentConversationId: id }),

  setMessages: (conversationId, messages) =>
    set((state) => ({
      messages: {
        ...state.messages,
        [conversationId]: messages,
      },
    })),

  addMessage: (conversationId, message) =>
    set((state) => ({
      messages: {
        ...state.messages,
        [conversationId]: [
          ...(state.messages[conversationId] || []),
          message,
        ],
      },
    })),

  updateMessage: (conversationId, messageId, updates) =>
    set((state) => ({
      messages: {
        ...state.messages,
        [conversationId]: (state.messages[conversationId] || []).map((msg) =>
          msg.id === messageId ? { ...msg, ...updates } : msg
        ),
      },
    })),

  deleteMessage: (conversationId, messageId) =>
    set((state) => ({
      messages: {
        ...state.messages,
        [conversationId]: (state.messages[conversationId] || []).filter(
          (msg) => msg.id !== messageId
        ),
      },
    })),

  setAppState: (appStateUpdates) =>
    set((state) => ({
      appState: {
        ...state.appState,
        ...appStateUpdates,
      },
    })),

  reset: () => set(initialState),
}));
