import { Component } from '@angular/core';
import { EventDetailsService } from './services/event-details/event-details.service';
import { HttpClient } from '@angular/common/http';
import { ElementRef, Renderer2 } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
}
