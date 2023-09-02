import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { CustomerModule } from './customer/customer.module';
import { AdminModule } from './admin/admin.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// Angular Material
import {MatSnackBarModule} from '@angular/material/snack-bar';

// Services
import { ApiService, httpInterceptorProviders  } from './services/api.service/api.service.component';
import { EventDetailsService } from './services/event-details/event-details.service';
import { HttpinterceptorService } from './services/interceptor/httpinterceptor.service';



@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    CustomerModule,
    AdminModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatSnackBarModule,
  ],
  providers: [ApiService, EventDetailsService, 
    { provide: HTTP_INTERCEPTORS, useClass: HttpinterceptorService, multi: true }, httpInterceptorProviders ],
  bootstrap: [AppComponent]
})
export class AppModule { }
