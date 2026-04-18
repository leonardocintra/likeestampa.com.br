import type { Address } from "./order";

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  document?: string;
  dateOfBirth?: string;
  gender?: "male" | "female" | "other";
  addresses: Address[];
  preferences: {
    newsletter: boolean;
    sms: boolean;
    whatsapp: boolean;
  };
  createdAt: string;
  updatedAt: string;
  lastLoginAt?: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone?: string;
  acceptsTerms: boolean;
  acceptsNewsletter?: boolean;
}

export interface LoginResponse {
  user: User;
  tokens: AuthTokens;
}

export interface UpdateProfileRequest {
  firstName?: string;
  lastName?: string;
  phone?: string;
  dateOfBirth?: string;
  gender?: "male" | "female" | "other";
  preferences?: {
    newsletter?: boolean;
    sms?: boolean;
    whatsapp?: boolean;
  };
}

export interface ChangePasswordRequest {
  currentPassword: string;
  newPassword: string;
}
