import { Injectable, inject } from '@angular/core';
import { Router, UrlTree } from '@angular/router';
import { CanActivateFn, ActivatedRouteSnapshot, RouterStateSnapshot, UrlSegment } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
class AuthGuard {

  constructor(private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean | UrlTree {
    const isAuth = this.checkIfAuthenticated();

    if (isAuth) {
      return true;
    } else {
      return this.router.parseUrl('/login');
    }
  }

  private checkIfAuthenticated(): boolean {
    const sessionId = this.getCookie('sessionid');
    // return !!sessionId; // Return true if session ID cookie exists, otherwise false
    return true;
  }


  private getCookie(name: string): string {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || '';
    return '';
  }
}

export const isAuthGuard: CanActivateFn = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean => {
  return inject(AuthGuard).canActivate(route, state) as boolean;
}
