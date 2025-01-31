import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http'; // Import HttpClient

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';
  successMessage: string = '';
  accessToken: string = '';
  refreshToken: string = '';

  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient // Inject HttpClient
  ) {}

  login() {
    if (this.username.trim() && this.password.trim()) {
      this.authService.login(this.username, this.password).subscribe(
        (response) => {
          this.accessToken = response.access;
          this.refreshToken = response.refresh;

          localStorage.setItem('accessToken', this.accessToken);
          localStorage.setItem('refreshToken', this.refreshToken);

          this.successMessage = 'Login successful!';
          this.errorMessage = '';

          this.router.navigate(['/query']); // Redirect to query page
        },
        (error) => {
          this.errorMessage = error.error.error || 'Login failed.';
          this.successMessage = '';
        }
      );
    } else {
      this.errorMessage = 'Username and password are required.';
    }
  }

  forgotPassword() {
    const email = prompt('Enter your registered email:');
    if (email) {
      this.http.post('http://localhost:8000/api/forgot-password/', { email }).subscribe(
        (response) => {
          alert('Reset link has been sent to your email.');
        },
        (error) => {
          alert('Error: ' + (error.error.error || 'Something went wrong.'));
        }
      );
    }
  }
}
