import { Component } from '@angular/core';
import {MediaMatcher} from '@angular/cdk/layout';
import {ChangeDetectorRef, OnDestroy} from '@angular/core';

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
    { path: '/admin/events', label: 'Events', icon: 'event' },
    { path: '/admin/addon', label: 'Addons', icon: 'add_circle' },
  ];
  private _mobileQueryListener: () => void;
  constructor(changeDetectorRef: ChangeDetectorRef, media: MediaMatcher) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
  }
}
