export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: number;
  userId?: string;
  conversationId: string;
  metadata?: {
    edited?: boolean;
    editedAt?: number;
    reactions?: Record<string, number>;
  };
}

export interface Conversation {
  id: string;
  title: string;
  userId: string;
  createdAt: number;
  updatedAt: number;
  lastMessage?: string;
  messageCount: number;
  archived?: boolean;
  tags?: string[];
}

export interface User {
  id: string;
  email?: string;
  displayName?: string;
  photoURL?: string;
  provider: 'email' | 'google' | 'guest';
  createdAt: number;
  lastSeen: number;
  preferences?: {
    theme?: 'light' | 'dark' | 'auto';
    notifications?: boolean;
    autoSave?: boolean;
  };
}

export interface Draft {
  conversationId: string;
  content: string;
  timestamp: number;
}

export interface AppState {
  isOnline: boolean;
  isSyncing: boolean;
  lastSyncAt?: number;
  pendingChanges: number;
}
