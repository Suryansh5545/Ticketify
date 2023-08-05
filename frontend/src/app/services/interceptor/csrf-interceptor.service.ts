import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class CsrfInterceptorService implements HttpInterceptor {
  constructor() {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the CSRF token from the cookie
    const csrftoken = this.getCookie('csrftoken');

    // Clone the request and add the CSRF token to the headers
    if (csrftoken) {
      request = request.clone({
        setHeaders: {
          'X-CSRFToken': csrftoken,
        },
      });
    }

    return next.handle(request);
  }

  private getCookie(name: string): string {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || '';
    return '';
  }
}
