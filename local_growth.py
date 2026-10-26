"""Post-construction and cost content, with distinct city planning scenarios."""
from html import escape as e
from urllib.parse import urlencode

POST_SLUG = 'post-construction-high-dusting'
POST_PATH = '/services/' + POST_SLUG + '/'
FR_POST_PATH = '/fr/services/depoussierage-apres-construction/'
COST_PATH = '/guides/high-dusting-cost/'
FR_COST_PATH = '/fr/guides/prix-depoussierage-hauteur/'
POST_IMAGE = '/assets/services/' + POST_SLUG + '.webp'
FR_POST_IMAGE = '/assets/services/post-construction-high-dusting-fr.webp'
COST_IMAGES = {False: '/assets/guides/high-dusting-cost-en.webp', True: '/assets/guides/high-dusting-cost-fr.webp'}
TRANSLATIONS = {POST_PATH: FR_POST_PATH, COST_PATH: FR_COST_PATH}
POST_SERVICE = (POST_SLUG, 'Post-construction high dusting', 'Finish the work above. Prepare the space below.', '',
    'Remove settled construction dust from accessible rafters, beams, duct exteriors, high ledges and fixture housings after a commercial build, renovation or tenant fit-out. We define the overhead scope with your contractor or facility team and plan around remaining trades, protected finishes and the handover schedule.',
    ['Overhead surfaces in new builds, renovations and tenant improvements',
     'Access and protection coordinated with the contractor or facility team',
     'A defined clean after dust-producing work, with any return visit agreed separately'])

# These are project-planning scenarios, not claims about local branches or completed jobs.
CITY_HANDOVERS = {
 'toronto': 'For a tenant renovation, identify which overhead zones belong to the new fit-out and which remain shared with neighbouring occupants. Agree building access and loading time before the final clean, then separate any later contractor touch-ups from the handover scope.',
 'mississauga': 'For a warehouse expansion, plan overhead cleaning before newly installed racks are loaded where practical. Mark both the existing operating aisles and the extension, and tell us when the contractor will release each zone.',
 'brampton': 'If a loading area is being refurbished while dispatch continues, separate the construction zone from active docks. Confirm when overhead door work is finished and how goods beneath the cleaning area will be protected.',
 'vaughan': 'After a packaging-area fit-out, coordinate the overhead clean with the site quality team before product is introduced. Identify which ceilings sit above open-product zones and which are above sealed storage so the boundaries are explicit.',
 'markham': 'For an assembly-space renovation, show where new overhead services pass above sensitive workstations. Agree whether the clean can happen before equipment commissioning and document any areas that must remain covered throughout the work.',
 'hamilton': 'After alterations to a fabrication bay, distinguish construction dust from existing process deposits on the steelwork. Have the site team identify the materials and release crane or machine areas before an overhead method is agreed.',
 'ottawa': 'For an institutional refurbishment, give each building its own handover date and access contact. Schedule atrium and corridor work around remaining trades, escorts and the dates when staff or public occupants return.',
 'london': 'When a production extension connects to an operating plant, define the boundary between the new space and existing sanitation zones. Coordinate the overhead clean with contractor completion and the facility’s own final sanitation sequence.',
 'kitchener': 'For a workshop conversion, mark newly installed ducts, lights and structural surfaces separately from retained equipment. An area-by-area release helps avoid sending cleaning equipment back through a finished zone when another trade still needs access.',
 'waterloo': 'For campus refurbishment, list the rooms being handed back and their first scheduled use. Ceiling work above teaching spaces, gym floors and research-support areas may need separate access windows and finish protection.',
 'cambridge': 'After conveyor or production-line installation, identify the last clear route to the overhead structure before guarding and equipment obstruct it. Agree the timing with the installation team and confirm which surfaces will remain reachable.',
 'guelph': 'For a food-facility renovation, have the site lead distinguish construction deposits from existing product residues. Agree which overhead surfaces are included and where the facility’s specialist sanitation work begins before scheduling the handover clean.',
 'windsor': 'For a tooling-bay refit, coordinate overhead access with crane release and equipment installation. Photograph floor transitions and the planned lift route, then agree whether cleaning occurs before or after the machinery is returned to position.',
 'oshawa': 'Where a building is refurbished one bay at a time, list the handover order and the bays that continue operating. Treat each return visit and equipment move as part of the plan when comparing the scope and cost.',
 'burlington': 'For a warehouse-and-showroom renovation, split structural overhead cleaning from finish-sensitive display areas. Confirm when signage and lighting installation are complete, and identify the point at which stock and showroom fixtures will move back in.',
 'oakville': 'After a showroom fit-out, identify delicate ceiling features, installed lighting and finished flooring before selecting access equipment. An agreed clean before vehicles or displays return can give a clearer working area than a later occupied-space visit.',
 'barrie': 'For a retail or service-space refit, group the overhead surfaces by room and ceiling height. List the remaining trades and the delivery date for fixtures so cleaning and final placement can be scheduled in the right order.',
 'kingston': 'For an occupied-building refurbishment, define the renovated rooms and the routes through spaces that remain in use. Note decorative finishes and public bookings so the overhead handover work can be scoped without assuming the whole property is vacant.',
 'greater-sudbury': 'After a maintenance-bay renovation, ask the site team to identify deposits on retained steelwork as well as new surfaces. Confirm the release of large equipment and service lines before planning the final overhead cleaning pass.',
 'thunder-bay': 'For work across several refurbished buildings, list each address, entry point and contractor handover date. Confirm receiving arrangements for access equipment rather than assuming that one delivery and setup will cover the entire project.',
 'montreal': 'Pour un agrandissement d’entrepôt, précisez quand les nouveaux rayonnages seront installés et chargés. Séparez les allées en activité de la zone des travaux et convenez de la remise de chaque secteur avant le nettoyage en hauteur.',
 'quebec-city': 'Pour la rénovation d’un bâtiment institutionnel, planifiez séparément les atriums, les gymnases et les corridors. Indiquez la fin des travaux poussiéreux, les revêtements à protéger et la date de retour des occupants dans chaque espace.',
 'laval': 'Après l’aménagement d’une zone alimentaire, coordonnez le nettoyage en hauteur avec votre équipe qualité. Précisez les surfaces au-dessus des produits ouverts, les limites sanitaires et l’ordre prévu avant la remise en production.',
 'gatineau': 'Pour plusieurs bâtiments rénovés, donnez une date de remise et une personne-ressource par adresse. Les autorisations, les escortes et les chemins de livraison doivent être confirmés pour chaque intervention, même dans un même portefeuille.',
 'longueuil': 'Après la modification d’un atelier, montrez les nouvelles installations sous les poutres et les conduits. Convenez de la période d’accès avant la remise en place des postes sensibles et précisez les protections à conserver pendant le nettoyage.',
 'sherbrooke': 'Pour un atelier ou un espace d’enseignement réaménagé, distinguez les zones d’essai, les réserves et les salles occupées. Planifiez le nettoyage après les derniers travaux poussiéreux, avec une remise propre à chaque usage.',
 'trois-rivieres': 'Après des travaux dans une installation industrielle, distinguez les dépôts de chantier des résidus de production. Faites préciser les matériaux par l’équipe du site et confirmez la disponibilité des passerelles et des zones sous les ponts roulants.',
 'vancouver': 'For a commercial fit-out with limited staging space, confirm equipment delivery and the route through finished areas before handover. Identify atrium glass, floor finishes and remaining overhead installations so the cleaning scope matches the available access.',
 'surrey': 'For a distribution-space expansion, show how the construction area meets active picking aisles. Plan the overhead clean around rack installation and the arrival of stock, with clear boundaries for any zones that remain operational.',
 'burnaby': 'After a studio or workshop refit, distinguish fixed overhead surfaces from rigging and specialist equipment. Confirm who authorizes access to suspended services and agree which parts can be cleaned without changing their settings or positions.',
 'richmond': 'For a freight-building renovation, include contractor release dates alongside security and receiving arrangements. Record the equipment route from the delivery point to the overhead work zone, especially where doors or enclosed areas restrict movement.',
 'abbotsford': 'For a storage or processing extension, identify where construction dust could overlap with operating areas. Have the site team set product-protection boundaries and confirm when the new overhead surfaces are ready for assessment and cleaning.',
 'victoria': 'For a public-facing property renovation, identify retained decorative surfaces alongside new work. Agree the cleaning method and access route before equipment crosses finished floors, and separate the contractor handover from public reopening arrangements.',
 'kelowna': 'After a packaging or beverage-space refit, list moisture-sensitive finishes and the equipment being commissioned. Confirm the overhead cleaning window before the space returns to use, with process-residue treatment scoped separately where needed.',
 'kamloops': 'For a multi-bay renovation, show differences in ceiling height and floor level between the work areas. Plan the order of cleaning with the contractor so access equipment can move between bays before routes are closed by final installations.',
 'nanaimo': 'For a phased commercial refurbishment, confirm whether suitable access equipment can stay on site between releases. List any additional properties separately so repeat mobilisation and different handover dates are visible in the quote.',
 'calgary': 'For a high-bay fit-out, record the highest beam or ledge included in the handover clean. Ask the contractor when mezzanines, racks and services will be complete, then confirm access before stock or equipment fills the work area.',
 'edmonton': 'After a workshop upgrade, identify dust from the construction work separately from material already deposited by fabrication. Coordinate access to crane zones and protected workstations with the site team’s commissioning and equipment-release plan.',
 'red-deer': 'For a service-bay refurbishment, confirm when overhead doors, heaters and suspended lines are finished. An agreed bay-by-bay handover can clarify equipment moves and return visits where the rest of the workshop stays in use.',
 'lethbridge': 'After changes to a processing or dry-storage space, identify the materials present before proposing a clean. Coordinate overhead work with the site sanitation sequence and keep the boundary between construction deposits and product residues explicit.',
 'fort-mcmurray': 'For a controlled-access building refit, include orientation, entry-point and equipment-release requirements with the contractor’s handover dates. Confirm mobilisation arrangements before treating a short cleaning window as a confirmed booking.',
 'saskatoon': 'For a processing or agricultural-storage renovation, ask the site team to identify both the construction deposits and stored materials. Share any existing dust assessment and agree the cleaning boundary before equipment and timing are proposed.',
 'regina': 'After an equipment-facility fit-out, mark where parked machinery or pallets will restrict access to the new overhead surfaces. Agree which areas can be cleared for handover and whether cleaning needs to follow several installation stages.',
 'winnipeg': 'For a distribution-centre refurbishment, align contractor release with receiving, picking and dispatch schedules. Define overhead cleaning zones individually so a quiet period in one part of the building does not imply access throughout the facility.',
 'brandon': 'For a processing-site upgrade, coordinate the contractor’s final overhead work with the facility’s sanitation team. Record the production restart window, product-protection requirements and any separate specialist cleaning expected after the overhead dust removal.',
 'halifax': 'For a logistics or commercial refurbishment, identify the exact building and the zone being handed over. Keep active dock operations separate from finished public-facing areas when planning access, protection and the final cleaning sequence.',
 'moncton': 'After a distribution-space renovation, distinguish open warehouse areas from enclosed or temperature-controlled zones. Confirm the handover order and stocking schedule so the cleaning quote accounts for the actual number of setups and visits.',
 'st-johns': 'For a commercial fit-out, confirm a usable staging area and the equipment-delivery route with the contractor. If several properties are involved, provide each handover date and address so mobilisation can be assessed for the real sequence of work.',
 'charlottetown': 'For a retail or recreation-space renovation, plan overhead work around the first bookings and the return of fixtures. Note the route across finished areas and agree which surfaces below fans, lights and ledges require protection.',
 'whitehorse': 'For a warehouse or public-building refurbishment, confirm access-equipment availability alongside the contractor’s completion date. Include delivery and storage arrangements early so the overhead handover scope can be matched to a workable mobilisation plan.',
 'yellowknife': 'For a service-building upgrade, identify entry requirements, suitable equipment and the areas ready for release. Confirm the delivery arrangements before setting the final overhead cleaning date, particularly where several buildings are included.',
 'iqaluit': 'For a public-building renovation, provide photographs of entrances and overhead surfaces before fixing the handover cleaning scope. Equipment availability and mobilisation feasibility need to be established for the actual site before a price or work date is confirmed.',
}

COST_NOTES = {
 'warehouses': 'Rack height, aisle clearance, stock protection and the number of equipment setups all affect the scope. Two warehouses with the same floor area can involve very different overhead access and working time.',
 'manufacturing': 'Machinery, suspended services, equipment release and the material being removed affect the work. Identify access interruptions and protection needs so the quote reflects the actual production space.',
 'food-processing': 'Product protection, sanitation boundaries and the characteristics of the deposits affect the proposed method and timing. Agree those boundaries with the site team before comparing overhead cleaning quotes.',
 'education': 'Room layout, public access, bookings and finish protection affect the working window. A gym and an atrium in the same building may need different equipment and separate setups.',
 'retail': 'Atrium height, delicate finishes, display protection and access through occupied areas affect pricing. Explain what can be moved and when the space can be closed to customers.',
}
FR_COST_NOTES = {
 'warehouses': 'La hauteur des rayonnages, le dégagement des allées, la protection des marchandises et le nombre de mises en place influencent les travaux. La superficie au sol ne décrit pas à elle seule les accès en hauteur.',
 'manufacturing': 'Les machines, les services suspendus, la disponibilité des équipements et la nature des dépôts influencent les travaux. Précisez les obstacles et les protections nécessaires pour comparer des portées équivalentes.',
 'food-processing': 'La protection des produits, les limites sanitaires et la nature des dépôts influencent la méthode et le calendrier. Confirmez ces limites avec l’équipe du site avant de comparer les soumissions.',
 'education': 'La disposition des pièces, les horaires publics, les réservations et les revêtements à protéger influencent les accès. Un gymnase et un atrium peuvent nécessiter des équipements et des mises en place différents.',
}

def city_sections(city, origin):
    fr = city['province'] == 'QC'
    name = e(city['name'])
    query = '?' + urlencode({'city': city['name'] + ', ' + city['province'], 'source': origin})
    post = (FR_POST_PATH if fr else POST_PATH) + query
    cost = (FR_COST_PATH if fr else COST_PATH) + query
    heading = f'Dépoussiérage après construction à {name}' if fr else f'Post-construction high dusting in {name}'
    cost_heading = f'Prix du dépoussiérage en hauteur à {name}' if fr else f'High dusting costs in {name}'
    note = FR_COST_NOTES[city['focus']] if fr else COST_NOTES[city['focus']]
    return (f'<section class="section local-planning" id="post-construction"><div class="container planning-grid">'
            f'<article class="planning-card"><div class="eyebrow">{"Après les travaux" if fr else "Builds & renovations"}</div><h2>{heading}</h2>'
            f'<p>{e(CITY_HANDOVERS[city["slug"]])}</p><a class="text-link" href="{e(post)}">{"Voir le service après construction" if fr else "Explore post-construction cleaning"} ↗</a></article>'
            f'<article class="planning-card" id="cost"><div class="eyebrow">{"Préparer le budget" if fr else "Planning your budget"}</div><h2>{cost_heading}</h2>'
            f'<p>{e(note)}</p><p>{"Une courte description et votre ville suffisent pour commencer. Les détails techniques peuvent être précisés lors du suivi." if fr else "Start with your city and a short description. We can discuss measurements, access and timing during follow-up."}</p>'
            f'<a class="text-link" href="{e(cost)}">{"Lire le guide des prix" if fr else "Read the cost guide"} ↗</a></article></div></section>')


def resource_links(fr=False):
    return (f'<div class="resource-links"><a href="{FR_POST_PATH if fr else POST_PATH}">{"Dépoussiérage après construction" if fr else "Post-construction high dusting"} ↗</a>'
            f'<a href="{FR_COST_PATH if fr else COST_PATH}">{"Guide des prix" if fr else "High dusting cost guide"} ↗</a></div>')


def post_details(fr=False):
    if fr:
        title='Une remise des lieux bien préparée.'
        steps=[('Définir les surfaces','Identifiez les poutres, les conduits extérieurs, les rebords et les luminaires à nettoyer. Distinguez les dépôts de chantier des résidus déjà présents.'),('Convenir du moment','Planifiez après les travaux poussiéreux et avant l’installation des marchandises, lorsque cela est possible. Confirmez les zones libérées par les autres corps de métier.'),('Préciser la remise','Convenez des protections, des exclusions et des critères de fin de travaux. Toute visite après des retouches du chantier se prévoit séparément.')]
        note='Le service vise les surfaces en hauteur accessibles. Le ramassage de gros débris, le nettoyage complet des sols ou des vitres, l’intérieur des conduits et le traitement des matières dangereuses nécessitent une portée distincte.'
    else:
        title='A clearer handover starts overhead.'
        steps=[('Define the surfaces','List beams, duct exteriors, ledges and fixture housings to clean. Distinguish construction deposits from any material already present in the facility.'),('Agree the timing','Plan after dust-producing trades and before stock moves in where practical. Confirm which zones the contractor has released and whether other trades will return.'),('Set the handover scope','Agree protection, exclusions and completion criteria. Any return visit after contractor touch-ups should be planned and priced separately.')]
        note='This service covers accessible overhead surfaces. Bulk debris removal, complete floor or glass cleaning, internal duct cleaning and hazardous-material treatment require a separate scope.'
    return '<section class="section"><div class="container"><h2>'+title+'</h2><div class="planning-grid planning-three">'+''.join('<article class="planning-card"><h3>'+h+'</h3><p>'+p+'</p></article>' for h,p in steps)+'</div><p class="planning-note">'+note+'</p>'+resource_links(fr)+'</div></section>'


def cost_article(fr=False):
    if fr:
        title='Combien coûte le dépoussiérage en hauteur?'
        intro='Le prix dépend des surfaces à nettoyer, de leurs accès et des conditions du site. Une superficie au sol ou un tarif au pied carré ne suffit pas à décrire tous les travaux. Ce guide vous aide à préparer votre demande et à comparer des soumissions portant sur les mêmes surfaces.'
        rows=[('Surfaces incluses','Longueur et densité des poutres, conduits, rebords et luminaires.','Une liste des zones et quelques photos prises vers le haut.'),('Hauteur et accès','Portée nécessaire, largeur des passages et nombre de mises en place.','Photos des entrées, des allées et des obstacles.'),('Dépôts et matériaux','Nature de la poussière et compatibilité des surfaces.','Informations disponibles sur les matériaux et les revêtements.'),('Protection et occupation','Marchandises, équipements sensibles et activités sous la zone.','Ce qui peut être déplacé, couvert ou isolé.'),('Horaires et visites','Zones libérées, travaux par étapes et visites de retour.','Périodes possibles et contraintes de remise des lieux.'),('Lieu et mobilisation','Livraison des équipements, accès au site et déplacements.','Ville, adresse et renseignements sur la réception.')]
        compare='Comparer des soumissions équivalentes'
        bullets=['Même liste de surfaces et mêmes exclusions.','Équipements, livraison, protections et déplacements clairement indiqués.','Horaires, nombre de visites et responsabilités du site précisés.','Critères de fin de travaux et traitement des retouches convenus.','Taxes et modalités de paiement précisées dans la soumission.']
        example='Deux entrepôts de même superficie peuvent présenter des accès très différents : l’un vide avec des allées dégagées, l’autre occupé avec des rayonnages serrés et des horaires limités. Le temps de mise en place et de protection peut donc différer, même si la surface au sol est identique.'
        after='Après construction ou entretien récurrent?'
        after_text='Après construction, la fin des travaux poussiéreux et l’ordre de remise des zones influencent le calendrier. Pour un entretien récurrent, les dépôts observés et l’activité du site servent à définir la fréquence. Il n’existe pas de remise ou d’intervalle universel à appliquer à tous les établissements.'
        cta='Commencez par votre ville et une courte description. Les mesures, les photos et les détails d’accès pourront être précisés lors du suivi. Le prix et la disponibilité sont confirmés pour votre projet.'
        labels=('Facteur','Pourquoi il compte','Renseignements utiles')
    else:
        title='How much does high dusting cost?'
        intro='High dusting is quoted around the surfaces to clean, the access needed and the conditions at your facility. Floor area or a square-foot rate alone cannot describe every overhead project. Use this guide to prepare a request and compare quotes for an equivalent scope.'
        rows=[('Surfaces included','Length and density of beams, ducts, ledges and fixtures.','A list of work areas and a few upward-looking photos.'),('Height and access','Required reach, clearances and number of equipment setups.','Photos of entrances, aisles and obstructions.'),('Deposits and materials','Dust characteristics and compatibility with surface finishes.','Available information about deposits and materials.'),('Protection and occupancy','Stock, sensitive equipment and activity beneath the work.','What can be moved, covered or isolated.'),('Timing and visits','Released work areas, phasing and return visits.','Possible working windows and handover constraints.'),('Location and mobilisation','Equipment delivery, site access and travel arrangements.','Your city, facility address and receiving information.')]
        compare='Compare the same scope, not just the total'
        bullets=['Match the included surfaces and exclusions in each quote.','Check whether equipment, delivery, protection and mobilisation are included.','Confirm working hours, number of visits and the site team’s responsibilities.','Agree completion criteria and how contractor touch-ups or return visits are handled.','Check the stated taxes and payment terms.']
        example='Two warehouses with the same floor area can have very different access: one empty with clear aisles, the other occupied with dense racking and restricted work windows. Setup and protection time can differ even when the square footage is identical.'
        after='Post-construction or recurring maintenance?'
        after_text='After construction, the completion of dust-producing trades and the order of zone handovers affect scheduling. For recurring maintenance, observed deposits and facility activity help define the interval. A universal discount or cleaning frequency would not reflect every building.'
        cta='Start with your city and a short description. Measurements, photos and access details can follow in the conversation. Pricing and availability are confirmed for your specific project.'
        labels=('Cost factor','Why it matters','Helpful information')
    return ('<section class="section"><div class="container guide-content"><h2>'+title+'</h2><p class="guide-lead">'+intro+'</p>'
            '<div class="cost-table-wrap"><table class="cost-table"><caption>'+('Les principaux facteurs du devis' if fr else 'The main factors behind a high dusting quote')+'</caption><thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in labels)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+row[0]+'</th><td>'+row[1]+'</td><td>'+row[2]+'</td></tr>' for row in rows)+'</tbody></table></div>'
            '<div class="scope-note"><h3>'+('Pourquoi la superficie ne suffit pas' if fr else 'Why floor area is only a starting point')+'</h3><p>'+example+'</p></div>'
            '<h2>'+compare+'</h2><ul>'+''.join('<li>'+x+'</li>' for x in bullets)+'</ul><h2>'+after+'</h2><p>'+after_text+'</p>'+resource_links(fr)+'<p>'+cta+'</p><a class="btn dark" href="#quote">'+('Demander une soumission' if fr else 'Request a quote')+' ↗</a></div></section>')
