from datetime import datetime, timedelta
from crispy_forms.layout import Submit

from lmgtfy.models import Domain, DomainSearch, TLD
from lmgtfy.tasks import search_bing_task


class CleanSubmitButton(Submit):
    field_classes = 'btn btn-default'


# def search_yahoo(domain):
#     domain_db_record, _created = Domain.objects.get_or_create(name=domain)
#     # currently we are do not allow to search the same domain more than once per day
#     recently_searched = DomainSearch.objects.filter(
#         created_at__gte=datetime.now()-timedelta(days=1),
#         domain=domain_db_record
#     ).count()
#     if recently_searched:
#         return False
#     else:
#         search_yahoo_task.apply_async(kwargs={'domain': domain})
#         return True


def search_bing(domain):
    domain_db_record, _created = Domain.objects.get_or_create(name=domain)
    # currently we are do not allow to search the same domain more than once per day
    recently_searched = DomainSearch.objects.filter(
        created_at__gte=datetime.now()-timedelta(days=1),
        domain=domain_db_record
    ).count()
    if recently_searched:
        return False
    else:
        search_bing_task.apply_async(kwargs={'domain': domain})
        return True


def check_valid_tld(domain):
    allowed_tlds = TLD.objects.all().values_list('name', flat=True)
    for tld in allowed_tlds:
        if domain.endswith(tld):
            return True
    return False
