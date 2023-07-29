import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class ApiService {
  API = environment.api_endpoint;
  HEADERS = { 'Content-Type': 'application/json' };
  HTTP_OPTIONS: any;

    /**
   * Constructor.
   * @param http  Http Injection.
   * @param globalService  GlobalService Injection.
   */
    constructor(private http: HttpClient) {}

    get<T>(endpoint: string): Observable<T> {
      const url = `${this.API}${endpoint}`;
      const headers = this.HEADERS;
      return this.http.get<T>(url, { headers });
    }
  
    post<T>(endpoint: string, data: any): Observable<T> {
      const url = `${this.API}${endpoint}`;
      const headers = this.HEADERS;
      return this.http.post<T>(url, data, { headers });
    }

}
