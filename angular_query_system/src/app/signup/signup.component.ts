import { Component } from '@angular/core';
import { AuthService } from '../auth.service';  // Import AuthService to interact with the backend

@Component({
  selector: 'app-signup',
  standalone: false,
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  username: string = '';
  password: string = '';
  confirmPassword: string = '';
  errorMessage: string = '';
  successMessage: string = '';

  constructor(private authService: AuthService) {}

  signUp() {
    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match.';
      this.successMessage = '';
      return;
    }
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/;
    if (!passwordPattern.test(this.password)) {
      this.errorMessage = 'Password must be at least 8 characters long, contain at least one digit and one special symbol.';
      this.successMessage = '';
      return;
    }

    // Call the signup API
    this.authService.signUp(this.username, this.password).subscribe(
      (response) => {
        this.successMessage = 'Registration successful!';
        this.errorMessage = '';
      },
      (error) => {
        console.error('Signup Error: ', error);
        this.errorMessage = 'Registration failed. ' + (error.error.error || 'user already exists or give correct email');
        this.successMessage = '';
      }
    );
  }
}