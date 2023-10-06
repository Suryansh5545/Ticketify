import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Components
import { MaintenanceComponent } from './customer/maintenance/maintenance.component';
import { DeliveryComponent } from './customer/delivery/delivery.component';
import { DeliveryStudentComponent } from './customer/delivery-student/delivery-student.component';
import { CheckoutComponent } from './customer/checkout/checkout.component';

const routes: Routes = [
  { path: '', redirectTo: 'checkout', pathMatch: 'full' },
  { path: 'checkout', component: CheckoutComponent },
  { path: 'maintenance', component: MaintenanceComponent },
  { path: 'delivery/:ticketId', component: DeliveryComponent },
  { path: 'delivery-student', component: DeliveryStudentComponent },

  {
    path: 'admin',
    loadChildren: () =>
      import('./admin/admin.module').then((m) => m.AdminModule)
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
