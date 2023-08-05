import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApiServiceComponent } from './api.service.component';

describe('ApiServiceComponent', () => {
  let component: ApiServiceComponent;
  let fixture: ComponentFixture<ApiServiceComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ApiServiceComponent]
    });
    fixture = TestBed.createComponent(ApiServiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
