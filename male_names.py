import random

spanish_names = [
    "Alejandro", "Mateo", "Javier", "Carlos", "Miguel", "Luis", "Diego", "Santiago",
    "Gabriel", "José", "Juan", "Francisco", "Daniel", "Manuel", "Antonio", "Jorge",
    "Rafael", "Alberto", "Fernando", "Pablo", "Andrés", "Adrián", "Emilio", "Héctor",
    "Iván", "Roberto", "Raúl", "Julio", "Gonzalo", "Eduardo", "Víctor", "Mario",
    "Ángel", "Sergio", "Rubén", "Esteban", "Felix", "Joaquín", "Óscar", "Pedro",
    "Ricardo", "Enrique", "Francisco", "Ignacio", "Salvador", "Xavier", "Aleix"
]

north_african_names = [
    "Mohamed", "Ahmed", "Youssef", "Amir", "Ali", "Omar", "Khalid", "Ismail",
    "Said", "Abdullah", "Yasin", "Hassan", "Mustafa", "Karim", "Hamza", "Anwar",
    "Farid", "Zayd", "Jamal", "Nabil", "Tariq", "Kamal", "Mehdi", "Rachid",
    "Othmane", "Aziz", "Malik", "Bilal", "Samir", "Hakim", "Najib", "Jalil"
]

french_names = [
    "Pierre", "Jean", "Jacques", "François", "Paul", "Michel", "Louis", "Claude",
    "Henri", "Philippe", "Antoine", "Sylvain", "Olivier", "Guillaume", "Étienne",
    "Vincent", "Romain", "Alexandre", "Sébastien", "Rémy", "Thierry", "Baptiste",
    "Luc", "Gérard", "Alain", "Mathieu", "Lionel", "Damien", "Fabien", "Christophe",
    "Yves", "Cédric", "Georges", "René", "Nicolas", "Arnaud", "Julien", "Patrice",
    "Didier", "Joël", "Xavier", "Fabrice", "Benjamin", "Denis", "Emmanuel", "Cyril"
]

italian_names = [
    "Giuseppe", "Luca", "Alessandro", "Marco", "Francesco", "Andrea", "Matteo", "Davide",
    "Giovanni", "Lorenzo", "Stefano", "Riccardo", "Simone", "Antonio", "Nicola", "Alberto",
    "Filippo", "Fabio", "Roberto", "Enrico", "Michele", "Claudio", "Gabriele", "Emanuele",
    "Massimo", "Vincenzo", "Salvatore", "Federico", "Alessio", "Leonardo", "Mario", "Gianluca",
    "Domenico", "Diego", "Angelo", "Raffaele", "Luigi", "Bruno", "Alessio", "Pietro", "Renato",
    "Giacomo", "Dario", "Valentino"
]

# Combine all the lists
all_names = spanish_names + north_african_names + french_names + italian_names

# Example usage
print("Total number of names:", len(all_names))
print("Sample names:", all_names[:10])

personality_adjectives = [
    "Adventurous", "Affectionate", "Agreeable", "Ambitious", "Amiable", "Analytical", "Artistic", "Assertive",
    "Attentive", "Bold", "Calm", "Caring", "Charismatic", "Cheerful", "Clever", "Compassionate", "Confident",
    "Cooperative", "Courageous", "Creative", "Curious", "Determined", "Diplomatic", "Easygoing", "Empathetic",
    "Energetic", "Enthusiastic", "Friendly", "Generous", "Genuine", "Graceful", "Gracious", "Helpful",
    "Honest", "Humorous", "Imaginative", "Independent", "Innovative", "Insightful", "Intelligent", "Joyful",
    "Kind", "Loyal", "Meticulous", "Open-minded", "Optimistic", "Passionate", "Patient", "Perceptive",
    "Persistent", "Polite", "Practical", "Proactive", "Reliable", "Resilient", "Resourceful", "Respectful",
    "Self-confident", "Sincere", "Steadfast", "Sympathetic", "Tactful", "Thoughtful", "Trustworthy", "Understanding",
    "Versatile", "Warm-hearted", "Witty", "Adaptable", "Altruistic", "Charming", "Dynamic", "Eloquent", "Faithful",
    "Inventive", "Mellow", "Nurturing", "Pleasant", "Quirky", "Receptive", "Sociable", "Tenacious", "Unassuming",
    "Vivacious", "Wholesome", "Zealous", "Admirable", "Balanced", "Diligent", "Exuberant", "Forgiving", "Grateful",
    "Harmonious", "Inquisitive", "Jovial", "Keen", "Lively", "Modest", "Nonjudgmental", "Outgoing", "Praiseworthy",
    "Radiant", "Stoic", "Trusting", "Unselfish", "Vibrant", "Wise", "Yielding", "Zestful"
]


def get_personality():
    random.shuffle(personality_adjectives)
    return personality_adjectives[0].lower()


def get_random():
    random.shuffle(all_names)
    return all_names[0]
