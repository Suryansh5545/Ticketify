import { Injectable } from '@angular/core';
import { ApiService } from '../api.service/api.service.component';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class EventDetailsService {
  event: any;
  SubEvent: any;
  Addon: any;
  PromoData: any;
  CheckoutData: any;
  SalesData: any;
  SubEventData: any;
  AddonData: any;
  TicketData: any;
  CheckInResponse: any;
  CheckInData: any;
  ResendEmailResponse: any;
  TicketID: any;
  Ticket_by_list: any;

  constructor(private HttpService: ApiService, private router: Router, private _snackBar: MatSnackBar) {
  }


  EventDetails(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_event').subscribe(data => {
        this.event = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  SubEventDetails(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      if (this.event[0].id) {
        this.HttpService.get<Event[]>('event/get_sub_event/' + this.event[0].id + '/').subscribe(data => {
          this.SubEvent = data;
          resolve(); // Resolve the promise after the HTTP request is complete
        }, error => {
          reject(error); // Reject the promise if an error occurs
        });
      } else {
        reject('Event data is not available.'); // Reject the promise if event data is not available
      }
    });
  }

  AddonDetails(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_addon/' + this.event[0].id + '/').subscribe(data => {
        this.Addon = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  SendPromoCode(promoCode: string): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('event/process_promo_code/', { 'promo_code': promoCode, 'event_id': this.event[0].id }).subscribe(data => {
        this.PromoData = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  SendCheckoutData(userData: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('transactions/handle-payment/', userData).subscribe(data => {
        this.CheckoutData = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  GetSalesData(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_max_ticket_sales/' + this.event[0].id + "/").subscribe(data => {
        this.SalesData = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  GetSubEventsSalesData(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_sub_event_sales/' + this.event[0].id + "/").subscribe(data => {
        this.SubEventData = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  GetAddonSalesData(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_addon_sales/' + this.event[0].id + "/").subscribe(data => {
        this.AddonData = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  GetTicketData(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_tickets_by_filter/', data).subscribe(data => {
        this.TicketData = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
        this._snackBar.open(error.error.message, 'Close', {
          duration: 2000,
          });
      });
    });
  }

  SendCheckIn(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/handle_check_in/', data).subscribe(data => {
        this.CheckInResponse = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
        this._snackBar.open(error.error.message, 'Close', {
          duration: 2000,
          });
      });
    });
  }

  GetCheckInData(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_check_in_data/', data).subscribe(data => {
        this.CheckInData = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  trigger_resend_email(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/resend_email/', data).subscribe(data => {
        this.ResendEmailResponse = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
      });
    });
  }

  get_ticket_id(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_ticket_id/', data).subscribe(data => {
        this.TicketID = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        reject(error); // Reject the promise if an error occurs
        this._snackBar.open(error.error.message, 'Close', {
          duration: 2000,
          });
      });
    });
  }

  get_ticket_by_subevent(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_ticket_by_subevents/', data).subscribe(data => {
        this.Ticket_by_list = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        this.Ticket_by_list = [];
        reject(error); // Reject the promise if an error occurs
        this._snackBar.open(error.error.message, 'Close', {
          duration: 2000,
          });
      });
    });
  }

  get_ticket_by_addon(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_ticket_by_addons/', data).subscribe(data => {
        this.Ticket_by_list = data;
        resolve(); // Resolve the promise after the HTTP request is complete
      }, error => {
        this.Ticket_by_list = [];
        reject(error); // Reject the promise if an error occurs
        this._snackBar.open(error.error.message, 'Close', {
          duration: 2000,
          });
      });
    });
  }

}