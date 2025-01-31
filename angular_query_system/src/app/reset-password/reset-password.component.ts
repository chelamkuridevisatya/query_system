import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-reset-password',
  standalone: false,
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css'], // Fix typo
})
export class ResetPasswordComponent {
  newPassword: string = '';

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  resetPassword() {
    const token = this.route.snapshot.paramMap.get('token');
    const uid = this.route.snapshot.paramMap.get('uid');

    if (!this.newPassword.trim()) {
      alert('Please enter a new password.');
      return;
    }

    this.http.post(`http://localhost:8000/api/reset-password/${uid}/${token}/`, { new_password: this.newPassword })
      .subscribe(
        (response) => {
          alert('Password reset successful!');
        },
        (error) => {
          alert('Error: ' + (error.error.error || 'Something went wrong.'));
        }
      );
  }
}
