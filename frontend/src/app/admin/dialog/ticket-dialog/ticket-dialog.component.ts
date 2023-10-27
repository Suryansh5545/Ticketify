import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { EventDetailsService } from 'src/app/services/event-details/event-details.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TransactionsComponent } from '../transactions/transactions.component';
import { MatDialog } from '@angular/material/dialog';


export interface TicketDialogData {
  ticket: any;
}

@Component({
  selector: 'app-ticket-dialog',
  templateUrl: './ticket-dialog.component.html',
  styleUrls: ['./ticket-dialog.component.scss']
})
export class TicketDialogComponent {
  ticket_data= {};
  CheckInData: any;
  ticket_id: any;
  displayedColumns: string[] = ['ticket_id', 'check_in_time', 'operator', 'method'];
  constructor(@Inject(MAT_DIALOG_DATA) public data: TicketDialogData, private EventDetailsService: EventDetailsService,
   private _snackBar: MatSnackBar, public dialogRef: MatDialogRef<TicketDialogComponent>, private dialog: MatDialog) {
    this.ticket_id = {
      ticket_id: this.data.ticket.id
    }
    this.EventDetailsService.GetCheckInData(this.ticket_id).then(() => {
      this.CheckInData = this.EventDetailsService.CheckInData;

    });
  }

  ResendEmail() {
    this.EventDetailsService.trigger_resend_email(this.ticket_id).then(() => {
      this._snackBar.open(this.EventDetailsService.ResendEmailResponse.message, 'Close');
    });
  }

  OpenTransaction() {
    this.dialog.open(TransactionsComponent, {
      data: { transaction: this.data.ticket.transaction_id }
    });
  }

  OpenVerification() {
    window.open(this.data.ticket.verification_id, "_blank");
  }

  confirmVerification() {
    const isConfirmed = window.confirm('Are you sure you want to verify this ticket? This action cannot be undone.');
    if (isConfirmed) {
      this.Verify(); // Call your Verify() function if the user confirmed.
    }
  }

  Verify() {
    this.EventDetailsService.SendVerify(this.ticket_id).then(() => {
      this._snackBar.open(this.EventDetailsService.VerifyResponse.message, 'Close');
    });
  }

  Decline() {
    this.EventDetailsService.SendDecline(this.ticket_id).then(() => {
      this._snackBar.open(this.EventDetailsService.DeclineResponse.message, 'Close');
    });
  }

  confirmCheckin() {
    const isConfirmed = window.confirm('Are you sure you want to check in this ticket? This action cannot be undone. Please use QR Scanner if available.');
    if (isConfirmed) {
      this.Checkin(); // Call your Checkin() function if the user confirmed.
    }
  }

  Checkin() {
    this.ticket_data = {
      ticket_id: this.data.ticket.id,
      operator: "Admin",
    }
    this.EventDetailsService.SendCheckIn(this.ticket_data).then(() => {
      this._snackBar.open(this.EventDetailsService.CheckInResponse.message, 'Close');
    });
    this.dialogRef.close();

  }
}
