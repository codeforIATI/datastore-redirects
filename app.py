from urllib.parse import urlencode
from luqum.parser import parser
import luqum
from flask import Flask, request, redirect, render_template, abort


application = Flask(__name__)


@application.route('/search/activity/')
@application.route('/search/activity')
def activity_search():
    '''
    Returns a redirect to the v2 (new) datastore.

    Request params are mapped onto OIPA filters.
    '''

    test = False

    request_args = dict([(k, v) for (k, v) in request.args.items()])

    # Current location of v2 (new) datastore
    base_url = 'https://datastore.codeforiati.org/api/1/access/activity.xml?unwrap=True&'

    # We collect redirect request params here
    if (request_args.get('wt') != 'xslt') and (request_args.get('tr') != 'activity'):
        could_not_redirect('Datastore Classic is only able to serve IATI XML requests, as the format of JSON and CSV outputs differ from Datastore v2.')

    if request_args.get('test') is not None:
        test = True
        del request_args['test']

    filters = {}

    def fix_group(tree):
        if (type(tree) in (luqum.tree.Group, luqum.tree.FieldGroup)) and (len(tree.children) == 1):
            tree = tree.children[0]
        return tree

    def fix_name(name):
        # DS Classic automatically searches on activities and transactions
        # for sectors and recipient countries
        fixed = name.replace("transaction_", "")
        if fixed in ["sector", "recipient_country_code"]:
            return fixed
        return name

    def get_from_or(tree, filters):
        seen_fields = []
        for child in tree.children:
            if type(child) == luqum.tree.SearchField:
                fixed_name = fix_name(child.name)
                if (len(seen_fields) > 0):
                    if fixed_name not in seen_fields:
                        return abort(400, "Not implemented: ORs with different fields")
                expr = fix_group(child.expr)
                if fixed_name not in filters:
                    filters[fixed_name] = expr.value
                else:
                    if expr.value not in filters[fixed_name]:
                        filters[fixed_name] += '|' + expr.value
                seen_fields.append(fixed_name)
        return filters

    def get_from_and(tree, filters):
        for child in tree.children:
            if type(child) == luqum.tree.SearchField:
                filters[child.name] = child.expr.value
            else:
                if (type(child) == luqum.tree.Group) and (len(child.children) == 1):
                    child = child.children[0]
                if type(child) == luqum.tree.OrOperation:
                    filters = get_from_or(child, filters)
        return filters

    def parse_expression(expr):
        filters = {}
        tree = parser.parse(expr)
        tree = fix_group(tree)
        if type(tree) == luqum.tree.OrOperation:
            filters = get_from_or(tree, filters)
        elif type(tree) == luqum.tree.AndOperation:
            filters = get_from_and(tree, filters)
        elif type(tree) == luqum.tree.SearchField:
            expr = fix_group(tree.expr)
            filters[tree.name] = expr.value
        return filters

    # From: https://docs.google.com/spreadsheets/d/19Qs6naJhoMIDpgbtNWr2Uab1mzzJge61_vfP4mEYCTs/edit

    solr_request_args = parse_expression(request_args.get('q'))

    mappings = {
        'iati_identifier': 'iati-identifier',
        'recipient_country_code': 'recipient-country',
        'recipient_region_code': 'recipient-region',
        'reporting_org_ref': 'reporting-org',
        'sector': 'sector'
    }

    # Check if any unexpected URL params have been used ...
    unknown_filters = [x for x in solr_request_args.keys()
                       if x not in mappings.keys()]
    if unknown_filters != []:
        # ... if so, error
        return could_not_redirect('Unknown filter(s): {}'.format(
            ', '.join(unknown_filters)))

    # Check if any of the undefined mappings have been used ...
    undefined_mappings = [x for x in solr_request_args.keys()
                          if not mappings.get(x)]
    if undefined_mappings != []:
        # ... if so, error
        return could_not_redirect('Mapping to new filter(s) not known: {}'.format(
            ', '.join(undefined_mappings)))

    # Build the redirect request params
    for old_filter, value in solr_request_args.items():
        new_filter = mappings[old_filter]
        # v2 (new) datastore uses `,` as a separator
        # for lists of values, whereas
        # v1 (old) datastore used `|`
        filters[new_filter] = value.replace(',', '|')

    rows = request_args.get('rows', 1)
    if (int(rows) > 1000):
        filters['stream'] = 'True'
    else:
        filters['limit'] = rows

    # Return the redirect

    if test:
        return base_url + urlencode(filters)
    return redirect(base_url + urlencode(filters))

@application.route('/api/activities/')
@application.route('/api/activities')
def activity():
    test = False
    '''
    Returns a redirect to the v2 (new) datastore.

    Request params are mapped onto OIPA filters.
    '''

    request_args = dict([(k, v) for (k, v) in request.args.items()])

    # Current location of v2 (new) datastore
    base_url = 'https://datastore.codeforiati.org/api/1/access/activity.xml?unwrap=True&'

    # We collect redirect request params here
    if request_args.get('format') != 'xml':
        return could_not_redirect('Datastore Classic is only able to serve XML requests, as the format of JSON and CSV outputs differ from Datastore v2.')
    del request_args['format']

    if request_args.get('test') is not None:
        test = True
        del request_args['test']

    filters = {}

    # From: https://docs.google.com/spreadsheets/d/19Qs6naJhoMIDpgbtNWr2Uab1mzzJge61_vfP4mEYCTs/edit
    mappings = {
        'iati_identifier': 'iati-identifier',
        'recipient_country': 'recipient-country',
        'recipient_region': 'recipient-region',
        'reporting_organisation_identifier': 'reporting-org',
        'sector': 'sector',
        'participating_organisation': 'participating-org',
        'related_activity_id': 'related-activity',
        'transaction_provider_organisation': 'transaction_provider-org',
        'transaction_provider_activity': 'transaction_provider-org.provider-activity-id',
        'transaction_receiver_organisation': 'transaction_receiver-org',
        'transaction_receiver_activity': 'transaction_receiver-org.receiver-activity-id',
        'actual_start_date_lte': 'start-date__lt',
        'actual_start_date_gte': 'start-date__gt',
        'actual_end_date_lte': 'end-date__lt',
        'actual_end_date_gte': 'end-date__gt',
        'rows': 'limit'
    }

    # Check if any unexpected URL params have been used ...
    unknown_filters = [x for x in request_args.keys()
                       if x not in mappings.keys()]
    if unknown_filters != []:
        # ... if so, error
        return could_not_redirect('Unknown filter(s): {}'.format(
            ', '.join(unknown_filters)))

    # Check if any of the undefined mappings have been used ...
    undefined_mappings = [x for x in request_args.keys()
                          if not mappings.get(x)]
    if undefined_mappings != []:
        # ... if so, error
        return could_not_redirect('Mapping to new filter(s) not known: {}'.format(
            ', '.join(undefined_mappings)))

    # Build the redirect request params
    for old_filter, value in request_args.items():
        new_filter = mappings[old_filter]
        # v2 (new) datastore uses `,` as a separator
        # for lists of values, whereas
        # v1 (old) datastore used `|`
        if (new_filter == 'limit') and (int(value) > 1000):
            filters['stream'] = 'True'
        else:
            filters[new_filter] = value.replace(',', '|')

    # Return the redirect
    if test:
        return base_url + urlencode(filters)
    return redirect(base_url + urlencode(filters))


def could_not_redirect(message):
    return abort(400, message)


@application.errorhandler(400)
def error_400(error):
    return render_template('could_not_redirect.html', error=error), 400


@application.errorhandler(404)
def error_404(error):
    return render_template(
        'could_not_redirect.html',
        error={'description': "Redirects have not been implemented for that route."}), 404


@application.route('/')
def home():
    '''
    Serve the homepage.

    Very simple - just read and return the contents of index.html
    '''
    with open('index.html') as handler:
        html = handler.read()
    return html
