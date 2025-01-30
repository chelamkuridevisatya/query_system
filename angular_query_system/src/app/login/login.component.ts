import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';  // Import Router for navigation

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

  constructor(private authService: AuthService, private router: Router) {}

  login() {
    if (this.username.trim() && this.password.trim()) {
      this.authService.login(this.username, this.password).subscribe(
        (response) => {
          // Store the tokens if needed
          this.accessToken = response.access;
          this.refreshToken = response.refresh;

          // Store the access token in localStorage (optional)
          localStorage.setItem('accessToken', this.accessToken);
          localStorage.setItem('refreshToken', this.refreshToken);

          // Show success message
          this.successMessage = 'Login successful!';
          this.errorMessage = '';

          // Redirect to the query page after successful login
          this.router.navigate(['/query']);
        },
        (error) => {
          // Show error message if login fails
          this.errorMessage = error.error.error || 'Login failed.';
          this.successMessage = '';
        }
      );
    } else {
      // Handle empty username or password
      this.errorMessage = 'Username and password are required.';
    }
  }
}

