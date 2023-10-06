import { Component } from '@angular/core';
import {MediaMatcher} from '@angular/cdk/layout';
import {ChangeDetectorRef, OnDestroy} from '@angular/core';
import { Router } from '@angular/router';
import { EventDetailsService } from '../../services/event-details/event-details.service';

@Component({
  selector: 'side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss']
})
export class SideBarComponent {
  mobileQuery: MediaQueryList;
  links = [
    { path: '/admin/dashboard', label: 'Dashboard', icon: 'dashboard' },
    { path: '/admin/scan', label: 'Scan', icon: 'qr_code_scanner' },
    { path: '/admin/tickets', label: 'Tickets', icon: 'confirmation_number' },
    { path: '/admin/verify', label: 'Verify', icon: 'verified' },
    { path: '/admin/events', label: 'Events', icon: 'event' },
    { path: '/admin/addon', label: 'Addons', icon: 'add_circle' },
  ];
  private _mobileQueryListener: () => void;
  constructor(changeDetectorRef: ChangeDetectorRef, media: MediaMatcher, private router: Router, private EventDetailsService: EventDetailsService) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
  }

  logout() {
    this.EventDetailsService.send_logout().then(() => {
      localStorage.clear();
      sessionStorage.clear();
      document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      this.router.navigate(['/login']);
    });
  }
}
