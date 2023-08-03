import { Component } from '@angular/core';
import { EventDetailsService } from '../../services/event-details/event-details.service';
import { HttpClient } from '@angular/common/http';
import { ElementRef, Renderer2 } from '@angular/core';
import { LoadingServiceComponent } from '../../loading-service/loading-service.component';

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

  constructor(
    private http: HttpClient,
    private EventDetailsService: EventDetailsService, private renderer: Renderer2, private elementRef: ElementRef, public loadingService: LoadingServiceComponent) { }

    ngOnInit() {
      this.EventDetailsService.EventDetails().then(() => {
        this.EventDetailsService.SubEventDetails().then(() => {
          this.EventDetailsService.AddonDetails().then(() => {
            this.eventdata = this.EventDetailsService.event;
            this.TotalPrice += parseFloat(this.eventdata[0].price);
            this.SubEvents = this.EventDetailsService.SubEvent;
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
      this.EventDetailsService.SendPromoCode(coupon).then(() => {
        if (this.EventDetailsService.PromoData.discount) {
          this.isDiscountApplied = true;
          this.DiscountValue = this.EventDetailsService.PromoData.discount;
          this.TotalPrice = this.TotalPrice - this.DiscountValue;
        }
    });
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
      this.loadingService.showLoading();
      setTimeout(() => {
        // Hide the loading overlay after the operation is complete
        this.loadingService.hideLoading();
      }, 20000);
      var nameInput = document.getElementById("name") as HTMLInputElement;
      var emailInput = document.getElementById("email") as HTMLInputElement;
      var phoneNumberInput = document.getElementById("phone") as HTMLInputElement;
      
      if(nameInput.value == '' || emailInput.value == '' || phoneNumberInput.value == '') {
        alert('Please fill all the fields');
        return;
      }
else {
        var name = nameInput.value;
        var email = emailInput.value;
        var phoneNumber = phoneNumberInput.value;
      }
      const data = {
        customer_name: name,
        customer_email: email,
        customer_phone: phoneNumber,
        event_id: this.eventdata[0].id,
        selected_sub_events: this.SubEventsSelected.map((subEvent: { id: any; }) => subEvent.id),
        selected_addons: this.AddonsSelected.map((addon: { id: any; }) => addon.id),
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
