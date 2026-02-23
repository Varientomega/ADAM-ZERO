'use client';

import { useState, useEffect } from 'react';
import { useAppStore } from '@/store/appStore';
import { Conversation } from '@/types';
import { formatDistanceToNow } from 'date-fns';
import {
  FiPlus,
  FiMessageSquare,
  FiTrash2,
  FiMenu,
  FiX,
  FiArchive,
  FiSettings,
} from 'react-icons/fi';
import { SkeletonConversation } from './LoadingSpinner';

interface SidebarProps {
  onNewConversation: () => void;
  onSelectConversation: (id: string) => void;
  onDeleteConversation: (id: string) => void;
}

export function Sidebar({
  onNewConversation,
  onSelectConversation,
  onDeleteConversation,
}: SidebarProps) {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const conversations = useAppStore((state) => state.conversations);
  const currentConversationId = useAppStore((state) => state.currentConversationId);
  const user = useAppStore((state) => state.user);

  useEffect(() => {
    setTimeout(() => setIsLoading(false), 500);
  }, []);

  const handleNewConversation = () => {
    onNewConversation();
    setIsMobileOpen(false);
  };

  const handleSelectConversation = (id: string) => {
    onSelectConversation(id);
    setIsMobileOpen(false);
  };

  const activeConversations = conversations.filter((c) => !c.archived);
  const archivedConversations = conversations.filter((c) => c.archived);

  return (
    <>
      {/* Mobile menu button */}
      <button
        onClick={() => setIsMobileOpen(!isMobileOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-card border border-border rounded-lg shadow-lg"
        aria-label="Toggle menu"
      >
        {isMobileOpen ? <FiX size={24} /> : <FiMenu size={24} />}
      </button>

      {/* Overlay */}
      {isMobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setIsMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-40
          w-80 bg-card border-r border-border
          transform transition-transform duration-300 ease-in-out
          ${isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="p-4 border-b border-border">
            <button
              onClick={handleNewConversation}
              className="w-full flex items-center justify-center gap-2 bg-primary text-primary-foreground px-4 py-3 rounded-lg hover:opacity-90 transition-opacity"
            >
              <FiPlus size={20} />
              <span className="font-medium">New Conversation</span>
            </button>
          </div>

          {/* Conversations List */}
          <div className="flex-1 overflow-y-auto p-2">
            {isLoading ? (
              <>
                <SkeletonConversation />
                <SkeletonConversation />
                <SkeletonConversation />
              </>
            ) : activeConversations.length === 0 ? (
              <div className="text-center py-12 px-4">
                <FiMessageSquare size={48} className="mx-auto text-muted-foreground mb-4" />
                <p className="text-muted-foreground text-sm">
                  No conversations yet. Start a new one!
                </p>
              </div>
            ) : (
              <div className="space-y-1">
                {activeConversations.map((conv) => (
                  <ConversationItem
                    key={conv.id}
                    conversation={conv}
                    isActive={conv.id === currentConversationId}
                    onSelect={() => handleSelectConversation(conv.id)}
                    onDelete={() => onDeleteConversation(conv.id)}
                  />
                ))}
              </div>
            )}

            {archivedConversations.length > 0 && (
              <div className="mt-6">
                <div className="flex items-center gap-2 px-3 py-2 text-sm text-muted-foreground">
                  <FiArchive size={16} />
                  <span>Archived</span>
                </div>
                <div className="space-y-1">
                  {archivedConversations.map((conv) => (
                    <ConversationItem
                      key={conv.id}
                      conversation={conv}
                      isActive={conv.id === currentConversationId}
                      onSelect={() => handleSelectConversation(conv.id)}
                      onDelete={() => onDeleteConversation(conv.id)}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-border">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="text-primary font-semibold">
                  {user?.displayName?.[0]?.toUpperCase() || 'U'}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">
                  {user?.displayName || 'Guest User'}
                </p>
                <p className="text-xs text-muted-foreground truncate">
                  {user?.email || 'Not signed in'}
                </p>
              </div>
              <button
                className="p-2 hover:bg-secondary rounded-lg transition-colors"
                aria-label="Settings"
              >
                <FiSettings size={20} />
              </button>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  onSelect: () => void;
  onDelete: () => void;
}

function ConversationItem({
  conversation,
  isActive,
  onSelect,
  onDelete,
}: ConversationItemProps) {
  const [showDelete, setShowDelete] = useState(false);

  return (
    <div
      className={`
        group relative p-3 rounded-lg cursor-pointer
        ${isActive ? 'bg-primary/10 border border-primary/20' : 'hover:bg-secondary'}
      `}
      onClick={onSelect}
      onMouseEnter={() => setShowDelete(true)}
      onMouseLeave={() => setShowDelete(false)}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-sm truncate">{conversation.title}</h3>
          {conversation.lastMessage && (
            <p className="text-xs text-muted-foreground truncate mt-1">
              {conversation.lastMessage}
            </p>
          )}
          <p className="text-xs text-muted-foreground mt-1">
            {formatDistanceToNow(conversation.updatedAt, { addSuffix: true })}
          </p>
        </div>
        {showDelete && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
            className="p-1 hover:bg-destructive/10 rounded transition-colors"
            aria-label="Delete conversation"
          >
            <FiTrash2 size={16} className="text-destructive" />
          </button>
        )}
      </div>
    </div>
  );
}
