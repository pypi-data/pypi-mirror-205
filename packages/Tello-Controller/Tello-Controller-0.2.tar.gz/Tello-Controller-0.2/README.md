Per far eseguire al Tello una serie di comandi è necessario scriverli uno per riga nel file `comandi.txt`.<br>
I parametri di certi comandi vanno separati dal comando stesso con un solo spazio.<br>
La sintassi per le stringhe passate direttamente come argomento nello `ScriptSender` è la stessa.<br>

Lista di comandi:<br>

`command`; Nessun parametro; Inizializza la ricezione di comandi del drone<br>
`takeoff`; Nessun parametro; Fa decollare il drone da terra fino a circa 120cm di altezza<br>
`emergency`; Nessun parametro; Spegne istantaneamente tutte le eliche. Non sicuro<br>
`land`; Nessun parametro; Fa scendere il drone fino a terra e spegne le eliche quando ci arriva<br>
`up`; Distanza in cm da 20 a 500; Solleva il drone di quanto inserito<br>
`down`; Distanza in cm da 20 a 500; Abbassa il drone di quanto inserito<br>
`left`; Distanza in cm da 20 a 500; Sposta il drone di quanto inserito verso la sinistra relativa al drone<br>
`right`; Distanza in cm da 20 a 500; Sposta il drone di quanto inserito verso la destra relativa al drone<br>
`forward`; Distanza in cm da 20 a 500; Sposta il drone in avanti di quanto inserito<br>
`back`; Distanza in cm da 20 a 500; Sposta il drone all'indietro di quanto inserito più lentamente<br>
`cw`; Angolo da 1 a 360; Ruota il drone in senso orario dell'angolo inserito rispetto al suo asse verticale<br>
`ccw`; Angolo da 1 a 360; Ruota il drone in senso antiorario dell'angolo inserito rispetto al suo asse verticale<br>
`flip`; "l", "r", "f" o "b"; Fa fare al drone una capriola nella direzione specificata e lo ristabilizza. "l" a sinistra, "r" a destra, "f" in avanti, "b" all'indietro.<br>
`stop`; Nessun parametro; Ferma il drone a mezz'aria. Quando viene eseguito interrompe altri comandi in corso<br>


Altri comandi a https://dl-cdn.ryzerobotics.com/downloads/Tello/Tello%20SDK%202.0%20User%20Guide.pdf<br>
