# Datastore Redirect

A tiny flask app to do v1 -> v2 datastore redirects. Based on [this excellent spreadsheet](https://docs.google.com/spreadsheets/d/19Qs6naJhoMIDpgbtNWr2Uab1mzzJge61_vfP4mEYCTs/edit) by [@markbrough](https://twitter.com/Mark_Brough).

## Test it out!

 * [https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?iati-identifier=44000-P090807](https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?iati-identifier=44000-P090807)
 * [https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?recipient-country=BD](https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?recipient-country=BD)
 * [https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?reporting-org=GB-GOV-1](https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?reporting-org=GB-GOV-1)
 * [https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?sector=11110](https://v1-iati-datastore.herokuapp.com/api/1/access/activity.xml?sector=11110)
 * …etc.

All the stuff in [the spreadsheet](https://docs.google.com/spreadsheets/d/19Qs6naJhoMIDpgbtNWr2Uab1mzzJge61_vfP4mEYCTs/edit) should work.

## Installation

```shell
$ pipenv install
$ pipenv run flask run
```
