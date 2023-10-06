import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeliveryStudentComponent } from './delivery-student.component';

describe('DeliveryStudentComponent', () => {
  let component: DeliveryStudentComponent;
  let fixture: ComponentFixture<DeliveryStudentComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DeliveryStudentComponent]
    });
    fixture = TestBed.createComponent(DeliveryStudentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
