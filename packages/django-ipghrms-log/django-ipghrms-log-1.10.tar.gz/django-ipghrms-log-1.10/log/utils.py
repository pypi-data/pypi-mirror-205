from django.utils import timezone
from .models import Log

from settings_app.utils import getnewid
from ipware import get_client_ip


def log_action(request, model, action, field_id ):

    # work: WORK ON HERE
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None :
        client_ip = "0.0.0.0"
    else:
        if is_routable:
            ipv = "Public"
        else:
            ipv = "Private"

    try:
        country = 'Unknown'
        lat = 'Unknown'
        lon = 'Unknown'
        city = 'Unknown'
    except:
        country = 'Unknown'
        city = 'Unknown'
        lat = None
        lon = None

    new_client_ip_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')    
    newid, new_hashid = getnewid(Log)
    Log.objects.create(
        pk = newid,
        username=request.user,
        ip_address=new_client_ip_address,
        is_private=is_routable,
        priv_address = client_ip,
        model=model,
        action=action,
        field_id=field_id,
        timestamp=timezone.now(),
        hashed=new_hashid
    )
