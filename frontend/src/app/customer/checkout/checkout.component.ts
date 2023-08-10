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
  AddonsSelected: any = [];
  TotalPrice: number = 0;
  showCouponInput: boolean = false;
  couponCode: string = '';
  appliedCoupon: string = '';

  constructor(
    private http: HttpClient,
    private EventDetailsService: EventDetailsService, private renderer: Renderer2, 
    private elementRef: ElementRef, public loadingService: LoadingServiceComponent,
    private _snackBar: MatSnackBar) { }

    ngOnInit() {
      this.EventDetailsService.EventDetails().then(() => {
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

    toggleDescription(eventItem: any, event: Event) {
      event.preventDefault();
      eventItem.showDescription = !eventItem.showDescription;
    }

    toggleCouponInput() {
      this.showCouponInput = !this.showCouponInput;
    }

    applyCoupon(coupon: any) {
      if ( this.isDiscountApplied == false ) {
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
      if (event.checked) {
        this.SubEventsSelected.push(subEvent);
        if (this.SubEventsSelected.length > this.EventDetailsService.event[0].sub_events_included_allowed) {
        this.TotalPrice += parseFloat(subEvent.price);
        }
      } else {
        if (this.SubEventsSelected.length > this.EventDetailsService.event[0].sub_events_included_allowed) {
          this.TotalPrice -= parseFloat(subEvent.price);
          }
          this.SubEventsSelected.splice(this.SubEventsSelected.indexOf(subEvent), 1);
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
      }
      const data = {
        customer_name: name,
        customer_email: email,
        customer_phone: phoneNumber,
        referral: referral,
        event_id: this.eventdata[0].id,
        selected_sub_events: this.SubEventsSelected.map((subEvent: { id: any; }) => subEvent.id),
        selected_addons: this.AddonsSelected.map((addon: { id: any; }) => addon.id),
        coupon: this.appliedCoupon,
    }
    this.EventDetailsService.SendCheckoutData(data).then(() => {
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

    });
  }

  private createForm(formData: { [key: string]: any }): HTMLFormElement {
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
  

  private submitFormElement(form: HTMLFormElement) {
    this.renderer.appendChild(this.elementRef.nativeElement, form);
    form.submit();
  }
    

}
