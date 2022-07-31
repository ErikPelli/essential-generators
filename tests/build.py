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
    'Nessuno', 'Opinionista', 'Umberto Bossi', 'Roberto Saviano', 'Mozzarella di bufala', 'YouTube', 'Vangeli', 'Morte', 'Carabinieri', 'Camorra',
    'Marcello Dell\'Utri', 'Bitcoin', 'Elon Musk', 'Multinazionale', 'Tesla (azienda)', 'Top Gear', 'Mamma', 'Primo giorno di scuola',
    'Caffè', 'California', 'Silicon Valley', 'Steve Jobs', 'Stewie Griffin', 'Greta Thunberg', 'Bambino', 'Trenitalia', 'TeleTù', 'Omofobia',
    'Telecom Italia', 'Enel', 'Fedez', 'Wind', 'Internet key', 'Salvatore Aranzulla', 'Immanuel Casto', 'Pover Paint', 'E-mail', 'Radio Maria',
    'Banca centrale europea', 'Mario Monti', 'Banca Mediolanum', 'Unical', 'Coca Cola', 'Vasco Rossi', 'Chinotto', 'Le Iene (programma televisivo)',
    'Filosofia', 'Facoltà di Lettere e Filosofia', 'Polizia', 'Guardia di Finanza', 'Guardia Padana', 'Politecnico di Milano', 'Invisibile unicorno rosa',
    'Politecnico di Torino', 'Università di Bologna', 'Scuola Anormale di Pizza', 'UNICEF',  'Ubuntu', 'Fenomeni da baraccone italiani su YouTube',
    'Partito Socialista Italiano', 'Tizio', 'Studente', 'Politico', 'Andrea Diprè', 'Giulio Andreotti', 'Roma', 'Cocaina', 'Capitan Findus', 'Pubblicità',
    'Energia nucleare', 'Eutanasia', 'Francia', 'Rivoluzione francese', 'Mani pulite', 'Stipendio', 'Ritorno al futuro', 'Viaggio nel tempo', 'Esperimento',
    'DeLorean-DMC-12', 'Il laboratorio di Dexter', 'Duracell', 'The Flintstones', 'Struzzo', 'Forno a microonde', 'Radiazione comica di fondo', 'Giove (pianeta)',
    'Universo', 'Bug', 'Gay', 'Windows Vista', 'Che Guevara', 'Fidel Castro', 'Flavio Briatore', 'Dolce&Gabbana', 'Formula 1', 'Red Bull', 'Cervello',
    'Fuga di cervelli', 'Etanolo', 'Videogioco', 'Leggi di Murphy', 'Game Therapy', 'GameStop', 'Nerd', 'Mozilla Firefox', 'Internet Explorer', 'Google Chrome',
    'Australia', 'Foglietto illustrativo', 'Babbo Natale', 'Polo Nord', 'Limone', 'Tè', 'Aperitivo', 'Cultura', 'Qualunquismo', 'Effetto serra',
    'Due di picche', 'Anziano', 'Albero', 'Tassa', 'Benzina', 'Tabacco', 'Religione', 'Pollo', 'Scientology', 'Tom Cruise', 'Top Gun', 'Vegano', 'Gente come te',
    'Coglione', 'Beatles', 'Winx Club', 'Diritto d\'autore', 'UTorrent', 'Comunismo', 'P2P', 'Informatica', 'Floppy disk', 'Chiesa cazzolica', 'Svezia', 'IKEA',
    'Gioconda', 'Occhio', 'Stronzo', 'Idiota', 'Mazzancolla', 'Ragno', 'Pesci', 'Buddha', 'Emmett Brown', 'Galera', 'Mar Mediterraneo', 'Film', 'Cinema', 'Premio Oscar',
    'Snoop Dogg', 'Scooby Doo', 'Uomo (maschio)', 'Mai', 'Pokémon (videogioco)', 'Homo sapiens', 'Aztechi', 'Scimmia', 'Intellettuale', 'Coraggio', 'Giuseppe Garibaldi',
    'Pokémon (creatura)', 'Pedofilia', 'MOIGE', 'George Orwell', 'Fratello maggiore', 'Grande Fratello (programma televisivo)', 'Adolf Hitler', 'Scienza', 'Peppa Pig',
    'Famiglia', 'Omicidio', 'Epifania', 'Pozzanghera', 'Caritas', 'Papa Francesco', 'Re Magi', 'Gorbaciov', 'Boris Eltsin', 'Germano Mosconi', 'Friedrich Nietzsche',
    'Belgio', 'Ungheria', 'Servizio sanitario nazionale', 'Governo', 'Costituzione della Repubblica Italiana', 'OMS', 'Farmacista', 'Laurea', 'Farmaco',
    'Medico', 'Maccio Capatonda', 'Tumore', 'Buddhismo', 'Carnevale', 'Lupo Alberto', 'Forza', 'Mosè', 'Roberto Giacobbo', 'Alieni comunisti', 'Egitto', 'India',
    'Cammello', 'Mario Giordano', 'World of Warcraft', 'Ambientalista', 'ITIS', 'Colesterolo', 'Giappone', 'Disoccupato', 'Nonno', 'Escursione termica',
    'Sushi', 'Sumo', 'Forse', 'Laura Pausini', 'Cane', 'Brian Griffin', 'Televisione', 'Fuoco', 'Cacca di cane', 'Rapper', 'Ano', 'Metallaro', 'Università', 'Volo',
    'Topolino (personaggio)', 'Walt Disney', 'Briscola', 'Boeing', 'Arma di distruzione di massa', 'Anno', 'Liceo', 'Liceo scientifico', 'Liceo linguistico',
    'Organizzazione delle Nazioni Unite', 'Afroitaliano', 'Spacciatore', 'Gianfranco Fini', 'George W. Bush', 'Tg4', 'Mediaset', 'Gerry Scotti', 'Maurizio Costanzo',
    'Arcore', 'Lourdes', 'Vanna Marchi', 'Marilyn Manson', 'Letargo', 'Mojito', 'Rete 4', 'Emilio Fede', 'Europarlamento', 'Corea del nord', 'La ruota della fortuna',
    'Tortura', 'Medioevo', 'Deluso di sinistra', 'Telefono cellulare', 'Nokia', 'Nokia 3310', 'Armi di distrazione di massa', 'Pubblicità della Cedrata Tassoni', 
    'Miss Italia', 'Sasso', 'Acqua', 'Particella di sodio', 'Trattato di Lisbona', 'Elezioni europee', 'Enrico Papi', 'Uomo Gatto', 'Truzzo', 'Random', 'Chef Tony',
    'Miracle Blade', 'Bibbia', 'Josif Stalin', 'Lenin', 'Antonio Gramsci', 'Globalizzazione', 'Classe operaia', 'Pacifismo', 'Pop (genere musicale)', 'ConFindustria',
    'Parlamento', 'Molise', 'Navigatore satellitare', 'Meteorologia', 'Immaginazione', 'Suonerie per cellulari di Italia 1', 'Operatore di call center', 'Scienze delle merendine',
    'Just Eat', 'A nessuno importa', 'BIOS', 'Zingaro', 'Read Only Memory', 'Mafia', 'Esame di stato', 'Radio Padania Libera', 'Padania', 'Indipendentismo padano', 'Lega Nord',
    'Dittatura', 'Edward mani di forbice', 'Gillette Fusion', 'Messaggio subliminale', 'Harry Potter', 'Albania', 'Inquisizione',
    'Alcide De Gasperi', 'Squola', 'Bart Simpson', 'DJ', 'Musica house', 'Campo magnetico', 'Nikola Tesla', 'Ponzio Pilato', 'INPS', 'Tirocinio', 'Full Metal Jacket', 'Piazzista',
    'Rai', 'Piero Angela', 'ISTAT', 'Barbara d\'Urso', 'Maestra', 'Erba', 'Albert Einstein', 'Genova', 'Cristoforo Colombo', 'UEFA Champions League', 'Miopia', 'Ricercatori Oral B',
    'Galileo Galilei', 'Terra', 'Matematica', 'Sindaco', 'Gardaland', 'Cosi che escono dalle fottute pareti',
    'Presidente del Consiglio dei Ministri', 'Francesco Totti', 'Soldi', 'Giornalista', 'Rompicoglioni',
    'Mondo', 'Sacra Sindone', 'Atlantide', 'Focus', 'Padre Pio', 'Loch Ness', 'Svizzera', 'Troll (Internet)',
    'Tsunami', 'Mosca (Russia)', 'Russia', 'Vodka', 'Maya', 'Vladimir Putin',
    'Voci nella testa', 'Cesso', 'Fisica', 'Storia', 'Risata malvagia', 'Fortuna', 'Architetto',
    'Giovanni Muciaccia', 'QI', 'Arabi', 'Maometto', 'Roberto Speranza', 'Luigi Di Maio', 'Mario Luigi', 'Super Mario',
    'Beppe Grillo', 'Scie chimiche', 'Bomba Molotov', 'Sampietrino', 'Infermiere', 'Contraddizione',
    'Tombola', 'Senato', 'Camera dei deputati', 'Centro benessere',
    'Educazione fisica', 'Professore di educazione fisica', 'Biologia', 'Geografia', 'Expo 2015',
    'G8 di Genova', 'Candid Camera', 'Anonymous', 'Macchina del tempo a manovella', 'Federazione dei Verdi',
    'Arabia Saudita', 'Cernobyl', 'Laser', 'Scherzo', 'Sommelier', 'Austria', 'Olocausto', 'Enrico Letta',
    'Enrico Berlinguer', 'Enrico Fermi', 'Enrico Mentana', 'Enrico Pasquale Pratticò', 'Bettino Craxi', 'Peter Griffin', 'Atomo',
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
