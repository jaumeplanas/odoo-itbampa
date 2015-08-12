Mòdul ITB AMPA
==============

.. _membres:

Membres
-------

S'aprofita el model ``res.partner`` bàsic de l'Odoo per definir els membres que formen l'AMPA.

Els membres de l'AMPA es distingueixen de la resta de *partners* amb el camp ``ampa_partner_type``, que pot tenir **tres** valors possibles:

* *Cap valor*, per indicar que és un *partner* comercial que no forma part de l'AMPA.
* *Tutor*, són els pares i mares que formen l'AMPA.
* *Estudiant* o *alumne*, són els fills i filles dels *Tutors* que estudien a l'Escola.

Els *estudiants* tenen els següents camps necessaris:

* *Data de naixement*
* *Cursos de retard* o avançament. Juntament amb la *data de naixement*, permet saber quin curs estudia (primer, segon de primària, etc.). Un valor positiu vol dir repetidor; un valor negatiu vol dir que va avançat.
* *Tutor o partner a facturar*: és el *tutor* responsable de pagar les despeses generades per l'*estudiant*.
* *Tutors*: Llista de tutors responsables de cada *estudiant*. Normalment són el pare i la mare, però evidentment hi poden haver casos diferents.

  .. _currentcoursefield:
  
* *Curs actual*: És un camp només de lectura, calculat pel sistema. Vegeu :ref:`school-calendar`. 

Els *tutors* tenen els següents camps necessaris:

* A la pestanya de **Comptabilitat**, els camps necessaris per mantenir operacions comercials: *NIF*, *Compte Corrent*, etc.
* *Tutor o partner a facturar*: és el *tutor* responsable de pagar les despeses generades pel *tutor*. Normalment és el mateix *tutor*, però pot ser també el cònjuge, en segons quins casos.
* *Fills*: Llista dels *estudiants* o *alumnes* dels quals n'és responsable

.. _pestanyamenjador:

A la pestanya **Menjador** es defineix la informació corresponent al servei de menjador:

* *És suscrit al menjador?* Si es marca, aquest membre es seleccionarà automàticament en les llistes d'assistència al menjador. Vegeu :ref:`Menjador <suscritmenjador>`
* *Producte de menjador*: Producte que es seleccionarà per defecte quan s'inclogui aquest membre a la llista d'assistència al menjador. Vegeu també :ref:`Menjador <suscritmenjador>`
* *Menjador*: Llista d'assistències al menjador.

Juntes
------

En el menú ``Configuració -> Càrrecs de junta`` es defineixen els diferents càrrecs d'una junta: presidència, secretaria, tresoreria, vocalia, etc.

En el menú ``Gestió -> Juntes`` es defineixen les juntes:

* Les juntes poden estar obertes o tancades. Només pot haver-hi una junta oberta en cada moment.
* La data d'inici d'una junta no pot ser anterior a la data final de qualsevol altra junta.

.. _school-calendar:

Calendari escolar
-----------------

Els **Calendaris escolars** serveixen per definir les dates corresponents a cada curs escolar. La informació que recull és la següent:

* *Data d'inici*: Data en la qual comença el curs. És el primer dia lectiu del curs.
* *Data final*: Data en la qual finalitza el curs. És l'últim dia lectiu del curs.
* *Festius*: Llista d'intervals de dades que són festius. Per exemple, les vacances de nadal (del 20 de desembre al 7 de gener, per exemple; 
  tant el 20-12 com el 7 de gener són considetars festius). Una festa d'un dia de durada s'especifica emprant el mateix dia, per exemple, 
  de l'1 de maig a l'1 de maig.

Aquesta informació permet al programa saber quins dies són lectius en cada curs. Això facilita la gestió del menjador, ja que es pot considerar
que els dies que s'ofereix servei de menjador són els mateixos dies que són lectius.

El botó ``Calcula curs actual`` utilitza un Calendari escolar per calcular el :ref:`curs actual <currentcoursefield>` de cadascun dels membres *alumne*.

Menjador
--------

La gestió del **Menjador** es fa mitjançant llistes d'assistències al menjador. Quan es selecciona l'opció de Menjador, per defecte es mostra la vista de *calendari* 
amb el mes actual. Si algun dia té una llista definida, es mostra a la corresponent casella del dia.

Quan es selecciona un dia es mostra la llista d'assistència. Els camps d'aquesta fitxa són els següents:

* *Data*: Data de la fitxa.
* *Total registrats*: Camp calculat pel sistema, que indica el total de comensals.
* *Comensals*: Llista de comensals o persones que han utilitzat el servei de menjador aquest dia. Aquesta llista mostra la següent informació:

  * *Comensal* o *Assistent*
  * *Curs actual*: Camp informatiu només de lectura.
  * *Producte*: Producte que s'aplicarà quan es facturi aquest servei.
  * *Comentari*: Camp opcional per facilitar el seguiment del comportament del comensal.

.. _suscritmenjador:

Quan es selecciona un dia per primera vegada, la llista d'assistents s'omple amb tots els membres que tenen activada la casella *És suscrit al menjador?* 
a la :ref:`pestanya Menjador <pestanyamenjador>` de la fitxa :ref:`membres`.   

A la fitxa també es troben dos botons:

* *Assistència*: genera un llistat per facilitar el control d'assistència.
* *Actualitza membres*: Combina la llista actual amb la llista de preinscrits, per si s'han fet molts canvis. 
  Només afegeix els membres preinscrits que faltin, no esborra cap membre no preinscrit que ja sigui a la llista.

Cada llistat pot tenir tes estats, que es corresponen al flux de treball proposat:

* *Oberta*: La llista és oberta i admet modificacions, tant per afegir com per esborrar membres. Això permet crear llistes per dates posteriors a l'actual.
* *Tancada*: La llista és tancada i no es poden fer modificacions.

  Quan és el dia, per exemple a les 10 hores, la llista es **tanca** i s'imprimeix el llistat d'assistència que permet passar llista al menjador i introduir comentaris. 
  Quan s'acaba el menjador, s'**obre** la llista i s'introdueixen els comentaris. Si ha faltat algun assistent, senzillament s'esborra de la llista.
  Un cop fets els canvis, es torna a **tancar** la llista.

 * *Facturada*: Quan el procés de facturació creï una factura per a aquest servei, la llista es marcarà com a **facturada**. 
 
   .. note:: Només es poden facturar llistes d'assistència que estiguin tancades.
   