=========================
Configuració del servidor
=========================

La configuració del servidor per tal d'executar el mòdul **ITBAMPA** consta dels
següents passos:

*  Crear una base de dades
*  Carregar mòduls requerits
*  Carregar mòdul **ITBAMPA**

Crear una base de dades
-----------------------

En un navegador, escriurem

:samp:`http://{url-servidor}:8069`

Si no hi cap base de dades creada, es mostrarà directament la pàgina per crear
una base de dades. En cas contrari, a la pàgina d'inici de sessió, seleccionarem
l'enllaç de gestió de bases de dades i en crearem una.

Carregar mòduls requerits
-------------------------

Un cop creada la base de dades, desactivarem el filtre d'aplicacions. Suggerim seguir aquest ordre per carregar els mòduls:

* ``Spanish Charts of Accounts (PGCE 2008)``, sense
  executar el *wizard* de configuració del módul. A la configuració
  de les plantilles de comptes, és recomenable canviar el tipus de compte associat
  al compte ``4482 Afiliados`` a ``Cobros``
* ``Accounting & Finance (account_accountant)`` i executarem el *wizard*
  per carregar el pla comptable per a associacions sense ànim de lucre.
* ``l10n_es_toponyms``. Tarda molt de temps.
* ``l10n_es_partner``. Importa els bancs espanyols.
* ``account_banking_sepa_direct_debit``, per girar rebuts SEPA.
* ``account_payment_partner``. Afegeix el camp **Mode de pagament** de client i proveïdor.

Després carregarem els mòduls que ens facin falta, com per exemple, els de
l'IVA, tancament d'exercicis fiscals, actius, pagaments SEPA, etc.
