import json, httpx
from ..config import settings
from ..db import db
 
SYSTEM = """Tu es KIM, assistant d'orientation du Centre Sportif, Culturel et des TIC Ivoiro-Coréen Alassane Ouattara. Réponds dans la langue de l'utilisateur (français, anglais ou coréen). Utilise uniquement les informations du contexte. Ne fabrique jamais horaires, contacts, tarifs, places ou disponibilités. Si le contexte ne répond pas, dis que tu ne disposes pas d'une source vérifiée et propose de transmettre la question à l'équipe. Tu peux préparer des demandes mais tu ne confirmes JAMAIS une réservation ou une inscription : seule l'équipe humaine décide. Mentionne les sources fournies en fin de réponse."""

CENTRE_SOURCE = "Site officiel du CSCTICAO — https://www.cscticao.ci/"
ADDRESS = "Le Centre se trouve à Abidjan-Cocody, derrière le lycée technique, dans le quartier Ancien Washington."
CONTACT = "Vous pouvez joindre l’accueil au +225 27 22 22 27 07 ou écrire à info@cscticao.ci."
FACILITIES = "Le Centre dispose notamment d’un gymnase, d’une bibliothèque, de salles de classe, d’une salle multimédia et d’une salle polyvalente."


async def answer(message: str, language: str = "fr"):
    with db() as c:
        if settings.storage_mode == 'snowflake':
            cur = c.cursor()
            cur.execute('SELECT NAME,CATEGORY,ELIGIBILITY,DESCRIPTION,PLACES FROM ACTIVITIES WHERE ACTIVE=TRUE')
            acts = [dict(zip(['name','category','eligibility','description','places'], row)) for row in cur.fetchall()]
            cur.execute('SELECT NAME,CAPACITY,EQUIPMENT FROM ROOMS WHERE ACTIVE=TRUE')
            rooms = [dict(zip(['name','capacity','equipment'], row)) for row in cur.fetchall()]
            cur.close()
        else:
            acts = [dict(r) for r in c.execute('SELECT name,category,eligibility,description,places FROM activities WHERE active=1').fetchall()]
            rooms = [dict(r) for r in c.execute('SELECT name,capacity,equipment FROM rooms WHERE active=1').fetchall()]
    context = {"activites": acts, "salles": rooms, "horaires": "Non renseignés dans les données vérifiées de démonstration.", "source": "Catalogue local de démonstration — à valider par le Centre"}
    context["fiche_officielle"] = {"adresse": ADDRESS, "accueil": CONTACT, "espaces": FACILITIES, "source": CENTRE_SOURCE}
    if settings.ai_provider == 'cortex' and settings.storage_mode == 'snowflake':
        prompt = SYSTEM + '\nCONTEXTE STRUCTURÉ : ' + json.dumps(context, ensure_ascii=False) + '\nQUESTION : ' + message
        with db() as c:
            cur = c.cursor()
            cur.execute('SELECT SNOWFLAKE.CORTEX.COMPLETE(%s, %s)', (settings.cortex_model, prompt))
            row = cur.fetchone()
            cur.close()
        return {"answer": row[0] if row else 'Je ne peux pas répondre pour le moment.', "sources":[context['source'], CENTRE_SOURCE], "provider":"snowflake-cortex"}
    if settings.ai_provider == 'openai_compatible' and settings.llm_api_key:
        async with httpx.AsyncClient(timeout=35) as client:
            r = await client.post(settings.llm_base_url.rstrip('/') + '/chat/completions',headers={'Authorization':f'Bearer {settings.llm_api_key}'},json={'model':settings.llm_model,'temperature':0.2,'messages':[{'role':'system','content':SYSTEM+'\nCONTEXTE: '+json.dumps(context,ensure_ascii=False)},{'role':'user','content':message}]})
            r.raise_for_status()
            return {"answer":r.json()['choices'][0]['message']['content'],"sources":[context['source'], CENTRE_SOURCE],"provider":"llm"}
    # Réponse locale contrôlée, sans inventer de faits.
    q = message.lower()
    practical = []
    if any(k in q for k in ("adresse", "itinéraire", "itineraire", "situé", "situe", "trouve", "localis", "venir", "rendre", "où est", "location", "address", "위치")):
        practical.append(ADDRESS + " Ouvrez la rubrique de visite du Centre pour afficher la carte et obtenir un itinéraire.")
    if any(k in q for k in ("contact", "téléphone", "telephone", "numéro", "appeler", "joindre", "mail", "phone", "연락")):
        practical.append(CONTACT)
    if any(k in q for k in ("bibliothèque", "gymnase", "multimédia", "équipements", "espaces")):
        practical.append(FACILITIES)
    if any(k in q for k in ("horaire", "ouvert", "tarif", "prix", "combien coûte", "hours", "open", "시간")):
        practical.append("L’accueil pourra confirmer les horaires et les tarifs." )
        if CONTACT not in practical:
            practical.append(CONTACT)
    if practical:
        return {"answer": " ".join(practical), "sources": [CENTRE_SOURCE], "provider": "local-fallback"}
    if any(k in q for k in ['activité','activités','activity','taekwondo','python','formation','cours','활동']):
        body = 'Voici le catalogue de démonstration actuellement chargé :\n' + '\n'.join(f"• {a['name']} — {a['category']} — {a['eligibility']} — {a['places']} places indicatives" for a in acts)
    elif any(k in q for k in ['salle','réserver','reservation','room','예약']):
        body = 'Je peux préparer une demande de salle. Les salles et capacités affichées sont des données de démonstration ; leur disponibilité doit être confirmée par l’équipe du Centre. Utilisez « Demander une salle » pour transmettre votre besoin.'
    elif any(k in q for k in ['horaire','ouvert','contact','adresse','hours','open','연락','시간']):
        body = 'Je ne dispose pas encore d’une source officielle vérifiée pour cette information. Je préfère ne pas vous donner une réponse incertaine. Vous pouvez transmettre votre question à l’équipe via une demande de contact.'
    else:
        body = 'Je peux vous orienter vers les activités, préparer une demande de salle, recueillir une pré-inscription ou transmettre une proposition de partenariat. Pour une information officielle absente de ma base, je préfère solliciter l’équipe du Centre.'
    return {"answer":body,"sources":[context['source']],"provider":"local-fallback"}
