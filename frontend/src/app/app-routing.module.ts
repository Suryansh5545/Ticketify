import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Components
import { MaintenanceComponent } from './customer/maintenance/maintenance.component';
import { DeliveryComponent } from './customer/delivery/delivery.component';
import { CheckoutComponent } from './customer/checkout/checkout.component';

// Services
import { isAuthGuard } from './services/authentication/authguard.guard';

const routes: Routes = [
  { path: '', redirectTo: 'checkout', pathMatch: 'full' },
  { path: 'checkout', component: CheckoutComponent },
  { path: 'maintenance', component: MaintenanceComponent },
  { path: 'delivery/:ticketId', component: DeliveryComponent },
  {
    path: 'admin',
    loadChildren: () =>
      import('./admin/admin.module').then((m) => m.AdminModule),
    canActivate: [isAuthGuard], // Apply the AuthGuard to the entire admin path
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
