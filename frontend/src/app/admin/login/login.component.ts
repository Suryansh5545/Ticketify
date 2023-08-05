import { Component } from '@angular/core';
import { EventDetailsService } from '../../services/event-details/event-details.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  username: string | undefined;
  password: string | undefined;

  constructor(private EventDetailsService: EventDetailsService, private router: Router) { }

  login() {
    const data = {
      username: this.username,
      password: this.password
    }
    this.EventDetailsService.send_login_data(data).then(() => {
      this.router.navigate(['/admin/dashboard']);
    });
  }
}
