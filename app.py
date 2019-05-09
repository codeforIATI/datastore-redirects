from urllib.parse import urlencode

from flask import Flask, request, redirect


application = Flask(__name__)


@application.route('/api/1/access/activity.xml')
def activity():
    '''
    Returns a redirect to the v2 (new) datastore.

    Request params are mapped onto OIPA filters.
    '''

    # Current location of v2 (new) datastore
    base_url = 'https://store.staging.iati.cloud/api/activities/?'

    # We collect redirect request params here
    filters = {
        'format': 'xml',
    }

    # From: https://docs.google.com/spreadsheets/d/19Qs6naJhoMIDpgbtNWr2Uab1mzzJge61_vfP4mEYCTs/edit
    known_filters = {
        'iati-identifier': 'iati_identifier',
        'recipient-country': 'recipient_country',
        'recipient-region': 'recipient_region',
        'reporting-org': 'reporting_organisation_identifier',
        'reporting-org.type': None,
        'sector': 'sector',
        'policy-marker': None,
        'participating-org': 'participating_organisation',
        'participating-org.role': None,
        'related-activity': 'related_activity_id',
        'transaction': None,
        'transaction_provider-org': 'transaction_provider_organisation',
        'transaction_provider-org.provider-activity-id':
            'transaction_provider_activity',
        'transaction_receiver-org': 'transaction_receiver_organisation',
        'transaction_receiver-org.receiver-activity-id':
            'transaction_receiver_activity',
        'start-date__lt': 'actual_start_date_lte',
        'start-date__gt': 'actual_start_date_gte',
        'end-date__lt': 'actual_end_date_lte',
        'end-date__gt': 'actual_end_date_gte',
        'last-change__lt': None,
        'last-change__gt': None,
        'last-updated-datetime__lt': None,
        'last-updated-datetime__gt': None,
        'registry-dataset': None,
    }

    # Check if any unexpected URL params have been used ...
    unknown_filters = [x for x in request.args.keys()
                       if x not in known_filters.keys()]
    if unknown_filters != []:
        # ... if so, error
        return 'Unknown filter(s): ' + ', '.join(unknown_filters), 400

    # Build the redirect request params
    for old_filter, value in request.args.items():
        new_filter = known_filters[old_filter]
        if new_filter is None:
            # Some mappings are not yet known.
            # If any of these are used, error.
            return 'Unknown mapping for: ' + old_filter, 400
        # v2 (new) datastore uses `,` as a separator
        # for lists of values, whereas
        # v1 (old) datastore used `|`
        filters[new_filter] = value.replace('|', ',')

    # Return the redirect
    return redirect(base_url + urlencode(filters))


@application.route('/')
def home():
    '''
    Serve the homepage.

    Very simple - just read and return the contents of index.html
    '''
    with open('index.html') as handler:
        html = handler.read()
    return html
