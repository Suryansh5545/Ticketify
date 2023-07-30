import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderComponent } from './header/header.component';
import { FormsModule } from '@angular/forms';
import { Routes , RouterModule } from '@angular/router';
import { CheckoutComponent } from './checkout/checkout.component';
import { SideBarComponent } from './side-bar/side-bar.component';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { TicketsComponent } from './admin/tickets/tickets.component';
import { TicketDialogComponent } from './admin/dialog/ticket-dialog/ticket-dialog.component';
import { ScanComponent } from './admin/scan/scan.component';
import { TransactionsComponent } from './admin/dialog/transactions/transactions.component';

// Angular Material
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatListModule} from '@angular/material/list';
import {MatIconModule} from '@angular/material/icon';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatTableModule} from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatDialogModule } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatSelectModule} from '@angular/material/select'; 

// Font Awesome
import { FontAwesomeModule, FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';

// NPM Module
import { NgxScannerQrcodeModule } from 'ngx-scanner-qrcode';
import { ListComponent } from './admin/list/list.component';
import { LoginComponent } from './admin/login/login.component';

// Services
import { ApiService, httpInterceptorProviders  } from './services/api.service/api.service.component';
import { EventDetailsService } from './services/event-details/event-details.service';
import { isAtuhGuard } from './services/authentication/authguard.guard';
import { HttpinterceptorService } from './services/interceptor/httpinterceptor.service';

const routes: Routes = [
  { path: 'login', component: LoginComponent},
  { path: '', redirectTo: 'checkout', pathMatch: 'full' },
  { path: 'checkout', component: CheckoutComponent },
  {
    path: 'admin',
    component: SideBarComponent, // AdminComponent will be displayed in the main router-outlet
    canActivate: [isAtuhGuard],
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' }, // Redirect to dashboard as the default child route for /admin
      { path: 'dashboard', component: DashboardComponent }, // DashboardComponent will be displayed in the router-outlet of AdminComponent
      { path: 'tickets', component: TicketsComponent },
      { path: 'scan', component: ScanComponent },
      { path: 'events', component: ListComponent },
      { path: 'addon', component: ListComponent },
    ],
  },
];



@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    CheckoutComponent,
    SideBarComponent,
    DashboardComponent,
    TicketsComponent,
    TicketDialogComponent,
    ScanComponent,
    TransactionsComponent,
    ListComponent,
    LoginComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatCardModule,
    MatCheckboxModule,
    MatFormFieldModule,
    MatListModule,
    MatIconModule,
    FontAwesomeModule,
    MatSidenavModule,
    MatToolbarModule,
    FormsModule,
    MatTableModule,
    MatInputModule,
    MatDialogModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    NgxScannerQrcodeModule,
    MatSlideToggleModule,
    MatSelectModule,
    RouterModule.forRoot(routes),
  ],
  providers: [ApiService, EventDetailsService, 
    { provide: HTTP_INTERCEPTORS, useClass: HttpinterceptorService, multi: true }, httpInterceptorProviders ],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(library: FaIconLibrary) {
    library.addIconPacks(fas, far);
  }
 }
