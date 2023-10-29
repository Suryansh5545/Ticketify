import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

// Components
import { SideBarComponent } from './side-bar/side-bar.component';
import { DashboardComponent } from '../admin/dashboard/dashboard.component';
import { TicketsComponent } from '../admin/tickets/tickets.component';
import { TicketDialogComponent } from '../admin/dialog/ticket-dialog/ticket-dialog.component';
import { ScanComponent } from '../admin/scan/scan.component';
import { TransactionsComponent } from '../admin/dialog/transactions/transactions.component';
import { ListComponent } from '../admin/list/list.component';
import { LoginComponent } from '../admin/login/login.component';
import { FormsModule } from '@angular/forms';

// Angular Material
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatListModule} from '@angular/material/list';
import {MatIconModule} from '@angular/material/icon';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatTableModule} from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatDialogModule } from '@angular/material/dialog';
import {MatSelectModule} from '@angular/material/select'; 

// NPM Module
import { NgxScannerQrcodeModule } from 'ngx-scanner-qrcode';
import { VerifyComponent } from './verify/verify.component';

// Font Awesome
import { FontAwesomeModule, FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';

const adminRoutes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: SideBarComponent,
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'tickets', component: TicketsComponent },
      { path: 'verify', component: VerifyComponent },
      { path: 'scan', component: ScanComponent },
      { path: 'events', component: ListComponent },
      { path: 'addon', component: ListComponent },
    ],
  },
];




@NgModule({
  declarations: [
    SideBarComponent,
    DashboardComponent,
    TicketsComponent,
    TicketDialogComponent,
    ScanComponent,
    TransactionsComponent,
    ListComponent,
    LoginComponent,
    VerifyComponent,
  ],
  imports: [
    CommonModule,
    MatButtonModule,
    MatCardModule,
    MatListModule,
    MatIconModule,
    MatSidenavModule,
    MatToolbarModule,
    FormsModule,
    MatTableModule,
    MatInputModule,
    MatDialogModule,
    NgxScannerQrcodeModule,
    MatSelectModule,
    FontAwesomeModule,
    RouterModule.forChild(adminRoutes),
  ], 
  exports: [
    SideBarComponent,
    DashboardComponent,
    TicketsComponent,
    TicketDialogComponent,
    ScanComponent,
    TransactionsComponent,
    ListComponent,
    LoginComponent,
    RouterModule
  ]
})
export class AdminModule { 
  constructor(library: FaIconLibrary) {
    library.addIconPacks(fas, far);
  }
 }
