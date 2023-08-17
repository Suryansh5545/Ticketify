# Ticketify

[![build](https://github.com/Suryansh5545/Ticketify/actions/workflows/django.yml/badge.svg)](https://github.com/Suryansh5545/Ticketify/actions/workflows/django.yml)

A System Made to Sell Event Tickets

# For whom is this system build?
This is build for the purpose of being a checkout page for events which doesn't have there own dedicated checkout page.

# Where did the idea came from to create this?
The idea to create this came from the fact that many fest/events hosted by colleges speically uses manual methods like asking customers to fill a google form and then using excel for check in purposes. This method is very ineffective and require significant manpower. I was a part of this ineffective system last year when my college did the similar thing and put up a google form for ticket selling, with qr code of a upi account put up as a image to scan then give the transaction id.


# What features does this system have?
1. Ticket Generation with QR Code Support
2. QR Scanning using WebCam from Admin panel
3. Integration with Payment Gateways like Razorpay, Phonepe(Under Development)
4. Sub Events support (If a fest have its own internal event which require another fee)
5. Addon Items Support (Anything that is limited in stock and doesn't fit the category of Sub Events)
6. Admin Page with Stats for Ticket Sale, Sub Event Sale, Addon and Total Check IN.
7. Android APP for QR Scanning (A Anroid app will be far more faster and better at this then a webcam)(Under Development).
8. Celery worker support to handle heavy task of ticket image generation.
9. Webhooks to detect initation of Dispute or refund and disable the ticket or payment captured in case of late capture. This will mark the ticket paid and send a email to customer.(Razorpay Only for now)
10. Constnat Evaluation of all ticket sold for the active event to check for there payment status. Which will make sure that all scenerios are covered of transaction failure or late success. (Razorpay Only for now)

# Is the system stable and tested for commercial use?
As of now the System is not finished for a live production usage, i will update as soon as we can declare it stable.
I am currently in process of getting a staging environment up for testing and a production environment for our upcoming Live Test run, with Sabrang 2023 at JKLU University.

# Installation
Setting up Ticketify on your local machine is really easy. You can setup Ticketify using docker: The steps are:
1. install [docker](https://docs.docker.com/install/) on your machine.

2. Get the source code on to your machine via git.

    ```shell
    git clone https://github.com/Suryansh5545/Ticketify.git ticketify && cd ticketify
    ```

3. Build and run the Docker containers. This might take a while.

    ```
    docker compose up --build
    ```
4. To Test Email support or Razorpay integration edit the docker.env.example file and rename the new one to docker.env
5. That's it. Open web browser and hit the URL [http://127.0.0.1:4200](http://127.0.0.1:4200). One user is created by default which are listed below -

    **SUPERUSER-** username: `admin` password: `password`

If you are facing any issue during installation, please feel free to reach out to me by mail [suryanshpathak5545@gmail.com](mailto:suryanshpathak5545@gmail.com)

# Planned Updates
1. Addition of more payment gateways Paytm and Phonepe(Under Development).
2. Android APP (Under Development).
3. Test Cases for most of the critical functions.
4. Addition of a organizer user to be able to add event without admin help from frontend.
5. Ability to host mutliple concurrently active events on the same site.

# Screenshot (Early Development Phase)
![image](https://github.com/Suryansh5545/Ticketify/assets/34577232/1874be8f-f40d-4038-abc4-479b9cbd53b9)
![image](https://github.com/Suryansh5545/Ticketify/assets/34577232/62f31e56-ebfe-41b3-9cba-54f108022571)
![image](https://github.com/Suryansh5545/Ticketify/assets/34577232/631b3526-236a-4aff-bceb-0f7868f383d8)
![image](https://github.com/Suryansh5545/Ticketify/assets/34577232/9bb1fc2d-e409-401a-88c1-8f22e3e1b6be)
![image](https://github.com/Suryansh5545/Ticketify/assets/34577232/6f20f547-0a2a-4f52-a20b-af1c35f439de)








