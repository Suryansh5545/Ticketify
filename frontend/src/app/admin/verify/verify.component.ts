import { Component, OnInit } from '@angular/core';
import { EventDetailsService } from '../../services/event-details/event-details.service';
import { TicketDialogComponent, TicketDialogData  } from '../dialog/ticket-dialog/ticket-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-verify',
  templateUrl: './verify.component.html',
  styleUrls: ['./verify.component.scss']
})
export class VerifyComponent implements OnInit {
  TicketData: any;
  displayedColumns: string[] = ['id', 'customer_email', 'customer_phone', 'customer_name', 'referral', 'ticket_view'];
  constructor(private EventDetailsService: EventDetailsService, private dialog: MatDialog, private _snackBar: MatSnackBar) {}

  ngOnInit(): void {
    this.EventDetailsService.UnverifiedTicket().then(() => {
      this.TicketData = this.EventDetailsService.unverfiedticket;
    }).catch((error) => {
      this.TicketData = [];
    });
  }

  ViweTicket(ticket: any) {
    const dialogData: TicketDialogData = {
      ticket: ticket,
    };
    this.dialog.open(TicketDialogComponent, {
      data: dialogData,
    });
  }

}
