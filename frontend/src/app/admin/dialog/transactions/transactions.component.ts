import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface TransactionsDialogData {
  transaction: any;
}

@Component({
  selector: 'app-transactions',
  templateUrl: './transactions.component.html',
  styleUrls: ['./transactions.component.scss']
})

export class TransactionsComponent {
  displayedColumns: string[] = ['payment_id', 'order_id', 'payment_method', 'payment_status', 'payment_amount', 'payment_currency'];
  constructor(@Inject(MAT_DIALOG_DATA) public data: TransactionsDialogData) {
  }

}
