import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseUrl = 'http://127.0.0.1:8000/api'; // Base URL of Django backend
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
    }),
  };

  constructor(private http: HttpClient) {}

  // Login Method
  login(username: string, password: string): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/login/`,
      { username, password },
      this.httpOptions
    );
  }

  // Refresh Token Method
  refreshToken(refresh: string): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/token/refresh/`,
      { refresh },
      this.httpOptions
    );
  }

  // Query Method to interact with the chatbot
  query(userQuery: string, accessToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    });
    return this.http.post(
      `${this.baseUrl}/query/`,
      { query: userQuery },
      { headers }
    );
  }

  // Sign Up Method
  signUp(username: string, password: string): Observable<any> {
    return this.http.post(
      `${this.baseUrl}/signup/`,
      { username, password },
      this.httpOptions
    );
  }
}
