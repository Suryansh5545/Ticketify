import { Component } from '@angular/core';
import { EventDetailsService } from '../../services/event-details/event-details.service';
import { Router } from '@angular/router';
import { MatSelectChange } from '@angular/material/select';
import { environment } from 'src/environments/environment';

interface List {
  name: string;
  id: number;
}

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.scss']
})
export class ListComponent {
  Listitems: List[] = [];
  title = 'Event';
  TableData: any;
  selectedValue: any;
  currentURL = this.router.url;
  displayedColumns: string[] = ['customer_name', 'customer_phone'];
  constructor(private EventDetailsService: EventDetailsService, private router: Router,) {
    this.EventDetailsService.EventDetails().then(() => {
    if (this.currentURL.includes('admin/events')) {
        this.EventDetailsService.SubEventDetails().then(() => {
          this.Listitems = this.EventDetailsService.SubEvent;
        });
      }
    else {
      this.title = 'Addons';
      this.EventDetailsService.AddonDetails().then(() => {
        this.Listitems = this.EventDetailsService.Addon;
      });
    }
    });
   }

   change_detection(event: MatSelectChange): void {
    const newValue = event.value;
    this.selectedValue = newValue;
    const data = {
      list_id: newValue
    }
    if (this.currentURL.includes('admin/events')) {
      this.EventDetailsService.get_ticket_by_subevent(data).then(() => {
        this.TableData = this.EventDetailsService.Ticket_by_list;
      }).catch((error) => {
        this.TableData = [];
      });
    }
    else {
      this.EventDetailsService.get_ticket_by_addon(data).then(() => {
        this.TableData = this.EventDetailsService.Ticket_by_list;
      }).catch((error) => {
        this.TableData = [];
      });
    }
   }

   downloadexcel(): void {
    
    const url = `${environment.api_endpoint}ticket/get_ticket_by_subevents_excel_download/`;
    const data = {
      list_id: this.selectedValue
    }
    if (this.currentURL.includes('admin/events')) {
      window.open(url + this.selectedValue, '_blank');
    }
   }

}
