import re
from build_text_model import make_training_data
from wiki import page


subjects = [
    'Milano', 'Salerno', 'Napoli', 'Padova', 'Bomba atomica', 'Java (linguaggio di programmazione)', 'Vero programmatore', 'Spritz',
    'Vaccino', 'MoVimento 5 Stelle', 'Fortnite', 'Complottista', 'Nintendo', 'Game boy', 'Xbox', 'Barba', 'Parigi', 'Euro', 'Lira',
    'Barbone', 'Matteo Salvini', 'Gesù', 'Città del Vaticano', 'Fascismo', 'McDonald\'s', 'Scoreggia', 'Benzinaio', 'Banca', 'Veneto',
    'Pastore sardo', 'Facebook', 'WhatsApp', 'Discord', 'Computer', 'RAM', 'Doom', 'Silvio Berlusconi', 'Una supposta per te', 'Chimica',
    'Economia', 'Spam', 'Trenord', 'Nutella', 'Mr. Bean', 'Natale', 'Intel', 'Cina', 'Mao Zedong', 'Taiwan', 'CIA', 'Cuba', 'Pianta',
    'Extraterrestre', 'Extracomunitario', 'Giardiniere', 'Inglisc', 'Matteo Renzi', 'Emiglio il meglio', 'Matrix (film)', 'Terminator',
    'Android', 'Linux', 'Google', 'Apple Inc.', 'Bill Gates', 'John Fitzgerald Kennedy', 'Barack Hussein Obama', 'South Park', 'Sardegna',
    'Pecora', 'Krukkia', 'Mario Draghi', 'Mastercard', 'Lingua ceca', 'Italiano medio', 'iPhone', 'Gabibbo', 'I Simpson', 'Mario De Filippi',
    'Vittorio Sgarbi', 'Cristiano Malgioglio', 'Sergio Mattarella', 'Presidente della Repubblica Italiana', 'Partigiano', 'Resistenza italiana',
    'Nessuno', 'Opinionista', 'Umberto Bossi', 'Roberto Saviano', 'Bufala', 'YouTube', 'Vangeli', 'Morte', 'Carabinieri', 'Camorra',
    'Marcello Dell\'Utri', 'Bitcoin', 'Elon Musk', 'Multinazionale', 'Tesla (azienda)', 'Top Gear', 'Mamma', 'Primo giorno di scuola',
    'Caffè', 'California', 'Silicon Valley', 'Steve Jobs', 'Stewie Griffin', 'Greta Thunberg', 'Bambino', 'Trenitalia', 'TeleTù', 'Omofobia',
    'Telecom Italia', 'Enel', 'Fedez', 'Wind', 'Internet key', 'Salvatore Aranzulla', 'Immanuel Casto', 'Pover Paint', 'E-mail', 'Radio Maria',
    'Banca centrale europea', 'Mario Monti', 'Banca Mediolanum', 'Unical', 'Coca Cola', 'Vasco Rossi', 'Chinotto', 'Le Iene (programma televisivo)',
    'Filosofia', 'Facoltà di Lettere e Filosofia', 'Polizia', 'Guardia di Finanza', 'Guardia Padana', 'Politecnico di Milano', 'Invisibile unicorno rosa',
    'Politecnico di Torino', 'Università di Bologna', 'Scuola Anormale di Pizza', 'UNICEF',  'Ubuntu', 'Fenomeni da baraccone italiani su YouTube',
    'Partito Socialista Italiano', 'Tizio', 'Studente', 'Politico', 'Andrea Diprè', 'Giulio Andreotti', 'Roma', 'Cocaina',
    'Energia nucleare', 'Eutanasia', 'Francia', 'Rivoluzione francese', 'Mani pulite', 'Stipendio', 'Ritorno al futuro', 'Viaggio nel tempo', 'Esperimento',
    'DeLorean', 'Il laboratorio di Dexter', 'Duracell', 'The Flintstones', 'Struzzo', 'Forno a microonde', 'Radiazione comica di fondo', 'Giove (pianeta)',
    'Universo', 'Bug', 'Gay', 'Windows Vista', 'Che Guevara', 'Fidel Castro', 'Flavio Briatore', 'Dolce&Gabbana', 'Formula 1', 'Red Bull', 'Cervello',
    'Fuga di cervelli', 'Etanolo', 'Videogioco', 'Leggi di Murphy', 'Game Therapy', 'GameStop', 'Nerd', 'Mozilla Firefox', 'Internet Explorer', 'Google Chrome',
    'Australia', 'Foglietto illustrativo', 'Babbo Natale', 'Polo Nord', 'Limone', 'Tè', 'Aperitivo', 'Cultura', 'Qualunquismo', 'Effetto serra',
    'Due di picche', 'Anziano', 'Albero', 'Tassa', 'Benzina', 'Tabacco', 'Religione', 'Pollo', 'Scientology', 'Tom Cruise', 'Top Gun', 'Vegano', 'Gente come te',
    'Coglione', 'Beatles', 'Winx Club', 'Copyright', 'UTorrent', 'Comunismo', 'P2P', 'Informatica', 'Floppy disk', 'Chiesa cazzolica', 'Svezia', 'IKEA'
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
