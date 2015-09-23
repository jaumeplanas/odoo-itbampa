==========
Activitats
==========

La gestió de les **Activitats** es fa mitjançant llistes d'assistències. Es poden definir diferents tipus d'activitats,
com per exemple, l'activitat de *Menjador* o *Acolliment del matí*, etc.

Tipus d'activitats
******************

Un Tipus d'activitat defineix una llista de **Membres** suscrits per defecte i un **Producte AMPA** associat. La definició de tipus d'activitats es troba al
menú ``Configuració -> Tipus d'activitats``.

A la fitxa de cada tipus d'activitat hi han els camps següents:

* **Tipus d'activitat**: el nom que volguem donar-li al tipus d'activitat.
* **Producte per defecte**: és el producte que es farà servir per defecte quan es generin factures de les activitats d'aquest tipus d'activitat.
  Només es poden seleccionar productes que siguin del tipus **Producte AMPA**. Vegeu `Productes <products.html>`_.
* **Membres suscrits**: Llista dels membres suscrits a aquest tipus d'activitat. cada membre té associat un producte (per defecte, el producte per defecte anterior)
  i un *Membre a facturar*, que és a qui s'enviaran les factures o rebuts.

El botó ``Selecció ràpida`` permet seleccionar grups de membres segons diferents criteris, per exemple, tots els de 2on de Primària, etc.

Activitats AMPA
***************

Quan es selecciona ``Gestió -> Activitats AMPA``, per defecte es mostra la vista de *calendari* 
amb el mes actual. Si algun dia té una o diverses activitats definides, es mostren a la corresponent casella del dia. 
Quan es selecciona un dia es mostra la llista d'assistència existent o una de nova. Els camps d'aquesta fitxa són els següents:

* **Tipus d'activitat**: és un dels tipus d'activitats definits a ``Configuració -> Tipus d'activitats``. 
* **Data**: Data de l'activitat.
* **Total registrats**: Camp calculat pel sistema, que indica el total de membres apuntats a aquesta activitat.
* **Calendari escolar**: Calendari escolar calculat pel sistema, segons la data de l'activitat.

  .. note:: Si la Data de l'activitat no està inclosa en un Calendari escolar, es mostrarà un avís d'aquest fet. Tot i que l'aplicació permet
     introduir activitats fora d'un calendari lectiu, no és recomanable fer-ho.
       
* **Membres**: Llista de membres apuntades a aquesta activitat en aquesta data. Aquesta llista mostra la següent informació:

  * **Membre**
  * **Curs actual**: Camp informatiu calculat pel sistema.
  * **Producte**: Producte que s'aplicarà quan es facturi aquesta activitat.
  * **Comentari**: Camp opcional. En versions futures es podrà fer servir aquest camp per comunicar incidències de menjador, per exemple.
  * **Factura**: Camp només de lectura que mostra en quina factura s'ha facturat aquesta activitat.

Quan es selecciona una activitat en un dia per primera vegada, la llista de membres assistents s'omple amb tots els membres suscrits que s'han definit
en el **Tipus d'activitat**.   

A la fitxa també hi han dos botons:

* **Assistència**: genera un llistat per facilitar el control d'assistència.
* **Actualitza membres**: Combina la llista actual amb la llista de membres suscrits, per si s'han fet molts canvis i es vol tenir la certesa de què s'inclouen els suscrits. 
  Només afegeix els membres suscrits que faltin, no esborra cap membre no suscrit que ja sigui a la llista.

Estats
------

Cada activitat pot tenir tres estats, que es corresponen al flux de treball proposat:

* **Obert**: L'activitat és oberta i admet modificacions, tant per afegir com per esborrar membres. Això permet crear llistes per dates posteriors a l'actual.
* **Tancat**: La llista és tancada i no es poden fer modificacions.

  En el cas del tipus d'activitat de *Menjador*, quan és el dia, per exemple a les 10 hores, la llista es **tanca** i s'imprimeix el llistat d'assistència 
  que permet passar llista al menjador i introduir comentaris. 
  Quan s'acaba el menjador, s'**obre** la llista i s'introdueixen els comentaris. Si ha faltat algun assistent, senzillament s'esborra de la llista.
  Un cop fets els canvis, es torna a **tancar** la llista.

* **Facturat**: Quan el procés de facturació creï factures per a aquesta activitat, l'activitat es marcarà com a **facturada**. Un cop facturada, no es poden fer canvis. 
 
  .. note:: Només es poden facturar llistes d'assistència que estiguin tancades.
  
Els passos d'estat obert a tancat i de tancat a obert es poden fer amb el botó ``Obrir o tancar esdeveniment d'activitat``.

Informes d'activitats
*********************

S'inclouen diferents llistats i resums per facilitar el control d'assistència a les activitats.

Informe mensual d'activitats
----------------------------

A ``Informes -> Llistat mensual d'activitas`` podem generar un resum mensual de les activitats fetes i llurs participants. 
Es selecciona el curs i el mes; només es mostren cursos existents i els mesos d'aquests cursos en els quals s'hagin fet activitats.
La informació mostrada és la següent:

* **Dies lectius totals** del mes del calendari escolar seleccionat.
* **Assistència mensual**: mostra els membres, productes i totals mensuals de cada activitat.

El botó ``Imprimeix assistència mensual`` genera un PDF d'aquest resum.

Resum d'activitats
------------------

a ``Informes -> Resum d'activitats`` es mostren dos gràfiques d'assistència a les activitats:

* Per membre, activitat i producte
* Per activitat, membre i producte

És una gràfica experimental, que permet jugar una mica amb les dimensions de la gràfica.

Facturació d'activitats
***********************

A ``Gestió -> Assistent de facturació d'activitats`` es troba l'assistent per facturar activitats. L'assistent demana la data de venciment. Aquesta data s'ajustarà
automáticament a l'últim dia del mes anterior, per garantir facturacions mensuals completes.

.. note:: L'assistent comprovarà que **totes** les activitats amb una data igual o anterior a la que s'ha especificat estiguin **facturades** o **tancades**. 
   No deixarà seguir si hi han activitats **obertes** abans d'aquesta data. Cal tancar-les per poder continuar.

L'assistent generarà una factura per cada combinació de *Membre a facturar*, *Membre*, *Producte* i *Quantitat* de les activitats. Aquesta factura contindrà una
línia de factura amb el concepte: *Membre* | *Producte* | *Mes i any*, amb el preu unitari definit a *Producte* i amb la *Quantitat* calculada per l'assistent.
L'estat de les factures serà el d'*Esborrany*.
 