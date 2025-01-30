import { Component } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-query',
  standalone: false,
  templateUrl: './query.component.html',
  styleUrls: ['./query.component.css'],
})
export class QueryComponent {
  query: string = '';
  response: string = '';
  // accessToken: string = '';

  constructor(private authService: AuthService) {}

  sendQuery() {
    const accessToken = localStorage.getItem('accessToken');
    if (this.query.trim() &&  accessToken) {
      this.authService.query(this.query, accessToken).subscribe(
        (res) => {
          this.response = res.response;
        },
        (err) => {
          this.response = err.error.error || 'Failed to fetch response.';
        }
      );
    } else {
      this.response = 'Query or access token is missing.';
    }
  }
}
