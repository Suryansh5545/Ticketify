import { Component } from '@angular/core';
import { EventDetailsService } from '../../services/event-details/event-details.service';
import { HttpClient } from '@angular/common/http';
import { ElementRef, Renderer2 } from '@angular/core';
import { LoadingServiceComponent } from '../../loading-service/loading-service.component';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss']
})
export class CheckoutComponent {

  eventdata: any;
  SubEvents: any;
  Addons: any;
  isDiscountApplied = false;
  DiscountValue: number = 0;
  SubEventsSelected: any = [];
  SubEventsIncluded: number = 0;
  PremiumSubEventsIncluded: number = 0;
  AddonsSelected: any = [];
  TotalPrice: number = 0;
  showCouponInput: boolean = false;
  couponCode: string = '';
  appliedCoupon: string = '';
  isMobile: boolean = false;
  agreeToTerms: boolean = false;
  studentType: string = 'COLLEGE';
  selectedFile: File | null = null;
  selectedImageSrc: string = '';
  ImageFile: Blob | undefined;
  ImageBase64: string | undefined;
  

  constructor(
    private http: HttpClient,
    private EventDetailsService: EventDetailsService, private renderer: Renderer2, 
    private elementRef: ElementRef, public loadingService: LoadingServiceComponent,
    private _snackBar: MatSnackBar) {
      this.selectedFile = null;
    }

    ngOnInit() {
      this.checkIfMobile();
      this.EventDetailsService.EventDetailsCustomer().then(() => {
        this.eventdata = this.EventDetailsService.event;
        this.TotalPrice += parseFloat(this.eventdata[0].price);
        this.EventDetailsService.SubEventDetails().then(() => {
          this.SubEvents = this.EventDetailsService.SubEvent;
          this.EventDetailsService.AddonDetails().then(() => {
            this.Addons = this.EventDetailsService.Addon;
          });
        });
      });
    }

    onFileChange(event: any) {
      this.selectedFile = event.target.files[0]; 
      if (this.selectedFile) {
        const reader = new FileReader();
        reader.onload = (e: any) => {
          this.selectedImageSrc  = e.target.result;
          if (this.selectedImageSrc) {
            this.blobToBase64(this.dataURItoBlob(this.selectedImageSrc), (base64String) => {
              this.ImageBase64 = base64String;
            });
          } else {
            this.ImageFile = undefined;
          }
        };
        reader.readAsDataURL(this.selectedFile);
      }
    }

    onStudentTypeChange(event: any) {
      if (event.target.value != this.studentType && this.isDiscountApplied == false) {
        if (event.target.value == "SCHOOL") {
          this.TotalPrice -= parseFloat(this.eventdata[0].price);
          this.TotalPrice += parseFloat(this.eventdata[0].student_price);
        }
        else {
          this.TotalPrice -= parseFloat(this.eventdata[0].student_price);
          this.TotalPrice += parseFloat(this.eventdata[0].price);
        }
      }
      this.studentType = event.target.value;
    }

    checkIfMobile() {
      const mobileBreakpoint = 780; // Adjust this value based on your requirements
  
      if (window.innerWidth < mobileBreakpoint) {
        this.isMobile = true;
      }
    }

    toggleDescription(eventItem: any, event: Event) {
      event.preventDefault();
      eventItem.showDescription = !eventItem.showDescription;
    }

    toggleCouponInput() {
      this.showCouponInput = !this.showCouponInput;
    }

    applyCoupon(coupon: any) {
      if ( this.isDiscountApplied == false &&  this.studentType != 'SCHOOL') {
      this.EventDetailsService.SendPromoCode(coupon).then(() => {
        if (this.EventDetailsService.PromoData.discount) {
          this.appliedCoupon = coupon;
          this.isDiscountApplied = true;
          this.DiscountValue = this.EventDetailsService.PromoData.discount;
          this.TotalPrice = this.TotalPrice - this.DiscountValue;
          this._snackBar.open('Coupon Applied', 'Close', {
            duration: 3000,
          });
        }
    });
  }
    }

    SelectSubEvent(event: any, subEvent: any) {
      if (subEvent.type == 'premium') {
        if (event.checked) {
          if (this.PremiumSubEventsIncluded+1 > this.EventDetailsService.event[0].flagship_event_included_allowed) {
          this.TotalPrice += parseFloat(subEvent.price);
          subEvent.given = false;
          this.SubEventsSelected.push(subEvent);
          }
          else {
            subEvent.given = true;
            this.SubEventsSelected.push(subEvent);
            this.PremiumSubEventsIncluded += 1;
          }
        } else {
          if (subEvent.given == false || this.PremiumSubEventsIncluded > this.EventDetailsService.event[0].flagship_event_included_allowed) {
            this.TotalPrice -= parseFloat(subEvent.price);
          }
          this.SubEventsSelected.splice(this.SubEventsSelected.indexOf(subEvent), 1);
          let executed = 0;
          for (let i = 0; i < this.SubEventsSelected.length && executed < this.EventDetailsService.event[0].flagship_event_included_allowed; i++) {
            if(this.SubEventsSelected[i].type == 'premium') {
              executed += 1;
              if (this.SubEventsSelected[i].given == false) {
                  this.TotalPrice -= parseFloat(this.SubEventsSelected[i].price);
                this.SubEventsSelected[i].given = true;
                }
            }
          }
          let count = 0;
          this.SubEventsSelected.forEach((subEvent: any) => {
            if (subEvent.type != 'standard') {
            if (subEvent.given == true) {
              count += 1;
            }
            }
          });
          this.PremiumSubEventsIncluded = count;
      }
      }
      else {
        if (event.checked) {
          if (this.SubEventsIncluded+1 > this.EventDetailsService.event[0].sub_events_included_allowed) {
          this.TotalPrice += parseFloat(subEvent.price);
          subEvent.given = false;
          this.SubEventsSelected.push(subEvent);
          }
          else {
            subEvent.given = true;
            this.SubEventsSelected.push(subEvent);
            this.SubEventsIncluded += 1;
          }
        } else {
          if (subEvent.given == false || this.SubEventsIncluded > this.EventDetailsService.event[0].sub_events_included_allowed) {
            this.TotalPrice -= parseFloat(subEvent.price);
          }
          this.SubEventsSelected.splice(this.SubEventsSelected.indexOf(subEvent), 1);
          let executed = 0;
          for (let i = 0; i < this.SubEventsSelected.length && executed < this.EventDetailsService.event[0].sub_events_included_allowed; i++) {
            if(this.SubEventsSelected[i].type == 'standard') {
            executed += 1;
            if (this.SubEventsSelected[i].given == false) {
                this.TotalPrice -= parseFloat(this.SubEventsSelected[i].price);
              this.SubEventsSelected[i].given = true;
              }
            }
          }
          let count = 0;
          this.SubEventsSelected.forEach((subEvent: any) => {
            if (subEvent.type != 'premium') {
            if (subEvent.given == true) {
              count += 1;
            }
            }
          });
          this.SubEventsIncluded = count;
        }
      }
  }

    onAddonSelectionChange(addonlist: any) {
      const previouslySelectedAddons = this.AddonsSelected;
      this.AddonsSelected = addonlist.selectedOptions.selected.map((option: { value: any; }) => option.value);
      const deselectedAddons = previouslySelectedAddons.filter(
        (addon: any) => !this.AddonsSelected.includes(addon)
      );
      const newlySelectedAddons = this.AddonsSelected.filter(
        (addon: any) => !previouslySelectedAddons.includes(addon)
      );
      let priceDifference = 0;
      deselectedAddons.forEach((addon: any) => {
        priceDifference -= parseFloat(addon.price);
      });
      newlySelectedAddons.forEach((addon: any) => {
        priceDifference += parseFloat(addon.price);
      });
      this.TotalPrice += priceDifference;
    }

    Checkout() {
      var nameInput = document.getElementById("name") as HTMLInputElement;
      var emailInput = document.getElementById("email") as HTMLInputElement;
      var phoneNumberInput = document.getElementById("phone") as HTMLInputElement;
      var referralInput = document.getElementById("referral") as HTMLInputElement;
      var institutenameInput = document.getElementById("institutename") as HTMLInputElement;
      var studentTypeInput = document.querySelector('input[name="studentType"]:checked') as HTMLInputElement;
      const studentType = studentTypeInput ? studentTypeInput.value : '';
      
      if(nameInput.value == '' || emailInput.value == '' || phoneNumberInput.value == '') {
        this._snackBar.open('Please fill all the required fields', 'Close', {
          duration: 3000,
        });
        return;
      }
      else if (phoneNumberInput.value.length != 10 || phoneNumberInput.value.match(/^[0-9]+$/) == null) {
        this._snackBar.open('Please enter a valid phone number', 'Close', {
          duration: 3000,
        });
        return;
      }
      else if (emailInput.value.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) == null) {
        this._snackBar.open('Please enter a valid email address', 'Close', {
          duration: 3000,
        });
        return;
      }
      else if (institutenameInput.value == '' || studentType === '') {
        this._snackBar.open('Please fill all the required fields', 'Close', {
          duration: 3000,
        });
        return;
      }
      else if (this.studentType == 'SCHOOL' && this.ImageBase64 == null) {
        this._snackBar.open('Please upload a valid School ID proof', 'Close', {
          duration: 3000,
        });
        return;
      }
      else {
        this.loadingService.showLoading();
        setTimeout(() => {
          // Hide the loading overlay after the operation is complete
          this.loadingService.hideLoading();
        }, 20000);
        var name = nameInput.value;
        var email = emailInput.value;
        var phoneNumber = phoneNumberInput.value;
        var referral = referralInput.value;
        var institutename = institutenameInput.value;
      }
      const data = {
        customer_name: name,
        customer_email: email,
        customer_phone: phoneNumber,
        customer_type: studentType,
        college_name: institutename,
        verification_id: this.ImageBase64,
        referral: referral,
        event_id: this.eventdata[0].id,
        selected_sub_events: this.SubEventsSelected.map((subEvent: { id: any; given: any; }) => ({
          id: subEvent.id,
          given: subEvent.given // Include the 'given' property if it exists in subEvent
        })),
        selected_addons: this.AddonsSelected.map((addon: { id: any; }) => addon.id),
        coupon: this.appliedCoupon,
    }
    if (this.eventdata[0].payment_gateway == 'razorpay') {
    this.EventDetailsService.SendCheckoutData(data).then(() => {
      if(this.EventDetailsService.CheckoutData.message == 5545) {
        window.location.href = '/delivery-student';
      }
      else {
      const checkoutData = {
        "key_id": this.EventDetailsService.CheckoutData.id,
        "order_id": this.EventDetailsService.CheckoutData.payment_id,
        "amount": this.TotalPrice * 100,
        "name": this.EventDetailsService.CheckoutData.Business,
        "image": this.EventDetailsService.CheckoutData.image,
        "currency": this.EventDetailsService.CheckoutData.currency,
        "callback_url": this.EventDetailsService.CheckoutData.callback_url,
        "prefill[name]": name,
        "prefill[email]": email,
        "prefill[contact]": phoneNumber,
      };
      const form = this.createForm(checkoutData);
      this.submitFormElement(form);
    }
    });
  }
  else if (this.eventdata[0].payment_gateway == 'billdesk') {
    this.EventDetailsService.SendCheckoutData(data).then(() => {
      if(this.EventDetailsService.CheckoutData.message == 5545) {
        window.location.href = '/delivery-student';
      }
      else {
      const checkoutData = this.EventDetailsService.CheckoutData;
      const form = this.createForm(checkoutData);
      this.submitFormElement(form);
      }
    });
  }
}

dataURItoBlob(dataURI: string): Blob {
  const byteString = atob(dataURI.split(',')[1]);
  const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  return new Blob([ab], { type: mimeString });
}

blobToBase64(blob: Blob, callback: (arg0: any) => void) {
  const reader = new FileReader();
  reader.onload = () => {
    const result = reader.result;
    if (typeof result === 'string') {
      const base64String = result.split(',')[1];
      callback(base64String);
    } else {
      throw new Error('Unexpected result type');
    }
  };
  reader.readAsDataURL(blob);
}

  private createForm(formData: { [key: string]: any }): HTMLFormElement {
  if (this.eventdata[0].payment_gateway == 'razorpay') {
    const form = this.renderer.createElement('form');
    form.method = 'POST';
    form.action = 'https://api.razorpay.com/v1/checkout/embedded';
  
    Object.entries(formData).forEach(([name, value]) => {
      const input = this.renderer.createElement('input');
      this.renderer.setAttribute(input, 'type', 'hidden');
      this.renderer.setAttribute(input, 'name', name);
  
      if (typeof value === 'object') {
        this.renderer.setAttribute(input, 'value', JSON.stringify(value));
      } else {
        this.renderer.setAttribute(input, 'value', value.toString());
      }
  
      this.renderer.appendChild(form, input);
    });
    return form;
  }
    else {
      const form = this.renderer.createElement('form');
      form.method = 'POST';
      form.action = 'https://pgi.billdesk.com/pgidsk/PGIMerchantPayment';
      const inputMsg = this.renderer.createElement('input');
      inputMsg.type = 'hidden';
      inputMsg.name = 'msg';
      inputMsg.value = formData.toString();
      form.appendChild(inputMsg);
      return form;
    }
  }
  

  private submitFormElement(form: HTMLFormElement) {
    this.renderer.appendChild(this.elementRef.nativeElement, form);
    form.submit();
  }
    

}
