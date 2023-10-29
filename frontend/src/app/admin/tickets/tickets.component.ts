import { Component } from '@angular/core';
import { EventDetailsService } from 'src/app/services/event-details/event-details.service';
import { TicketDialogComponent, TicketDialogData  } from '../dialog/ticket-dialog/ticket-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-tickets',
  templateUrl: './tickets.component.html',
  styleUrls: ['./tickets.component.scss']
})
export class TicketsComponent {
  email: any;
  phone: any;
  name: any;
  referral: any;
  TicketData: any;
  TotalTickets: any = 0;
  displayedColumns: string[] = ['id', 'customer_email', 'customer_phone', 'customer_name', 'referral', 'selected_sub_event', 'selected_addon', 'ticket_view'];
  constructor(private EventDetailsService: EventDetailsService, private dialog: MatDialog, private _snackBar: MatSnackBar) { }
  search() {
    if (this.email == undefined && this.phone == undefined && this.name == undefined && this.referral == undefined) {
      this._snackBar.open("Please enter any one of the field", "Close")
      return;
    }
    const data = {
      'email': this.email,
      'phone': this.phone,
      'name': this.name,
      'referral': this.referral
    }
    this.EventDetailsService.GetTicketData(data).then(() => {
      this.TicketData = this.EventDetailsService.TicketData;
      this.TotalTickets = this.TicketData.length;
    }).catch((error) => {
      this.TicketData = [];
      this.TotalTickets = 0;
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

  downloadexcel(): void {
    
    const url = `${environment.api_endpoint}ticket/get_all_tickets_excel/`;
      window.open(url, '_blank');
   }

}
