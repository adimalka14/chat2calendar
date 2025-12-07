"use client";
import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { apiClient } from "@/lib/api";

type User = { id: string; email: string; name?: string, picture?: string };
type AuthState = { user: User | null; isLoading: boolean; isAuthenticated: boolean };

interface AuthContextType {
  authState: AuthState;
  signIn: () => Promise<void>;
  signOut: () => Promise<void>;
  completeCallback: (code: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isLoading: true,
    isAuthenticated: false,
  });

  const saveSession = (token: string, user: User, expiresInSec: number) => {
    localStorage.setItem("chat2calendar-token", token);
    localStorage.setItem("chat2calendar-user", JSON.stringify(user));
    localStorage.setItem("chat2calendar-expires", (Date.now() + expiresInSec * 1000).toString());
    apiClient.setAuthToken(token);
  };

  const loadSession = () => {
    const token = localStorage.getItem("chat2calendar-token") || "";
    const userRaw = localStorage.getItem("chat2calendar-user");
    const expRaw = localStorage.getItem("chat2calendar-expires");
    const user = userRaw ? (JSON.parse(userRaw) as User) : null;
    const exp = expRaw ? Number(expRaw) : 0;
    return { token, user, exp };
  };

  const clearSession = () => {
    localStorage.removeItem("chat2calendar-token");
    localStorage.removeItem("chat2calendar-user");
    localStorage.removeItem("chat2calendar-expires");
    apiClient.setAuthToken("");
  };

  const hydratedOnce = useRef(false);
  const didTryRefresh = useRef(false);

  useEffect(() => {
    if (hydratedOnce.current) return;
    hydratedOnce.current = true;

    (async () => {
      const { token, user, exp } = loadSession();
      if (token && user && Date.now() < exp - 5_000) {
        apiClient.setAuthToken(token);
        setAuthState({ user, isLoading: false, isAuthenticated: true });
        return;
      }

      if (!didTryRefresh.current) {
        didTryRefresh.current = true;
        const res = await apiClient.refreshSession();
        if (res?.success && res.data) {
          const { access_token, user_id, email, expires_in, name, picture } = res.data;
          apiClient.setAuthToken(access_token);
          let u: User = { id: user_id, email, name, picture};
          const me = await apiClient.getMe();
            if (me?.success && me.data) {
              u = {
                id: me.data.user_id,
                email: me.data.email,
                name: me.data.name,
                picture: me.data.picture
              }
            }
          saveSession(access_token, u, Number(expires_in));
          setAuthState({ user: u, isLoading: false, isAuthenticated: true });
          return;
        }
      }

      clearSession();
      setAuthState({ user: null, isLoading: false, isAuthenticated: false });
    })();
  }, []);

  const signIn = async () => {
    setAuthState((p) => ({ ...p, isLoading: true }));
    try {
      await apiClient.initiateGoogleAuth();
    } catch {
      setAuthState({ user: null, isLoading: false, isAuthenticated: false });
    }
  };

  const completeCallback = async (code: string) => {
    setAuthState((p) => ({ ...p, isLoading: true }));
    const res = await apiClient.handleGoogleCallback(code);
    if (!res.success || !res.data) {
      clearSession();
      setAuthState({ user: null, isLoading: false, isAuthenticated: false });
      throw new Error(res.error || "Auth failed");
    }

    const { access_token, user_id, email, expires_in } = res.data;

    apiClient.setAuthToken(access_token);
    let u: User = { id: user_id, email, name: email.split("@")[0] };
    const me = await apiClient.getMe();
    if (me.success && me.data) {
      u = {
        id: me.data.user_id,
        email: me.data.email,
        name: me.data.name ?? me.data.email.split("@")[0],
        picture: me.data.picture,
      };
    }

    saveSession(access_token, u, Number(expires_in));
    setAuthState({ user: u, isLoading: false, isAuthenticated: true });
  };


  const signOut = async () => {
    try {
      await apiClient.logout();
    } finally {
      clearSession();
      setAuthState({ user: null, isLoading: false, isAuthenticated: false });
    }
  };

  return (
      <AuthContext.Provider value={{ authState, signIn, signOut, completeCallback }}>
        {children}
      </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
