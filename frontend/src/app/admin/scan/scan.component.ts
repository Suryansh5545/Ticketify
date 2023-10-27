import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { EventDetailsService } from 'src/app/services/event-details/event-details.service';
import { ScannerQRCodeConfig ,NgxScannerQrcodeComponent, ScannerQRCodeResult} from 'ngx-scanner-qrcode';
import { TicketDialogComponent, TicketDialogData  } from '../dialog/ticket-dialog/ticket-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-scan',
  templateUrl: './scan.component.html',
  styleUrls: ['./scan.component.scss']
})
export class ScanComponent implements AfterViewInit {
  constructor(private EventDetailsService: EventDetailsService, private dialog: MatDialog) {}
  public config: ScannerQRCodeConfig = {
        constraints: {
      audio: false,
    },
  };

  @ViewChild('action') action!: NgxScannerQrcodeComponent;

  ngAfterViewInit(): void {
    // Start the scanner on page load
    this.startScanner();
  }

  startScanner() {
    // Call the handle method with 'start' to start the scanner and 'playDeviceFacingBack' function
    this.handle(this.action, 'start');
  }

  playDeviceFacingBack = (devices: any[]) => {
    // front camera or back camera check here!
    const device = devices.find((f) => /back|rear|environment/gi.test(f.label)); // Default Back Facing Camera
    return this.action.playDevice(device ? device.deviceId : devices[0].deviceId);
  };

  handle(action: NgxScannerQrcodeComponent, fn: string) {
    if (fn === 'start') {
      action[fn]().subscribe(
        (r: any) => console.log(fn, r),
        (error: any) => console.error('Error while starting scanner:', error)
      );
    }
    if (fn === 'stop') {
      action[fn]();
    }
  }

  public onEvent(e: ScannerQRCodeResult[], action?: any): void {
    action.stop();
    const data = {
      'ticket_id': e[0].value,
    }
    this.EventDetailsService.GetTicketData(data).then(() => {
      const dialogData: TicketDialogData = {
        ticket: this.EventDetailsService.TicketData,
      };
      let ticketdialog = this.dialog.open(TicketDialogComponent, {
        data: dialogData,
      });
      ticketdialog.afterClosed().subscribe(result => {
        this.startScanner();
      });
    });

  }

}
