datatable-faker
================

    Library to generate fake datatable for unittest 

.. image:: https://img.shields.io/pypi/v/datatable-faker
   :target: https://pypi.python.org/pypi/datatable-faker/

.. image:: https://github.com/Agent-Hellboy/datatable-faker/actions/workflows/python-publish.yml/badge.svg
    :target: https://github.com/Agent-Hellboy/datatable-faker/

.. image:: https://img.shields.io/pypi/pyversions/datatable-faker.svg
   :target: https://pypi.python.org/pypi/datatable-faker/

.. image:: https://img.shields.io/pypi/l/datatable-faker.svg
   :target: https://pypi.python.org/pypi/datatable-faker/

.. image:: https://pepy.tech/badge/datatable-faker
   :target: https://pepy.tech/project/datatable-faker

.. image:: https://img.shields.io/pypi/format/datatable-faker.svg
   :target: https://pypi.python.org/pypi/datatable-faker/


Installation
============

::

   for stable version
      - pip install datatable-faker

   for developement
      - git clone https://github.com/Agent-Hellboy/datatable-faker
      - cd datatable-faker
      - python -m venv .venv
      - source .venv/bin/activate
      

Example
-------



.. code:: py
    from dataclasses import dataclass

    @dataclass()
    class Heartbeat:
        serialNumber: str
        cbsdId: str
        grantId: str
        grantState: str
        carrier: int
        maxEirp: int

    from datatable_faker import generate_fake_data

    fake_data = generate_fake_data(Heartbeat)
    print(fake_data)

::

    Heartbeat(serialNumber='economic', cbsdId='pull', grantId='save', grantState='same', carrier=729, maxEirp=1792)

Contributing
============

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
