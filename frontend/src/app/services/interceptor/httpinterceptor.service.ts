import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { Router } from '@angular/router';
import { catchError } from 'rxjs/operators';

@Injectable()
export class HttpinterceptorService implements HttpInterceptor {
  constructor(private router: Router) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error) => {
        if (error.status === 401) {
          // Handle 401 Unauthorized: Redirect the user to the login page
          this.router.navigate(['/login']);
        } else if (error.status === 403) {
          // Handle 403 Forbidden: Redirect the user to a different page
          this.router.navigate(['/login']); 
        }
        // Re-throw the error to continue error handling in other parts of the application
        return throwError(error);
      })
    );
  }
}
