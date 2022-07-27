import re
from build_text_model import make_training_data
from wiki import page


subjects = [
    'Milano', 'Salerno', 'Napoli', 'Padova', 'Bomba atomica', 'Java (linguaggio di programmazione)', 'Vero programmatore', 'Spritz', 'Vaccino',
    'MoVimento 5 Stelle', 'Fortnite', 'Complottista', 'Nintendo', 'Game boy', 'Xbox', 'Barba', 'Parigi', 'Euro', 'Lira',
    'Barbone', 'Matteo Salvini', 'Gesù', 'Città del Vaticano', 'Fascismo', 'McDonald\'s', 'Scoreggia', 'Benzinaio', 'Banca',
    'Veneto', 'Pastore sardo', 'Facebook', 'WhatsApp', 'Discord', 'Computer', 'RAM', 'Doom', 'Silvio Berlusconi', 'Una supposta per te', 'Chimica',
    'Economia', 'Spam', 'Trenord', 'Nutella', 'Mr. Bean', 'Natale', 'Intel', 'Cina', 'Mao Zedong', 'Taiwan', 'CIA', 'Cuba', 'Pianta', 'Extraterrestre',
    'Extracomunitario', 'Giardiniere', 'Inglisc', 'Matteo Renzi', 'Emiglio il meglio', 'Matrix (film)', 'Terminator', 'Android', 'Linux', 'Google',
    'Apple Inc.', 'Bill Gates', 'John Fitzgerald Kennedy', 'Barack Hussein Obama', 'South Park', 'Sardegna', 'Pecora', 'Krukkia', 'Mario Draghi',
    'Mastercard', 'Lingua ceca', 'Italiano medio', 'iPhone'
]

corpus = ""

for subject in subjects:
    try:
        p = page(title=subject)
        corpus += p.content
    except Exception as e:
        print(e)
        print("Failed on: " + subject)

corpus = re.sub(r'=+ .+ =+', '', corpus)

with open("corpus.txt", "w", encoding="utf8") as fp:
    fp.write(corpus)

make_training_data()
