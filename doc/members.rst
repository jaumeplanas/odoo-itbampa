=======
Membres
=======

S'aprofita el model ``res.partner`` de tercers bàsic de l'Odoo per definir els membres que formen l'AMPA.

És convenient omplir la informació de contacte: sempre és útil per consultar un telèfon o una adreça. 
Els camps de telèfon mòbil i adreça de correu electrònic serviran per imprimir un llistat dels membres d'una Junta amb aquesta informació de contacte, per exemple.

Els membres de l'AMPA es distingueixen de la resta de *partners* amb el camp ``ampa_partner_type``, **Tipus membre AMPA**, que pot tenir **tres** valors possibles:

* **Cap valor**, per indicar que és un *partner* comercial que no forma part de l'AMPA.
* **Tutor**, són els pares i mares que formen l'AMPA. Més genèricament, són els tercers relacionats amb l'AMPA que no són alumnes.
* **Estudiant** o **alumne**, són els fills i filles dels *Tutors* que estudien a l'Escola. Bàsicament, la distinció és entre qui pot pagar i qui no.

Alumnes
*******

A la pestanya ``AMPA``, els **alumnes** tenen els següents camps necessaris:

* **Data de naixement**
* **Cursos de retard** o avançament. Juntament amb la **Data de naixement**, permet saber quin curs estudia (primer, segon de primària, etc.). 
  Un valor positiu vol dir repetidor; un valor negatiu vol dir que va avançat.
* **Membre a facturar** és el **tutor** responsable de pagar les despeses generades per l'**alumne**.
* **Tutors**: Llista de tutors responsables de cada **alumne**. Normalment són el pare i la mare, però evidentment hi poden haver casos diferents. 
* **Curs actual**: És un camp només de lectura, calculat pel sistema. 

A la pestanya ``Vendes i compres``:

* **Client**: Sí

A la pestanya ``Comptabilitat``:

* **Customer Payment Term**: Cap
* **Customer Payment Mode**: Cap

Tutors
******

A la pestanya ``AMPA``, els **tutors** tenen els següents camps necessaris:

* **Membre a facturar** és el **tutor** responsable de pagar despeses generades. Normalment serà ell mateix.
* **Fills**: Llista d'**alumnes** que són responsabilitat d'aquest membre tutor.

A la pestanya ``Vendes i compres``:

* **Client**: Sí

A la pestanya ``Comptabilitat``:

Si aquest membre és responsable de fer pagaments, els camps següents són necessaris:

* **TIN o NIF**, és el NIF de la persona. Cal afegir les lletres ``ES`` al NIF, per exemple, *ES12345678A*
* **Compte a cobrar**, comproveu que és ``448200 Afiliados``.
* **Customer Payment Term**: Cap
* **Customer Payment Mode**: Hi han dues opcions:

  * Si els pagaments es faran mitjançant un compte bancari, cal triar un valor, normalment ``Rebut SEPA`` o similar.
  * Si els pagaments es fan manuals, deixeu el camp en blanc.

* **Números de compte**. Si es selecciona un Mode de Pagament, aquest camp és necessari. Si el Mode de Pagament és buit, es pot deixar buida 
  també aquesta llista de comptes bancaris.
