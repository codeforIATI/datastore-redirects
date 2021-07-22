import os
import pytest
import app


@pytest.fixture
def client():
    app.application.config['TESTING'] = True

    with app.application.test_client() as client:
        yield client


def test_routes_work(client):
    working_routes = [
        '/api/activities/?iati_identifier=44000-P090807&format=xml',
        '/api/activities/?recipient_country=BD&format=xml',
        '/api/activities/?reporting_organisation_identifier=GB-GOV-1&format=xml',
        '/api/activities/?sector=11110&format=xml'
    ]
    for route in working_routes:
        r = client.get(route)
        assert r.status_code == 302


def test_solr_routes_work(client):
    working_routes = [
        '/search/activity/?q=reporting_org_ref:GB-GOV-1 AND (recipient_country_code:SO OR transaction_recipient_country_code:SO)&wt=xslt&tr=activity-xml.xsl&rows=1',
        '/search/activity/?q=(reporting_org_ref:US-GOV-1 AND recipient_country_code:BD)&wt=xslt&tr=activity-xml.xsl&rows=1',
        '/search/activity/?q=iati_identifier:46002-P-LR-A00-003&wt=xslt&tr=activity-xml.xsl&rows=1',
    ]
    for route in working_routes:
        r = client.get(route)
        assert r.status_code == 302


def test_routes_dont_work(client):
    not_working_routes = [
        '/search/activity/?q=recipient_country_code:SO OR sector_code:11110&wt=xslt&tr=activity-xml.xsl&rows=1',
        '/search/activity/?q=recipient_country_code:SO&rows=1',
    ]
    for route in not_working_routes:
        r = client.get(route)
        assert r.status_code == 400
