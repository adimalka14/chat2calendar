export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export type ChatRole = "user" | "assistant";
export interface ChatMessageDTO {
  id: string;
  content: string;
  role: ChatRole;
  timestamp: string;
}

export interface AiReplyDTO {
  reply: string;
  intent?: string | null;
  data?: Record<string, unknown> | null;
  conversation_id?: string | null;
}
export interface GoogleLoginResponse {
  // Define the structure of the Google login response here
  access_token: string
  token_type: string
  user_id: string
  email: string
  expires_in: number
  name?: string
  picture?: string
}

export interface GetGoogleLoginUrlResponse {
  login_url: string
}

export interface RefreshTokenResponse {
  access_token: string
  token_type: string
  user_id: string
  email: string
  expires_in: number
  name?: string
  picture?: string
}

export interface UserInfoResponse {
  user_id: string
  email: string
  name?: string
  picture?: string
}

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

class ApiClient {
  private baseUrl: string
  private token: string | null = null

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  setAuthToken(token: string) {
    this.token = token
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    try {
      const headers = new Headers(options.headers || {});
      if (options.body && !headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
      }
      if (this.token) headers.set("Authorization", `Bearer ${this.token}`);

      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
        credentials: "include",
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        return { success: false, error: (data as any).detail || (data as any).message || "An error occurred" };
      }
      return { success: true, data: data as T };
    } catch (e) {
      return { success: false, error: e instanceof Error ? e.message : "Network error" };
    }
  }

  // Chat API methods
  async sendAiMessage(message: string, conversationId?: string | null): Promise<ApiResponse<AiReplyDTO>> {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    return this.request<AiReplyDTO>("/ai/message", {
      method: "POST",
      body: JSON.stringify({ message, timezone, conversation_id: conversationId }),
    });
  }

  // Google OAuth API methods
  async getGoogleLoginUrl(): Promise<ApiResponse<GetGoogleLoginUrlResponse>> {
    console.log("[v0] Requesting Google login URL from:", `${this.baseUrl}/auth/google/login-url`)
    try {
      const response = await fetch(`${this.baseUrl}/auth/google/login-url`, {
        method: "GET",
        mode: "cors",
        headers: {
          Accept: "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const data = await response.json()
      return {
        success: true,
        data,
      }
    } catch (error) {
      console.error("[v0] Fetch error:", error)
      return {
        success: false,
        error: error instanceof Error ? error.message : "Network error",
      }
    }
  }

  async initiateGoogleAuth(): Promise<void> {
    console.log("[v0] Initiating Google auth...")
    const response = await this.getGoogleLoginUrl()
    console.log("[v0] Google login URL response:", response)

    if (response.success && response.data) {
      console.log("[v0] Redirecting to:", response.data.login_url)
      window.location.href = response.data.login_url
    } else {
      console.error("[v0] Failed to get Google login URL:", response.error)
      throw new Error(response.error || "Failed to get Google login URL")
    }
  }

  async handleGoogleCallback(code: string): Promise<ApiResponse<GoogleLoginResponse>> {
    return this.request<GoogleLoginResponse>("/auth/google", {
      method: "POST",
      body: JSON.stringify({ code }),
    })
  }

  async refreshSession(): Promise<ApiResponse<RefreshTokenResponse>> {
    return this.request("/auth/refresh", {
      method: "POST",
    });
  }

  async logout() {
    return this.request("/auth/logout", {
      method: "POST",
    });
  }

  async getMe(): Promise<ApiResponse<UserInfoResponse>> {
    return this.request<UserInfoResponse>("/auth/me", { method: "GET" })
  }

}

export const apiClient = new ApiClient(API_BASE_URL)
