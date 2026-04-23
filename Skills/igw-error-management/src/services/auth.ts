import axios from "axios";
import { IgwAuthConfig, IgwTokenResponse } from "../types.js";
import { TOKEN_EXPIRY_BUFFER_MS } from "../constants.js";

export class IgwAuthManager {
  private token: IgwTokenResponse | null = null;
  private tokenExpiresAt: number = 0;
  private refreshPromise: Promise<string> | null = null;

  constructor(private readonly config: IgwAuthConfig) {}

  async getValidToken(): Promise<string> {
    // Mutex via shared promise — mirrors C# semaphore pattern
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    if (this.token && Date.now() < this.tokenExpiresAt) {
      return this.token.Token;
    }

    this.refreshPromise = this.acquireToken();
    try {
      return await this.refreshPromise;
    } finally {
      this.refreshPromise = null;
    }
  }

  private async acquireToken(): Promise<string> {
    // If we have a token but it's expired, try refresh first
    if (this.token) {
      const refreshed = await this.refreshToken(this.token);
      if (refreshed) {
        this.setToken(refreshed);
        return refreshed.Token;
      }
    }

    // Fresh login
    const loginResult = await this.login();
    if (!loginResult) {
      throw new Error("IGW login failed — check credentials");
    }
    this.setToken(loginResult);
    return loginResult.Token;
  }

  async forceRefresh(): Promise<string> {
    this.token = null;
    this.tokenExpiresAt = 0;
    this.refreshPromise = null;
    return this.getValidToken();
  }

  private setToken(response: IgwTokenResponse): void {
    this.token = response;
    this.tokenExpiresAt =
      new Date(response.Expiration).getTime() - TOKEN_EXPIRY_BUFFER_MS;
  }

  private async login(): Promise<IgwTokenResponse | null> {
    try {
      const { data } = await axios.post<IgwTokenResponse>(
        `${this.config.baseUrl}/authentication/login`,
        {
          Username: this.config.username,
          Password: this.config.password,
          WebApiKey: this.config.webApiKey,
        }
      );
      return data;
    } catch {
      return null;
    }
  }

  private async refreshToken(
    current: IgwTokenResponse
  ): Promise<IgwTokenResponse | null> {
    try {
      const { data } = await axios.post<IgwTokenResponse>(
        `${this.config.baseUrl}/authentication/refreshtoken`,
        {
          Token: current.Token,
          RefreshToken: current.RefreshToken,
        }
      );
      return data;
    } catch {
      return null;
    }
  }
}
