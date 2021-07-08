# Datastore Redirects

A tiny flask app to do v2 -&gt; v1 datastore redirects. Based on original work by [@andylolz](https://twitter.com/andylolz).

## Why are redirects important?

Putting in place redirects for the IATI Datastore will reduce disruption for users. Wherever possible, users can continue to use the same API calls, getting back the same response, without having to make any changes on their end. Without redirects, all users will be forced to make changes, which may involve having to go back to vendors to request changes to the source code.

## Test it out!

Below are examples of requests equivalent in format to those made to the [V2 Datastore](https://iatidatastore.iatistandard.org/). The requests are reshaped and redirected to the [Datastore Classic](https://datastore.codeforiati.org/).


### Django endpoints

 * [/api/activities/?iati_identifier=44000-P090807&format=xml](/api/activities/?iati_identifier=44000-P090807&format=xml)
 * [/api/activities/?recipient_country=BD&format=xml](/api/activities/?recipient_country=BD&format=xml)
 * [/api/activities/?reporting_organisation_identifier=GB-GOV-1&format=xml](/api/activities/?reporting_organisation_identifier=GB-GOV-1&format=xml)
 * [/api/activities/?sector=11110&format=xml](/api/activities/?sector=11110&format=xml)
 * …etc.

### SOLR endpoints

 * <a href="/search/activity/?q=reporting_org_ref:GB-GOV-1 AND (recipient_country_code:SO OR transaction_recipient_country_code:SO)&wt=xslt&tr=activity-xml.xsl&rows=1">/search/activity/?q=reporting_org_ref:GB-GOV-1 AND (recipient_country_code:SO OR transaction_recipient_country_code:SO)&wt=xslt&tr=activity-xml.xsl&rows=1</a>
 * <a href="/search/activity/?q=(reporting_org_ref:US-GOV-1 AND recipient_country_code:BD)&wt=xslt&tr=activity-xml.xsl&rows=1">/search/activity/?q=(reporting_org_ref:US-GOV-1 AND recipient_country_code:BD)&wt=xslt&tr=activity-xml.xsl&rows=1</a>
 * <a href="/search/activity/?q=iati_identifier:46002-P-LR-A00-003&wt=xslt&tr=activity-xml.xsl&rows=1">/search/activity/?q=iati_identifier:46002-P-LR-A00-003&wt=xslt&tr=activity-xml.xsl&rows=1</a>
 * …etc.


## Installation

```shell
$ git clone https://github.com/codeforiati/datastore-redirects.git
$ cd datastore-redirects
$ pipenv install
```

## Running

```shell
$ pipenv run flask run
```
