from contextlib import closing

from bokeh.client import push_session, pull_session
from bokeh.document import Document
from bokeh.embed import autoload_server

from .viz.individuals import update_individuals_data
from .viz.team import update_team_data
from .viz.teams import update_teams_data


def get_bokeh_script(user, plot, suffix):
    from .models import UserSession

    document = Document()
    document.add_root(plot)
    document.title = suffix

    with closing(push_session(document)) as session:
        # Save the session id to a UserSession
        UserSession.objects.create(user=user, bokeh_session_id=session.id)
        # Get the script to pass into the template
        script = autoload_server(None, session_id=session.id)

    return script


def update_bokeh_sessions(user_sessions):
    for us in user_sessions:
        with closing(pull_session(session_id=us.bokeh_session_id)) as session:
            if len(session.document.roots) == 0:
                # In this case, the session_id was from a dead session and
                # calling pull_session caused a new empty session to be
                # created. So we just delete the UserSession and move on.
                # It would be nice if there was a more efficient way - where I
                # could just ask bokeh if session x is a session.
                us.delete()
            else:
                # Call the appropriate update method based on the document's title
                if session.document.title == 'individuals':
                    update_individuals_data(user=us.user, session=session)
                if session.document.title == 'team':
                    update_team_data(user=us.user, session=session)
                if session.document.title == 'teams':
                    update_teams_data(user=us.user, session=session)
