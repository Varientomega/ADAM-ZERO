'use client';

import { useEffect } from 'react';
import { useAppStore } from '@/store/appStore';
import { ErrorBoundary } from './ErrorBoundary';

export function Providers({ children }: { children: React.ReactNode }) {
  const setAppState = useAppStore((state) => state.setAppState);

  useEffect(() => {
    // Online/offline detection
    const handleOnline = () => {
      setAppState({ isOnline: true });
    };

    const handleOffline = () => {
      setAppState({ isOnline: false });
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Initial state
    setAppState({ isOnline: navigator.onLine });

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [setAppState]);

  return <ErrorBoundary>{children}</ErrorBoundary>;
}
