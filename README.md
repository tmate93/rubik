# Rubik kocka felismerő (Gépi látás beadandó feladat)

Egy python-ban programozott rubik kocka oldalfelismerő program. A rubik kocka hat oldaláról készült kép alapján készít egy másolatot ahol kijelöli a felismert szegmenseket, illetve egy vizuális reprezentációt is rajzol a képre. A kocka kiterített testhálóját is megjeleníti és belerajzolja az adott oldalt a megfelelő pozícióba az eddig felismert többi oldal mellé egy külön file-ba. Végül egy szövegfile-ba kiírja a karakteres reprezentációját is az oldalaknak.

# Használata:

A rubik kocka mind a hat oldaláról készült egy-egy képet 1-6-ig elnevezve a főkönyvtára kell másolni, majd a program a fent említett módon létrehozza a többi file-t.

# Működése:

A kép beolvasása után átméretezi azt, a könyebb és gyorsabb kezelhetőség érdekében. Ezután szürkeárnyalatossá alakítja, elmossa a képet a zajok kiszűrése érdekében és egy küszöbölléssel binárissá alakítja azt. Ezután azátalakított képen kontúrokat keres majd a csúcsok száma alapján kiszűri a négyszögeket, és ezek oldalainak aránya alapján a négyzeteket. Ezután kiszűri azokat a négyzeteket amelyeknek ötnél kevesebb szomszédja van, így elkülönítve a kocka részeit. Rendezés után megvizsgálja az egyes négyzetek szinét határértékek alapján és eltárolja azokat. Ezután ha sikerült mind a kilenc négyzet szinét azonosítania, kirajzolja a hálót, minden lépéssel bővítve azt. Ezután ellenőrzi, hogy minden oldalt beolvasott-e és ha igen létrehozza a testháló képét és szövegfile-t ami karakteresen reprezentálja a kocka oldalait. 
