NZB - Parser
============

Parsing NZB

=========
Beispiel:
=========

.. code-block:: python

   from LordNzb import parser
   nzb = parser(pfad)
   print(n.to_dict())

Die Variable 'nzb' bitte nur als Read-Only verwenden


Ausgabe:
********

.. code-block:: json

    {
      "filename": "Sample.Name{{sample_password}}.nzb",
      "name": "Sample.Name",
      "header": "sample_header",
      "password": "sample_passw",
      "group": [
        "group-1",
        "group-2",
        "group-3"
      ],
      "size": "1.00 gb",
      "date": "YYYY-MM-DD HH:MM:SS",
      "nzbindex": "https://nzbindex.nl/?q=sample_header",
      "nzbking": "https://nzbking.com/?q=sample_header",
      "binsearch": "https://binsearch.info/?q=sample_header",
      "nzblnk": "nzblnk://?t=Sample.Name&h=sample_header&p=sample_passw&g=group-1"
    }


*by LordBex*

