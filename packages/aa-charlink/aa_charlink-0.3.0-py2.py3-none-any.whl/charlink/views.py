from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from allianceauth.services.hooks import get_extension_logger
from allianceauth.eveonline.models import EveCharacter

from .forms import LinkForm
from .app_imports import import_apps
from .decorators import charlink
from .app_settings import CHARLINK_IGNORE_APPS

logger = get_extension_logger(__name__)


@login_required
def index(request):
    imported_apps = import_apps()

    if request.method == 'POST':
        form = LinkForm(request.user, request.POST)
        if form.is_valid():

            scopes = set()
            selected_apps = []

            for app, to_import in form.cleaned_data.items():
                if to_import:
                    scopes.update(imported_apps[app].get('scopes', []))
                    selected_apps.append(app)

            logger.debug(f"Scopes: {scopes}")

            request.session['charlink'] = {
                'scopes': list(scopes),
                'apps': selected_apps,
            }

            return redirect('charlink:login')

    else:
        form = LinkForm(request.user)

    characters = EveCharacter.objects.filter(character_ownership__user=request.user)

    characters_added = {
        'apps': [data['field_label'] for app, data in imported_apps.items() if app not in CHARLINK_IGNORE_APPS and request.user.has_perms(data['permissions'])],
        'characters': {},
    }

    # for app, data in imported_apps.items():
    #     if app not in CHARLINK_IGNORE_APPS and request.user.has_perms(data['permissions']):
    #         for character in characters:
    #             setattr(character, f'has_{app}', data['has_character'](character))

    for character in characters:
        characters_added['characters'][character.character_name] = []
        for app, data in imported_apps.items():
            if app not in CHARLINK_IGNORE_APPS and request.user.has_perms(data['permissions']):
                characters_added['characters'][character.character_name].append(
                    data['is_character_added'](character)
                )

    context = {
        'form': form,
        'apps': [data for app, data in imported_apps.items() if app not in CHARLINK_IGNORE_APPS and request.user.has_perms(data['permissions'])],
        'characters_added': characters_added,
    }

    return render(request, 'charlink/charlink.html', context=context)


@login_required
@charlink
def login_view(request, token):
    imported_apps = import_apps()

    charlink_data = request.session.pop('charlink')

    for app in charlink_data['apps']:
        if app != 'add_character' and app not in CHARLINK_IGNORE_APPS and request.user.has_perms(imported_apps[app]['permissions']):
            try:
                imported_apps[app]['add_character'](request, token)
            except Exception as e:
                logger.exception(e)
                messages.error(request, f"Failed to add character to {imported_apps[app]['field_label']}")
            else:
                messages.success(request, f"Character successfully added to {imported_apps[app]['field_label']}")

    return redirect('charlink:index')
