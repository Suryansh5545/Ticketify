import { TestBed } from '@angular/core/testing';

import { CsrfInterceptorService } from './csrf-interceptor.service';

describe('CsrfInterceptorService', () => {
  let service: CsrfInterceptorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CsrfInterceptorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
