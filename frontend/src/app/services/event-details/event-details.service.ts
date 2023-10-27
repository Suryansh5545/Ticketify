import { Injectable } from '@angular/core';
import { ApiService } from '../api.service/api.service.component';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpHeaders } from '@angular/common/http';

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
  task_result: any;
  unverfiedticket: any;
  VerifyResponse: any;
  DeclineResponse: any;

  constructor(private HttpService: ApiService, private router: Router, private _snackBar: MatSnackBar) {
  }


  EventDetails(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_event').subscribe(data => {
        this.event = data;
        resolve();
      }, error => {
        this.router.navigate(['/maintenance']);
        reject(error); 
      });
    });
  }

  EventDetailsCustomer(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_event').subscribe(data => {
        this.event = data;
        if(this.event[0].maintaince_mode == true){
          this.router.navigate(['/maintenance']);
        }
        resolve();
      }, error => {
        this.router.navigate(['/maintenance']);
        reject(error); 
      });
    });
  }

  SubEventDetails(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      if (this.event[0].id) {
        this.HttpService.get<Event[]>('event/get_sub_event/' + this.event[0].id + '/').subscribe(data => {
          this.SubEvent = data;
          resolve();
        }, error => {
          reject(error);
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
        resolve();
      }, error => {
        reject(error);
      });
    });
  }

  SendPromoCode(promoCode: string): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('event/process_promo_code/', { 'promo_code': promoCode, 'event_id': this.event[0].id }).subscribe(data => {
        this.PromoData = data;
        resolve();
      }, error => {
        reject(error);
        this._snackBar.open(error.error.error, 'Close', {
          duration: 2000,
          });
      });
    });
  }

  SendCheckoutData(userData: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('transactions/handle-payment/', userData).subscribe(data => {
        this.CheckoutData = data;
        resolve();
      }, error => {
        reject(error);
      });
    });
  }

  GetSalesData(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_max_ticket_sales/' + this.event[0].id + "/").subscribe(data => {
        this.SalesData = data;
        resolve();
      }, error => {
        reject(error);
      });
    });
  }

  GetSubEventsSalesData(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_sub_event_sales/' + this.event[0].id + "/").subscribe(data => {
        this.SubEventData = data;
        resolve();
      }, error => {
        reject(error);
      });
    });
  }

  GetAddonSalesData(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.get<Event[]>('event/get_addon_sales/' + this.event[0].id + "/").subscribe(data => {
        this.AddonData = data;
        resolve();
      }, error => {
        reject(error);
      });
    });
  }

  GetTicketData(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_tickets_by_filter/', data).subscribe(data => {
        this.TicketData = data;
        resolve();
      }, error => {
        reject(error);
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
        resolve();
      }, error => {
        reject(error);
        this._snackBar.open(error.error.message, 'Close', {
          duration: 6000,
          });
      });
    });
  }

  GetCheckInData(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_check_in_data/', data).subscribe(data => {
        this.CheckInData = data;
        resolve();
      }, error => {
        reject(error);
      });
    });
  }

  trigger_resend_email(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/resend_email/', data).subscribe(data => {
        this.ResendEmailResponse = data;
        resolve();
      }, error => {
        reject(error);
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
        resolve();
      }, error => {
        this.Ticket_by_list = [];
        reject(error);
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
        resolve();
      }, error => {
        this.Ticket_by_list = [];
        reject(error);
        this._snackBar.open(error.error.message, 'Close', {
          duration: 2000,
          });
      });
    });
  }

  send_login_data(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
      this.HttpService.post<Event[]>('login/', data).subscribe(data => {
        resolve();
      }, error => {
        reject(error);
        this._snackBar.open(error.error.non_field_errors, 'Close', {
          duration: 4000,
          });
      });
    });
  }

  send_logout(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('logout/', 66).subscribe(data => {
        resolve();
      }, error => {
        reject(error);
        this._snackBar.open(error.error.message, 'Close', {
          duration: 4000,
          });
      });
    });
  }

  get_ticket_by_task(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/get_ticket_by_task/', data).subscribe(data => {
        this.task_result = data;
        resolve();
      }
      , error => {
        reject(error);
      });
    });
  }

  UnverifiedTicket(): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      if (this.event[0].id) {
        this.HttpService.get<Event[]>('ticket/get_unverified_ticket_by_time/').subscribe(data => {
          this.unverfiedticket = data;
          resolve();
        }, error => {
          reject(error);
          this._snackBar.open(error.error.message, 'Close', {
            duration: 4000,
            });
        });
      }
    });
  }

  SendVerify(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/verify_ticket/', data).subscribe(data => {
        this.VerifyResponse = data;
        resolve();
      }, error => {
        reject(error);
        this._snackBar.open(error.error.message, 'Close', {
          duration: 6000,
          });
      });
    });
  }

  SendDecline(data: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.HttpService.post<Event[]>('ticket/decline_verify_ticket/', data).subscribe(data => {
        this.DeclineResponse = data;
        resolve();
      }, error => {
        reject(error);
        this._snackBar.open(error.error.message, 'Close', {
          duration: 6000,
          });
      });
    });
  }

}