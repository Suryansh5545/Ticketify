import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EventDetailsService } from './event-details.service';

describe('EventDetailsComponent', () => {
  let component: EventDetailsService;
  let fixture: ComponentFixture<EventDetailsService>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [EventDetailsService]
    });
    fixture = TestBed.createComponent(EventDetailsService);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
