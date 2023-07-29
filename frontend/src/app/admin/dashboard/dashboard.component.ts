import { Component, OnInit } from '@angular/core';
import { EventDetailsService } from 'src/app/services/event-details/event-details.service';
import { Chart, registerables, Colors } from 'chart.js';
Chart.register(...registerables);
Chart.register(Colors);

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  SalesData: any;
  SubEventData: any;
  AddonData: any;

constructor(private EventDetailsService: EventDetailsService) {}

ngOnInit(): void {
  this.EventDetailsService.EventDetails().then(() => {
    this.EventDetailsService.GetSalesData().then(() => {
      this.SalesData = this.EventDetailsService.SalesData;
    });
    this.EventDetailsService.GetSubEventsSalesData().then(() => {
      this.SubEventData = this.EventDetailsService.SubEventData;
      this.Createchart(document.getElementById('SubEventSaleChart'), this.SubEventData.label, this.SubEventData.data);
    });
    this.EventDetailsService.GetAddonSalesData().then(() => {
      this.AddonData = this.EventDetailsService.AddonData;
      this.Createchart(document.getElementById('AddonSaleChart'), this.AddonData.label, this.AddonData.data);
    });
  });
}

Createchart(ctx: any, labelData: any, salesData: any, label: any = 'Sales') {
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labelData,
      datasets: [{
        label: label,
        data: salesData,
        backgroundColor: [
          'rgb(126, 191, 241)',
          'rgb(255, 159, 64)',
          'rgb(255, 255, 0)',
          'rgb(160, 160, 160)'
        ],
        borderColor: [
          'rgb(126, 191, 241)',
          'rgb(255, 159, 64)',
          'rgb(255, 255, 0)',
          'rgb(160, 160, 160)'
        ],
        borderWidth: 1,
        barThickness: 20,
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: "white",
            font: {
                  size: 14,
            }
          }
        },
        x: {
          beginAtZero: true,
          ticks: {
            color: "white",
          }
        }
      },
      plugins: {
        legend: {
            labels: {
              color: "white",
              font: {
                    size: 14,
                }
            }
        }
    },
    layout: {
      padding: 20
  }
    }
  });
}
}
