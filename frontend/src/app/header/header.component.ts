import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {
  constructor(private router: Router, private route: ActivatedRoute) {}
  isCheckoutURL(): boolean {
    // Check if the current URL is the "home" URL
    return this.router.isActive('/checkout', true);
  }
}
