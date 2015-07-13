Mòdul ITB AMPA
==============

Membres
-------

S'aprofita el model ``res.partner`` bàsic de l'Odoo per definir els membres que formen l'AMPA.

Els membres de l'AMPA es distingueixen de la resta de *partners* amb el camp ``ampa_partner_type``, que pot tenir **tres** valors possibles:

* *Cap valor*, per indicar que és un *partner* comercial que no forma part de l'AMPA.
* *Tutor*, són els pares i mares que formen l'AMPA.
* *Estudiant* o *alumne*, són els fills i filles dels *Tutors* que estudien a l'Escola.

Els *estudiants* ténen els següents camps necessaris:

* *Data de naixement*
* *Cursos de retard* o avançament. Juntament amb la *data de naixement*, permet saber quin curs estudia (primer, segon de primària, etc.). Un valor positiu vol dir repetidor; un valor negatiu vol dir que va avançat.
* *Tutor o partner a facturar*: és el *tutor* responsable de pagar les despeses generades per l'*estudiant*.
* *Tutors*: Llista de tutors responsables de cada *estudiant*. Normalment són el pare i la mare, però evidentment hi poden haver casos diferents.

Els *tutors* ténen els següents camps necessaris:

* A la pestanya de **Comptabilitat**, els camps necessaris per mantenir operacions comercials: *NIF*, *Compte Corrent*, etc.

* *Fills*: Llista dels *estudiants* o *alumnes* dels quals n'és responsable

Juntes
------

En el menú ``Configuració -> Càrrecs de junta`` es defineixen els diferents càrrecs d'una junta: presidència, secretaria, tresoreria, vocalia, etc.

En el menú ``Gestió -> Juntes`` es defineixen les juntes:

* Les juntes poden estar obertes o tancades. Només pot haver-hi una junta oberta en cada moment.
* La data d'inici d'una junta no pot ser anterior a la data final de qualsevol altra junta.
