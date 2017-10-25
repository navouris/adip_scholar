# adip_scholar
Ένα πρόγραμμα python που επιτρέπει τη δημιουργία καταλόγου αναφορών των μελών ερευνητικής ομάδας με βάση το πρότυπο της ΑΔΙΠ. Το πρότυπο αυτό απαιτεί ετήσιο αριθμό αναφορών για τα 5 τελευταία χρόνια για κάθε μέλος της ερευνητικς ομάδας (πχ για τα μέλη ενός Πανεπιστημιακού Τμήματος). Επίσης σε ξεχωριστές στήλες σημειώνονται οι τιμές των συνολικών αναφορών καθώς και του h-index. Τα στοιχεία συλλέγονται από το Scholar.

Το πρόγραμμα τρέχει με python 3
απαιτεί την ύπαρξη αρχείου με όνομα researchers_url.csv που περιέχει δεδομένα για ερευνητές το προφίλ των οποίων θέλουμε να ανακτήσουμε
Κάθε γραμμή του αρχείου περιλαμβάνει το όνομα του ερευνητή ; το url του προφίλ του στο Scholar πχ
"Einstein Albert","https://scholar.google.gr/citations?user=qc6CJjYAAAAJ&hl=el&oi=ao"

Το πρόγραμμα μας ζητάει το έτος αναφοράς της έκθεσης αν δώσουμε enter θεωρεί ότι είναι το τρέχον έτος και συνεπώς θα μας δώσει στοιχεία για τα έτη Y-6 .. Y-1 όπου Υ το τρέχον έτος.

Την πρώτη φορά που τρέχει κατεβάζει από το Scholar τα αρχεία του προφίλ των ερευνητών, τα οποία συβουλεύεται για τις επόμενες φορές

Παράγει αρχείο citations_y.csv όπου y το έτος αναφοράς. Το αρχείο αυτό είναι κωδικοποιημένο με utf-8 και ανοίγει συνήθως με libre office ή με επεξεργαστή κειμένου που δέχεται αυτή την κωδικοποίηση, ώστε να χρησιμοποιηθεί για περαιτέρω επεξεργασία ή να περιληφθεί στην ετήσια έκθεση της ερευνητικής ομάδας.
