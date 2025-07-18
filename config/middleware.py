from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect



class AutoLogoutMiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activiy')
            if last_activity is not None:
                difference_time = (now()-now().fromisoformat(last_activity)).total_seconds()
                if difference_time > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return redirect('shop:product')
            
            request.session['last_activity'] = now().isoformat()

        response = self.get_response(request)
        return response
