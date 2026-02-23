import { useEffect, useState } from 'react';
import { 
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User as FirebaseUser,
  signInAnonymously,
} from 'firebase/auth';
import { auth } from '@/lib/firebase';
import { useAppStore } from '@/store/appStore';
import { User } from '@/types';
import { toast } from 'react-hot-toast';

export function useFirebaseAuth() {
  const [loading, setLoading] = useState(true);
  const setUser = useAppStore((state) => state.setUser);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      if (firebaseUser) {
        const user: User = {
          id: firebaseUser.uid,
          email: firebaseUser.email || undefined,
          displayName: firebaseUser.displayName || undefined,
          photoURL: firebaseUser.photoURL || undefined,
          provider: firebaseUser.isAnonymous 
            ? 'guest' 
            : firebaseUser.providerData[0]?.providerId === 'google.com' 
            ? 'google' 
            : 'email',
          createdAt: Date.now(),
          lastSeen: Date.now(),
        };
        setUser(user);
      } else {
        setUser(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [setUser]);

  const signInWithEmail = async (email: string, password: string) => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
      toast.success('Signed in successfully!');
    } catch (error: unknown) {
      console.error('Sign in error:', error);
      toast.error('Failed to sign in. Please check your credentials.');
      throw error;
    }
  };

  const signUpWithEmail = async (email: string, password: string, displayName?: string) => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      if (displayName) {
        // You could update the profile here
      }
      toast.success('Account created successfully!');
      return userCredential.user;
    } catch (error: unknown) {
      console.error('Sign up error:', error);
      toast.error('Failed to create account.');
      throw error;
    }
  };

  const signInWithGoogle = async () => {
    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
      toast.success('Signed in with Google!');
    } catch (error: unknown) {
      console.error('Google sign in error:', error);
      toast.error('Failed to sign in with Google.');
      throw error;
    }
  };

  const signInAsGuest = async () => {
    try {
      await signInAnonymously(auth);
      toast.success('Signed in as guest!');
    } catch (error: unknown) {
      console.error('Guest sign in error:', error);
      toast.error('Failed to sign in as guest.');
      throw error;
    }
  };

  const signOut = async () => {
    try {
      await firebaseSignOut(auth);
      toast.success('Signed out successfully!');
    } catch (error: unknown) {
      console.error('Sign out error:', error);
      toast.error('Failed to sign out.');
      throw error;
    }
  };

  return {
    loading,
    signInWithEmail,
    signUpWithEmail,
    signInWithGoogle,
    signInAsGuest,
    signOut,
  };
}
