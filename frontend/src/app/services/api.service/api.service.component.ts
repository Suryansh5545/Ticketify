import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders, HTTP_INTERCEPTORS } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CsrfInterceptorService } from '../interceptor/csrf-interceptor.service';

@Injectable()
export class ApiService {
  API = environment.api_endpoint;
  private HEADERS = new HttpHeaders({
    'Content-Type': 'application/json',
  });
  HTTP_OPTIONS: any;

    /**
   * Constructor.
   * @param http  Http Injection.
   * @param globalService  GlobalService Injection.
   */
    constructor(private http: HttpClient) {}

    get<T>(endpoint: string, withCredentials: boolean = true): Observable<T> {
      const url = `${this.API}${endpoint}`;
      const options = { headers: this.HEADERS, withCredentials: withCredentials };
      return this.http.get<T>(url, options);
    }
  
    post<T>(endpoint: string, data: any, withCredentials: boolean = true): Observable<T> {
      const url = `${this.API}${endpoint}`;
      const options = { headers: this.HEADERS, withCredentials: withCredentials };
      return this.http.post<T>(url, data, options);
    }    

}

export const httpInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: CsrfInterceptorService, multi: true },
];
