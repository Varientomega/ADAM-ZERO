'use client';

import { useState, useRef, useEffect } from 'react';
import { useAppStore } from '@/store/appStore';
import { Message } from '@/types';
import { FiSend, FiPaperclip, FiMoreVertical } from 'react-icons/fi';
import { formatDistanceToNow } from 'date-fns';
import { TypingIndicator, SkeletonMessage } from './LoadingSpinner';
import { motion, AnimatePresence } from 'framer-motion';

interface ChatInterfaceProps {
  conversationId: string;
  onSendMessage: (content: string) => void;
  onSaveDraft: (content: string) => void;
  isLoading?: boolean;
}

export function ChatInterface({
  conversationId,
  onSendMessage,
  onSaveDraft,
  isLoading = false,
}: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const messages = useAppStore((state) => state.messages[conversationId] || []);
  const appState = useAppStore((state) => state.appState);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Auto-save draft
    const timer = setTimeout(() => {
      if (input.trim()) {
        onSaveDraft(input);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [input, onSaveDraft]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    onSendMessage(input);
    setInput('');
    setIsTyping(true);
    
    // Simulate AI response
    setTimeout(() => {
      setIsTyping(false);
    }, 2000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Header */}
      <div className="border-b border-border p-4 bg-card">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-semibold text-lg">Conversation</h2>
            <p className="text-sm text-muted-foreground">
              {appState.isOnline ? (
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-500 rounded-full" />
                  Online
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-yellow-500 rounded-full" />
                  Offline - Changes will sync when online
                </span>
              )}
            </p>
          </div>
          <button
            className="p-2 hover:bg-secondary rounded-lg transition-colors"
            aria-label="More options"
          >
            <FiMoreVertical size={20} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {isLoading && messages.length === 0 ? (
          <>
            <SkeletonMessage />
            <SkeletonMessage />
            <SkeletonMessage />
          </>
        ) : messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-md">
              <h3 className="text-xl font-semibold mb-2">Start a conversation</h3>
              <p className="text-muted-foreground">
                Type your message below to begin. Your conversations are automatically saved
                and synced across devices.
              </p>
            </div>
          </div>
        ) : (
          <AnimatePresence>
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
          </AnimatePresence>
        )}
        
        {isTyping && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
              <span className="text-primary font-semibold text-sm">AI</span>
            </div>
            <div className="bg-card border border-border rounded-lg px-4 py-2">
              <TypingIndicator />
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-border p-4 bg-card">
        <form onSubmit={handleSubmit} className="flex items-end gap-2">
          <button
            type="button"
            className="p-2 hover:bg-secondary rounded-lg transition-colors mb-2"
            aria-label="Attach file"
          >
            <FiPaperclip size={20} />
          </button>
          
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
              className="w-full resize-none bg-secondary border border-border rounded-lg px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-ring min-h-[52px] max-h-40"
              rows={1}
              style={{
                height: 'auto',
                minHeight: '52px',
              }}
              onInput={(e) => {
                const target = e.target as HTMLTextAreaElement;
                target.style.height = 'auto';
                target.style.height = Math.min(target.scrollHeight, 160) + 'px';
              }}
            />
          </div>

          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="p-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed mb-2"
            aria-label="Send message"
          >
            <FiSend size={20} />
          </button>
        </form>
        
        {input.trim() && (
          <p className="text-xs text-muted-foreground mt-2">
            Draft auto-saved
          </p>
        )}
      </div>
    </div>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser ? 'bg-accent/10' : 'bg-primary/10'
        }`}
      >
        <span className={`font-semibold text-sm ${isUser ? 'text-accent' : 'text-primary'}`}>
          {isUser ? 'U' : 'AI'}
        </span>
      </div>

      <div className={`flex-1 ${isUser ? 'flex justify-end' : ''}`}>
        <div
          className={`max-w-[80%] rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-accent text-accent-foreground'
              : 'bg-card border border-border'
          }`}
        >
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
          <p
            className={`text-xs mt-2 ${
              isUser ? 'text-accent-foreground/70' : 'text-muted-foreground'
            }`}
          >
            {formatDistanceToNow(message.timestamp, { addSuffix: true })}
          </p>
        </div>
      </div>
    </motion.div>
  );
}
