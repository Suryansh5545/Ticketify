import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoadingServiceComponent {
  isLoading: boolean = false;

  showLoading(): void {
    this.isLoading = true;
  }

  hideLoading(): void {
    this.isLoading = false;
  }
}
