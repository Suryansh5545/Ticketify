import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { EventDetailsService } from '../../services/event-details/event-details.service';

@Component({
  selector: 'app-delivery',
  templateUrl: './delivery.component.html',
  styleUrls: ['./delivery.component.scss']
})
export class DeliveryComponent implements OnInit {
shownnote = false;
  taskId: any;
  interval: any;
  ticketUrl: any;
  constructor(private route: ActivatedRoute, private EventDetailsService: EventDetailsService) { 
    setTimeout(() => {
      this.shownnote = true;
    }
    , 20000);
  }

  ngOnInit() {
    this.route.paramMap.subscribe((params: ParamMap) => {
      this.taskId = params.get('ticketId');
    });
    // Check the task status every 5 to 10 seconds using setInterval
    this.interval = setInterval(() => {
      this.checkTaskStatus();
    }, 5000);
  }

  checkTaskStatus() {
    const data = {
      'task_id': this.taskId
    }
    this.EventDetailsService.get_ticket_by_task(data).then(() => {
      this.ticketUrl = this.EventDetailsService.task_result;
      clearInterval(this.interval);
    });
  }


}
