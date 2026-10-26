"""Focused overhead services and contextual links, without duplicated photo cards."""
from html import escape as e
from urllib.parse import urlencode

NICHE_SERVICES = [
    ('acoustic-baffle-ceiling-cloud-dusting', 'Acoustic baffle & ceiling cloud dusting',
     'Care for the ceiling features that shape your space.', '',
     'Remove loose surface dust from accessible acoustic baffles and suspended ceiling clouds in offices, restaurants, auditoriums and education buildings. Panel material, finish and suspension details guide the proposed method, with manufacturer care instructions reviewed before work.',
     ['Panel manufacturer, product name and care information where available',
      'Baffle spacing, cloud height and photographs of accessible faces and edges',
      'Furniture, AV equipment and finishes beneath the work area']),
    ('warehouse-rack-top-cleaning', 'Warehouse rack-top cleaning',
     'Reach the rack surfaces above daily operations.', '',
     'Target settled dust on accessible upper pallet-rack beams, cross-members and rack-top surfaces. The scope follows your rack layout, stock locations and aisle-release plan so the surfaces to clean are agreed before equipment and access are arranged.',
     ['Rack rows, bay counts, upper-beam heights and aisle widths',
      'Stock protection or relocation arranged with the warehouse team',
      'Forklift routes, receiving hours and available work zones']),
    ('gymnasium-overhead-cleaning', 'Gymnasium overhead cleaning',
     'Prepare the space above the next game.', '',
     'Plan high dusting for school gyms, sports halls and recreation centres. Include roof trusses, accessible basketball support frames, high ledges and fixture exteriors, with court protection and access scheduled around classes, clubs and facility bookings.',
     ['Ceiling and support-frame heights, with photos from the court',
      'Floor type, floor-care requirements and equipment access route',
      'Booking windows and site-controlled isolation of moving or powered equipment']),
]
NICHE_SLUGS = {s[0] for s in NICHE_SERVICES}
NICHE_IMAGES = {'/assets/services/' + s + '.webp' for s in NICHE_SLUGS}
FR_NICHE = {
    'acoustic-baffle-ceiling-cloud-dusting': 'Dépoussiérage des baffles et îlots acoustiques',
    'warehouse-rack-top-cleaning': 'Nettoyage du haut des palettiers',
    'gymnasium-overhead-cleaning': 'Nettoyage en hauteur des gymnases',
}
FOCUS_SERVICES = {
    'warehouses': ['warehouse-rack-top-cleaning'],
    'retail': ['acoustic-baffle-ceiling-cloud-dusting'],
    'education': ['acoustic-baffle-ceiling-cloud-dusting', 'gymnasium-overhead-cleaning'],
    'arenas': ['gymnasium-overhead-cleaning', 'acoustic-baffle-ceiling-cloud-dusting'],
}
RELATED = {
    'acoustic-baffle-ceiling-cloud-dusting': ['commercial-high-dusting', 'elevated-fixture-cleaning'],
    'warehouse-rack-top-cleaning': ['warehouse-high-dusting', 'rafter-beam-cleaning'],
    'gymnasium-overhead-cleaning': ['ceiling-fan-cleaning', 'elevated-fixture-cleaning'],
}
ANSWERS = {
    'acoustic-baffle-ceiling-cloud-dusting': (
        'Can all acoustic baffles and ceiling clouds be cleaned the same way?',
        'No. Felt, fabric-faced, mineral-fibre and other acoustic products have different care requirements. Provide the product details if available. We assess the material and accessible surfaces against the manufacturer instructions; stain treatment, panel removal and repairs are separate scopes.'),
    'warehouse-rack-top-cleaning': (
        'Does every rack need to be emptied before cleaning?',
        'The stock arrangement and surfaces to reach determine whether goods need to be moved or protected. Agree this by rack row or work zone with the warehouse team. Access equipment, aisle clearance and released forklift routes are confirmed before scheduling.'),
    'gymnasium-overhead-cleaning': (
        'How do you plan access without damaging the gym floor?',
        'The facility team provides floor-care requirements and confirms the access route and equipment restrictions. Floor loading, equipment choice and suitable protection are reviewed before the work. Share the floor type, door clearances and any recent refinishing information with your request.'),
}

DETAILS = {
    'acoustic-baffle-ceiling-cloud-dusting': (
        'Start with the panel, then plan the access.',
        [('Identify the material', 'Share a product reference or close-up photos of the finish, edges and suspension. A method that suits one ceiling product may not suit another.'),
         ('Define reachable surfaces', 'Distinguish vertical baffles from horizontal clouds. Specify which faces and edges can be reached without moving panels or disturbing their suspension.'),
         ('Coordinate the room', 'Identify tables, seating, displays and AV equipment below. Plan a released work area and a cleaning window with the building team.')],
        'This service focuses on loose surface dust. Repainting, stain removal, panel replacement, suspension repairs and claims about restoring acoustic performance are outside the dusting scope.'),
    'warehouse-rack-top-cleaning': (
        'Build the scope by row and bay.',
        [('Map the rack surfaces', 'A row-and-bay list helps distinguish upper rack beams from roof steel, stored goods and mezzanine surfaces. Include photos looking along the upper levels.'),
         ('Agree stock handling', 'Identify exposed products, packaging and areas that need temporary relocation or covering. The warehouse team coordinates stock movements before a zone is released.'),
         ('Sequence the aisles', 'Plan work around picking, replenishment and receiving. Confirm access through the narrowest aisle and allow time for equipment moves between zones.')],
        'Cleaning concerns agreed accessible rack surfaces. Rack inspection or certification, structural repairs, goods handling and cleaning individual products are separate. Dust from a process or material needs identification before a method is selected.'),
    'gymnasium-overhead-cleaning': (
        'Plan above the court and around the calendar.',
        [('List the overhead areas', 'Identify trusses, high ledges, basketball support frames and light housings separately. Acoustic panels and fans can be included after their care and access requirements are reviewed.'),
         ('Protect the playing surface', 'Share the court finish, equipment restrictions and entrance dimensions. The proposed access and protection plan must suit the facility floor and the route into the gym.'),
         ('Coordinate the handover', 'Agree a work window with the school or recreation team, including equipment setup, removal and floor-protection removal before the next booking.')],
        'This is an overhead surface-cleaning scope. Court refinishing, sports-equipment inspection, electrical servicing and repairs to retractable basketball systems are separate. Moving and powered systems require site-controlled isolation.'),
}


def details(slug):
    heading, steps, note = DETAILS[slug]
    return ('<section class="section niche-details"><div class="container"><div class="section-heading"><h2>' + e(heading)
            + '</h2></div><div class="niche-step-grid">'
            + ''.join('<article><h3>' + e(title) + '</h3><p>' + e(copy) + '</p></article>' for title, copy in steps)
            + '</div><div class="scope-note"><h3>Scope boundaries</h3><p>' + e(note) + '</p></div></div></section>')


def links(focus, city='', origin='', fr=False):
    slugs = FOCUS_SERVICES.get(focus, [])
    if not slugs:
        return ''
    heading = 'Des surfaces à préciser' if fr else 'A more specific cleaning scope'
    intro = ('Pour votre établissement' + (' à ' + city if city else '') + ', précisez ces surfaces dans votre demande. La méthode et les accès sont évalués pour chaque site.') if fr else ('For your facility' + (' in ' + city if city else '') + ', explore the details that affect these specialist scopes.')
    titles = {s[0]: s[1] for s in NICHE_SERVICES}
    anchors = []
    for slug in slugs:
        target = '/services/' + slug + '/'
        if city:
            target += '?' + urlencode({'city': city, 'source': origin})
        if fr:
            anchors.append('<a href="#quote" data-service-choice="' + slug + '">' + e(FR_NICHE[slug]) + ' ↗</a>')
        else:
            anchors.append('<a href="' + e(target) + '">' + e(titles[slug]) + ' ↗</a>')
    return '<section class="section niche-links" id="specialist-surfaces"><div class="container"><h2>' + heading + '</h2><p class="planning-note">' + e(intro) + '</p><div class="resource-links">' + ''.join(anchors) + '</div></div></section>'


def local_links(slug, cities, city_url):
    relevant = [c for c in cities if slug in FOCUS_SERVICES.get(c['focus'], [])]
    anchors = ''.join('<a href="' + city_url(c) + '#specialist-surfaces">' + e(c['name']) + ' ↗</a>' for c in relevant)
    return ('<section class="section"><div class="container"><h2>Plan for your location</h2>'
            '<p class="planning-note">Explore the facility planning notes for your city, or include another location in your quote request. Access, equipment and local availability are confirmed for each project.</p>'
            '<div class="industry-chips">' + anchors + '</div><p class="planning-note"><a class="text-link" href="/locations/">Find another Canadian city ↗</a></p></div></section>')
