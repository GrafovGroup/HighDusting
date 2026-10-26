"""Visible buyer questions, edited for the actual boundaries of each service."""
from html import escape
from niche_services import ANSWERS as NICHE_ANSWERS

ANSWERS = {
    'post-construction-high-dusting': ('When should overhead cleaning happen after construction?', 'Plan the overhead clean after dust-producing trades have finished and the contractor has released the work areas. Where practical, clean before stock and sensitive equipment move in. Agree any later touch-ups or return visits separately.'),
    'commercial-high-dusting': ('Can high dusting be planned around customers?', 'Customer hours, deliveries and the areas below the work all affect scheduling. Identify when public access can be controlled and which displays or finished surfaces need protection. The service window is agreed during scoping.'),
    'industrial-high-dusting': ('What information matters for industrial dust removal?', 'Identify the process that produces the dust, known materials and any site restrictions. Include machinery, cranes and conveyors that obstruct access. Potentially hazardous or combustible materials require separate assessment before a method is proposed.'),
    'warehouse-high-dusting': ('Is warehouse floor area enough to price high dusting?', 'Floor area is a starting point. The amount of overhead steelwork, racking layout, ceiling height, aisle clearance and stock protection also affect the work. Include photos looking up and along the working aisles so access can be assessed.'),
    'ceiling-cleaning': ('Which ceiling surfaces should I include in the request?', 'List the ceiling structures, ledges, fixtures and other overhead surfaces you want addressed. Identify fragile finishes and obstructions. The agreed scope specifies the accessible surfaces and a method suited to their materials and dust conditions.'),
    'rafter-beam-cleaning': ('Does the scope include trusses and structural connections?', 'Rafters, joists, trusses, beams and their accessible connections can be considered together. Photographs of the structure help define the surfaces, reach and obstructions. The quote confirms which areas are included.'),
    'pipe-conduit-cleaning': ('Does pipe cleaning include work on the systems themselves?', 'The scope concerns accessible exterior surfaces. Identify sensitive systems and any required isolation with your facility team. Work near sprinklers and other overhead services is assessed against their protection requirements.'),
    'duct-exterior-cleaning': ('Is duct exterior cleaning the same as internal duct cleaning?', 'No. Duct exterior cleaning removes settled dust from accessible surfaces outside exposed ductwork. Internal duct cleaning, HVAC servicing and changes to ventilation equipment are outside this service scope.'),
    'hepa-high-dusting': ('Does HEPA filtration make equipment suitable for every dust type?', 'No. Filtration alone does not establish equipment suitability for hazardous or combustible dust. Dust characteristics and site conditions must be assessed before selecting a vacuum system or proposing a cleaning method.'),
    'food-facility-high-dusting': ('How is overhead work coordinated in a food facility?', 'Your sanitation and quality teams help define product protection, hygiene requirements and the cleaning window. Identify open-product, packaging and storage areas separately. The scope and sequence are assessed against those site requirements.'),
    'manufacturing-high-dusting': ('Can manufacturing overhead cleaning be phased?', 'Phasing depends on the machinery layout, dust, access restrictions and whether work zones can be released. Share production and maintenance windows so the scope can be assessed for phased work or a planned shutdown.'),
    'high-level-cobweb-removal': ('Does high-level cobweb removal include pest treatment?', 'No. This scope addresses cobwebs on accessible elevated corners, ledges, roof structures and fixtures. Pest treatment is separate. Cobweb removal can be included in a broader overhead cleaning request.'),
    'elevated-fixture-cleaning': ('Does fixture cleaning include electrical repairs?', 'The proposed cleaning scope concerns accessible exterior surfaces of lighting housings, signs and suspended fixtures. Identify delicate finishes and any site-controlled isolation requirements. Equipment servicing and electrical repairs are separate from surface cleaning.'),
    'ceiling-fan-cleaning': ('What details are needed for high ceiling fan cleaning?', 'Include the fan height, diameter, manufacturer information and the activity below each fan. Access, compatible cleaning methods and equipment isolation need to be considered before blade and exterior surface cleaning is agreed.'),
    'equipment-exterior-cleaning': ('Does equipment exterior cleaning include internal maintenance?', 'This scope addresses accessible exterior surfaces and equipment tops. Internal maintenance is separate. Identify openings, sensors, delicate components and the equipment owner’s isolation and protection requirements in the request.'),
    'shutdown-cleaning': ('What should be agreed before a shutdown clean?', 'Define the available outage window, when work areas are released, other trades, equipment protection and the handover requirements. These details help establish a cleaning sequence within the facility’s maintenance plan.'),
    'recurring-overhead-maintenance': ('How often should high dusting be scheduled?', 'There is no single interval for every facility. A recurring scope considers observed buildup, operations and access windows. Review points allow the frequency and areas included to change as facility conditions change.'),
}

ANSWERS.update(NICHE_ANSWERS)

def render(slug):
    questions = [ANSWERS[slug],
        ('What affects the cost of this service?', 'The quote depends on the surfaces and extent of work, ceiling height, dust conditions, access equipment, protection requirements and available work windows. Share the facility location and photos to help define the scope; a site visit may be needed.'),
        ('How do I request a quote for my facility?', 'Start with your name, email, city and a short description of what needs cleaning. Phone and photos are optional. We can discuss measurements, access and timing during follow-up; availability and methods are confirmed for your project.')]
    return ('<section class="section faq service-answers" id="service-questions"><div class="container faq-layout">'
            '<div><div class="eyebrow">Before you request a quote</div><h2>Your scope.<br>Clear answers.</h2>'
            '<p>Use these details to prepare a facility-specific request.</p></div><div>'
            + ''.join(f'<details open><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in questions)
            + '<div class="resource-links"><a href="/guides/high-dusting-cost/">Read the high dusting cost guide ↗</a><a href="#quote">Request your facility quote ↗</a></div></div></div></section>')
