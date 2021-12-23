from django.forms.widgets import Input
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader


from django.contrib.auth.decorators import login_required

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.mail import send_mail



from . import forms


# Create your views here.
@login_required(login_url="/accounts/login/")
def homepage(request):
    return render(request, 'main/homepage.html')


@login_required(login_url="/accounts/login/")
def bus_details(request, slug):
    # return HttpResponse(slug)
    return render(request, 'main/bus_details.html')


@login_required(login_url="/accounts/login/")
def about(request):
    # return HttpResponse("About")
    return render(request, 'main/about.html')


@login_required(login_url="/account/login/")
def contact(request):
    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_phone = request.POST['message-phone']
        message = request.POST['message-message']

        #send email
        send_mail(
            'Mail Sent By '+message_name , # subject
            '\n'+'Senders Phone: '+message_phone + '\nSenders Email: '+message_email+ ' \nMessage: ' + message, #message
            message_email, #from mail
            ['rashikbuksh71@gmail.com'], #tomail
        )
        return render(request, 'main/contact.html', {'message_name': message_name})
    else:
        return render(request, 'main/contact.html')


@login_required(login_url="/account/login/")
def ticket_page(request):
    return render(request, 'main/ticket_page.html')


@login_required(login_url="/account/login/")
def ticket_page(request):
    ticket_page.message_name = request.POST.get('message-name')
    ticket_page.message_email = request.POST.get('message-email')
    ticket_page.message_phone = request.POST.get('message-phone')
    ticket_page.message_start = request.POST.get('message-start')
    ticket_page.message_end = request.POST.get('message-end')
    ticket_page.message_date = request.POST.get('message-date')
    ticket_page.message_bus = request.POST.get('message-bus')
    ticket_page.text = request.POST.get('message-text')

    return render(request, 'main/ticket_page.html', {'message_name': ticket_page.message_name})


@login_required(login_url="/account/login/")
def ticket(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    name = ticket_page.message_name
    mail = ticket_page.message_email
    phone = ticket_page.message_phone
    start = ticket_page.message_start
    end = ticket_page.message_end
    date = ticket_page.message_date
    bus = ticket_page.message_bus
    text = ticket_page.text
    # print(text)

    lines = [
        "Welcome to optimal transportation system",
        " ",
        "Your ticket is below",
        " ",
        "Full name: " + name,
        " ",
        "Email: " + mail,
        " ",
        "Phone: "+phone,
        " ",
        "Pickup place: "+start,
        " ",
        "Destination: "+end,
        " ",
        "Journey Date: "+date,
        " ",
        "Bus: "+bus,
        " ",
        ""+text,
        "",
        "All right reserved by optimal transportation system",

    ]

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="ticket.pdf")


@login_required(login_url="/account/login/")
def bolakareview(request):
    form = forms.balakareview()
    if request.method == 'POST':
        form = forms.balakareview(request.POST)
        if form.is_valid():
            # save to db
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # instance = balaka.objects.get(id=id)
            # instance.delete()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    else:
        form = forms.balakareview()
    return render(request, 'main/balakareview.html', {'form': form})


@login_required(login_url="/account/login/")
def culturalfood(request):
    return render(request, 'main/culturalfood.html')

