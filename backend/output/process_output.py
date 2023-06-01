import random
from ro_diacritics import restore_diacritics


def build_response(crime_type, punishment_info):
    crime_type = restore_diacritics(crime_type)
    punishment_info = restore_diacritics(punishment_info)
    templates = [
        "Pentru infracțiunea '{crime}', pedeapsa în România este {punishment}.",
        "Dacă cineva comite '{crime}' în România, poate suporta {punishment}.",
        "În România, pedeapsa pentru '{crime}' este {punishment}.",
        "În ceea ce privește '{crime}', pedeapsa obișnuită în România este {punishment}.",
        "Potrivit Codului Penal, '{crime}' se pedepsește cu {punishment}."
    ]

    hello_templates = [
        "Salut. Cum pot să te ajut azi?",
        "Bună! Cu ce pot sa te ajut?",
        "Salutare. Cu ce pot sa te ajut azi?"
    ]

    thanks_templates = [
        "Mă bucur dacă am putut să te ajut. Dacă mai ai nevoie de ajutor, poți să îmi scrii.",
        "Mă bucur dacă te-am ajutat. Dacă mai ai vreo întrebare, nu ezita să îmi scrii.",
    ]

    if crime_type == "Salut":
        response_template = random.choice(hello_templates)
        return response_template
    if crime_type == "Multumesc":
        response_template = random.choice(thanks_templates)
        return response_template
    if crime_type == "Pa":
        response_template = "Salut."
        return response_template

    if punishment_info:
        response_template = random.choice(templates)
        response = response_template.format(crime=crime_type, punishment=punishment_info)
    else:
        response = "Îmi pare rău, dar nu am găsit informații despre pedeapsa pentru infracțiunea '{}' în România." \
            .format(crime_type)

    return response

# print(build_response("Omorul", "inchisoarea de la 10 la 20 de ani"))
