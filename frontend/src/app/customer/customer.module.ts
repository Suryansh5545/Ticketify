import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

// Components
import { CheckoutComponent } from './checkout/checkout.component';
import { DeliveryComponent } from './delivery/delivery.component';
import { DeliveryStudentComponent } from './delivery-student/delivery-student.component';
import { MaintenanceComponent } from './maintenance/maintenance.component';

// Angular Material
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatListModule} from '@angular/material/list';
import {MatIconModule} from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';

// Font Awesome
import { FontAwesomeModule, FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';


const customerRoutes = [
  { path: 'maintenance', component: MaintenanceComponent },
  { path: 'delivery/:ticketId', component: DeliveryComponent },
  { path: 'delivery-student', component: DeliveryStudentComponent },

  { path: 'checkout', component: CheckoutComponent },
];



@NgModule({
  declarations: [
    CheckoutComponent,
    DeliveryComponent,
    MaintenanceComponent,
    DeliveryStudentComponent
  ],
  imports: [
    CommonModule,
    MatButtonModule,
    MatListModule,
    MatIconModule,
    MatCardModule,
    MatCheckboxModule,
    MatInputModule,
    MatProgressSpinnerModule,
    FontAwesomeModule,
    FormsModule,
    RouterModule.forChild(customerRoutes)
  ],
  exports: [
    CheckoutComponent,
    DeliveryComponent,
    DeliveryStudentComponent,
    MaintenanceComponent,
    RouterModule
  ]
})
export class CustomerModule {
  constructor(library: FaIconLibrary) {
    library.addIconPacks(fas, far);
  }
 }
