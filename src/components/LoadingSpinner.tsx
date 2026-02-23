'use client';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function LoadingSpinner({ size = 'md', className = '' }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div
      className={`${sizeClasses[size]} border-primary border-t-transparent rounded-full animate-spin ${className}`}
      role="status"
      aria-label="Loading"
    />
  );
}

export function TypingIndicator() {
  return (
    <div className="flex space-x-1 items-center py-2">
      <div className="w-2 h-2 bg-muted-foreground rounded-full typing-dot" />
      <div className="w-2 h-2 bg-muted-foreground rounded-full typing-dot" />
      <div className="w-2 h-2 bg-muted-foreground rounded-full typing-dot" />
    </div>
  );
}

export function SkeletonMessage() {
  return (
    <div className="animate-pulse space-y-3">
      <div className="flex space-x-3">
        <div className="w-8 h-8 bg-secondary rounded-full" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-secondary rounded w-3/4" />
          <div className="h-4 bg-secondary rounded w-1/2" />
        </div>
      </div>
    </div>
  );
}

export function SkeletonConversation() {
  return (
    <div className="animate-pulse p-4 space-y-2">
      <div className="h-5 bg-secondary rounded w-3/4" />
      <div className="h-3 bg-secondary rounded w-1/2" />
    </div>
  );
}
