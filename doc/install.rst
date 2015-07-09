Instal·lació i configuració de l'Odoo 8
=======================================

Per facilitar les coses, farem servir una màquina amb una instal·lació bàsica d'Ubuntu. La versió recomenada és la 14.04.

Per instal·lar l'ERP Odoo 8, farem servir el mètode *Packaged Installers* que s'explica al seu `web <https://www.odoo.com/documentation/8.0/setup/install.html#setup-install-packaged>`_:

.. code::

    wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
    echo "deb http://nightly.odoo.com/8.0/nightly/deb/ ./" >> /etc/apt/sources.list
    apt-get update && apt-get install odoo

Com explica el web de l'Odoo, cal instal·lar el paquet ``wkhtmltopdf``. Ho farem de la següent forma, sobretot si surten errors de dependències no satisfetes (suposarem que la versió és ``wkhtmltox-0.12.2.1_linux-trusty-amd64.deb``)::

    dpkg -i wkhtmltox-0.12.2.1_linux-trusty-amd64.deb
    sudo apt-get install -f

Aquest mètode *Packaged Installers* crea el rol ``odoo`` a PostgresQL sense contrasenya. És convenient, doncs, assignar-li una abans de continuar per tenir una mica més de seguretat::

    sudo su postgres
    psql
    alter role odoo with password='<contrasenya>'
    exit

Actualitzem la contrasenya al fitxer ``/etc/odoo/openerp-server.conf`` i reiniciem el servidor::

    sudo service odoo restart

Configuració dels *addons*
--------------------------

Crearem un directori, per exemple ``/home/odoo/addons``, on instal·larem els diferents mòduls necessaris per a **ITBAMPA**.

A l'Odoo, els mòduls *oficials* es gestionen a `Github <http://github.com>`_, per tant, si no el tenim instal·lat encara, ens farà falta el programa ``git``::

    sudo apt-get install git

Haurem de baixar els mòduls necessaris per a la comptabilitat espanyola i per a pagaments SEPA. En el directori ``/home/odoo/addons`` (o el que s'hagi triat):

partner-contact
    ``git clone -b 8.0 https://github.com/OCA/partner-contact``
    Mòduls dels quals depén la comptabilitat espanyola


account-financial-tools
    ``git clone -b 8.0 https://github.com/OCA/account-financial-tools``
    Mòduls dels quals depén la comptabilitat espanyola


reporting-engine
    ``git clone -b 8.0 https://github.com/OCA/reporting-engine``
    Mòduls dels quals depén la comptabilitat espanyola


bank-statement-import
    ``git clone -b 8.0 https://github.com/OCA/bank-statement-import``
    Mòduls dels quals depén la comptabilitat espanyola


bank-payment
    ``git clone -b 8.0 https://github.com/OCA/bank-payment``
    Mòduls dels quals depén la comptabilitat espanyola. Inclou la gestió de pagaments i fitxers SEPA.


l10n-spain
    ``git clone -b 8.0 https://github.com/OCA/l10n-spain``
    Mòdul que conté la comptabilitat espanyola


Per tal que el servidor detecti i carregui els mòduls, els haurem d'afegir al paràmetre ``addons-path`` del fitxer de configuració ``/etc/odoo/openerp-server.conf``::

    ...
    addons_path = /home/odoo/addons/partner-contact,
      /home/odoo/addons/account-financial-tools,
      /home/odoo/addons/reporting-engine,
      /home/odoo/addons/bank-statement-import,
      /home/odoo/addons/bank-payment,
      /home/odoo/addons/l10n-spain,
      /usr/lib/python2.7/dist-packages/openerp/addons
    ...

Reiniciarem el servidor per tal que els canvis tinguin efecte::

    sudo service odoo restart

Altres mòduls necessaris
------------------------

També són necessaris alguns mòduls dels quals depenen altres mòduls::

    sudo apt-get install python-unidecode
    sudo apt-get install python-unicodecsv
