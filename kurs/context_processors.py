from market.forms import SearchAllForm


def search_form(request):
    return {
         'search_all_form' : SearchAllForm()
    }
