from urllib.parse import parse_qs

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cms.models import Subscriber

from .views import notify_subscriber_on_signup


@require_POST
@csrf_exempt
def sync_mailchimp_subscribers(request):
    """
    When the audience list is adjusted via mailchimp site this view will
    receive the webhook and update the database accordingly.
    One webhook is sent per subscription/ unsubscription.
    """

    raw_response = request.body
    response = parse_qs(raw_response.decode('UTF-8'))
    req_type = response['type'][0]

    if req_type == "subscribe":
        fname_key = 'data[merges][FNAME]'
        lname_key = 'data[merges][LNAME]'
        email_key = 'data[email]'
        phone_key = 'data[merges][PHONE]'

        name, email, number = '', '', ''

        if fname_key in response:
            name = response[fname_key][0]

        if lname_key in response:
            name += " " + response[lname_key][0]

        if email_key in response:
            email = response[email_key][0]

        if phone_key in response:
            number = response[phone_key][0]

        sub_to_add = Subscriber.objects.create(name=name, email=email,
                                               number=number)
        sub_to_add.save()
        notify_subscriber_on_signup(request, sub_to_add)

    elif req_type == "unsubscribe":
        sub_email = response['data[email]'][0]
        try:
            sub_to_del = Subscriber.objects.get(email=sub_email)
            sub_to_del.delete()
        except ObjectDoesNotExist:
            print("Subscriber with that email doesn't exist within database.")
        except Exception:
            print("Unable to delete subscriber.")

    return HttpResponse('Hello, world. This is the webhook response.')
