const french = document.documentElement.lang.startsWith('fr');
const translations = {
'Please complete this field.':'Veuillez remplir ce champ.',
'Please select no more than 5 files.':'Veuillez choisir un maximum de 5 fichiers.',
'Each file must be 10 MB or smaller.':'Chaque fichier doit faire 10 Mo ou moins.',
'Please use JPG, PNG, WebP, MP4 or MOV files.':'Utilisez des fichiers JPG, PNG, WebP, MP4 ou MOV.',
'Too many requests. Please wait a few minutes or call us.':'Trop de demandes. Veuillez patienter quelques minutes ou nous appeler.',
'Up to 5 files, 10 MB each. JPG, PNG, WebP, MP4 or MOV.':'Jusqu’à 5 fichiers de 10 Mo. JPG, PNG, WebP, MP4 ou MOV.'
};
const tr = text => french ? (translations[text] || text) : text;
const menu = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  menu.setAttribute('aria-label', open ? (french ? 'Fermer le menu' : 'Close menu') : (french ? 'Ouvrir le menu' : 'Open menu'));
  menu.textContent = open ? '×' : '☰';
  navigation.classList.toggle('open', open);
});
navigation?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
  menu.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-label', french ? 'Ouvrir le menu' : 'Open menu'); menu.textContent = '☰'; navigation.classList.remove('open');
}));
document.addEventListener('keydown', e => {if(e.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true'){menu.click();menu.focus();}});
const form = document.querySelector('#quote-form');
if (form) {
  let submitting = false;
  const mobileQuoteLink = document.querySelector('.mobile-cta');
  if (mobileQuoteLink && 'IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      mobileQuoteLink.hidden = entry.isIntersecting;
    }).observe(form);
  }
  const error = form.querySelector('#form-error');
  const submit = form.querySelector('#form-submit');
  const submitLabel = submit.innerHTML;
  const fallback = document.createElement('p');
  fallback.hidden = true;
  fallback.className = 'form-hint';
  const fallbackLink = document.createElement('a');
  fallbackLink.href = 'mailto:info@highdusting.ca?subject=HighDusting.ca%20quote%20request';
  fallbackLink.textContent = french ? 'Envoyez votre demande et vos fichiers à info@highdusting.ca' : 'Email your request and attachments to info@highdusting.ca';
  fallback.append(fallbackLink);
  error.after(fallback);
  const showError = message => {error.textContent = tr(message);error.hidden = false;};
  function validateForm() {
    for (const field of form.querySelectorAll('input,textarea')) {
      if (field.type === 'hidden' || field.name === '_gotcha') continue;
      if (field.required && field.type !== 'checkbox' && !field.value.trim()) {
        field.setCustomValidity(tr('Please complete this field.'));
        field.reportValidity();field.setCustomValidity('');return false;
      }
      if (!field.reportValidity()) return false;
    }
    return true;
  }
  document.querySelectorAll('button[data-city]').forEach(button => button.addEventListener('click', () => {
    if(button.dataset.city !== 'Other locations') {
      form.elements.city.value = button.dataset.city;
      form.elements.city.dispatchEvent(new Event('input'));
    }
    document.querySelector('#quote').scrollIntoView({behavior:'smooth'});
    form.elements.city.focus({preventScroll:true});
  }));
  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (submitting || !validateForm()) return;
    form.elements.selected_city.value = form.elements.city.value.trim();
    const data = new FormData(form);
    // Attachments are emailed separately; this endpoint does not permit uploads.
    data.delete('photos');
    data.set('language', french ? 'fr-CA' : 'en-CA');
    submitting = true;
    form.setAttribute('aria-busy','true');
    [...form.elements].forEach(field => field.disabled = true);
    submit.textContent = french ? 'Envoi en cours…' : 'Sending your request…';
    error.hidden = true;
    try {
      await sendQuoteRequest(form.action, data);
      form.replaceChildren();
      const success = document.createElement('div');success.className = 'quote-success';success.setAttribute('role','status');
      const heading=document.createElement('h3');heading.textContent=french ? 'Votre demande a été reçue.' : 'Your request has been received.';
      const text=document.createElement('p');text.textContent=french ? 'Merci. Nous communiquerons avec vous pour discuter de votre projet.' : 'Thank you. We’ll be in touch to discuss your project.';
      const phone=document.createElement('a');phone.href='tel:+18884513878';phone.className='btn dark';phone.textContent=french ? 'Appeler le (888) 451 - DUST (3878) ↗' : 'Call (888) 451 - DUST (3878) ↗';
      const email = document.createElement('a');email.href='mailto:info@highdusting.ca?subject=HighDusting.ca%20project%20photos';email.className='quote-email';email.textContent=french ? 'Envoyer vos photos à info@highdusting.ca' : 'Email project photos to info@highdusting.ca';
      success.append(heading,text,phone,email);form.append(success);success.tabIndex=-1;success.focus();
    } catch (err) {
      [...form.elements].forEach(field => field.disabled = false);
      const invalid = (err.fields || []).map(name => form.elements.namedItem(name)).find(field => field?.matches('input:not([type="hidden"]):not(.form-honeypot),textarea'));
      let message = french ? 'Impossible de confirmer l’envoi. Vos renseignements sont conservés dans ce formulaire. Réessayez ou appelez le (888) 451 - DUST (3878).' : 'We couldn’t confirm your submission. Your details are still in this form. Try again or call (888) 451 - DUST (3878).';
      if (invalid) message = french ? 'Veuillez vérifier le champ indiqué et réessayer.' : 'Please check the highlighted field and try again.';
      if (err.status === 429) message = tr('Too many requests. Please wait a few minutes or call us.');
      if (err.status === 413) message = french ? 'Les fichiers sont trop volumineux pour cet envoi. Choisissez des fichiers plus petits ou appelez-nous.' : 'The attachments are too large to send. Choose smaller files or call us.';
      showError(message);
      fallback.hidden = false;
      if (!invalid) { error.tabIndex = -1; error.focus(); }
      if (invalid) {
        const disclosure = invalid.closest('details');
        if (disclosure) disclosure.open = true;
        invalid.setAttribute('aria-invalid','true');invalid.focus();
        invalid.addEventListener('input',()=>invalid.removeAttribute('aria-invalid'),{once:true});
      }
      submit.innerHTML = submitLabel;
      submitting = false;
    } finally {
      form.removeAttribute('aria-busy');
    }
  });
}

// Page-specific quote context is submitted with the facility details.
const quoteParams = new URLSearchParams(location.search);
if (form) {
  const city = form.dataset.city || quoteParams.get('city') || '';
  const service = form.dataset.service || quoteParams.get('service') || '';
  const originatingPage = quoteParams.get('source');
  if (city) form.elements.city.value = city.slice(0,120);
  form.elements.selected_city.value = city.slice(0,120);
  form.elements.selected_service.value = service.slice(0,120);
  form.elements.source_page.value = location.pathname;
  form.elements.originating_page.value = originatingPage?.startsWith('/') && !originatingPage.startsWith('//') ? originatingPage.slice(0,512) : location.pathname;
  const serviceLabels = JSON.parse(document.querySelector('#service-labels')?.textContent || '{}');
  const context = document.querySelector('#quote-context');
  const isFrench = form.dataset.language === 'fr';
  const updateContext = () => {
    const selection = [form.elements.city.value,serviceLabels[form.elements.selected_service.value] || form.elements.selected_service.value.replaceAll('-',' ')].filter(Boolean);
    context.hidden = !selection.length;
    context.textContent = `${isFrench ? 'Votre demande' : 'Your enquiry'}: ${selection.join(' · ')}`;
  };
  updateContext();
  form.elements.city.addEventListener('input',()=>{form.elements.selected_city.value=form.elements.city.value;updateContext();});
  document.querySelectorAll('[data-service-choice]').forEach(link=>link.addEventListener('click',()=>{
    if(form.elements.selected_service){form.elements.selected_service.value=link.dataset.serviceChoice;updateContext();}
  }));
}

const searchForm = document.querySelector('#location-search');
if (searchForm) {
  const query=document.querySelector('#location-query');
  const province=document.querySelector('#location-province');
  const resultBox=document.querySelector('#location-results');
  const status=document.querySelector('#location-status');
  const more=document.querySelector('#location-more');
  let directory=null, filtered=[], visible=0, timer;
  const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replaceAll('’',"'").toLowerCase();
  query.value=quoteParams.get('q') || '';province.value=quoteParams.get('province') || '';
  function paint(reset=true){
    if(reset){resultBox.replaceChildren();visible=0;}
    resultBox.hidden=false;
    for(const place of filtered.slice(visible,visible+48)){
      const a=document.createElement('a');a.className='location-result';a.href=place.url;
      const name=document.createElement('strong');name.textContent=place.name;
      const region=document.createElement('span');region.textContent=[place.province,place.division].filter(Boolean).join(' · ');
      const action=document.createElement('small');action.textContent=place.featured?'Explore local services ↗':'Request an assessment here ↗';
      a.append(name,region,action);resultBox.append(a);
    }
    visible=Math.min(visible+48,filtered.length);more.hidden=visible>=filtered.length;
    status.textContent=`${filtered.length.toLocaleString('en-CA')} location${filtered.length===1?'':'s'} found · Showing ${visible.toLocaleString('en-CA')}`;
    if(!filtered.length){
      const empty=document.createElement('div');empty.className='empty-locations';
      const text=document.createElement('p');text.textContent='No matching community in the directory. You can still request an assessment for your address.';
      const link=document.createElement('a');link.className='btn';link.textContent='Use this location ↗';link.href='/?'+new URLSearchParams({city:query.value+(province.value?', '+province.value:''),source:'/locations/'})+'#quote';
      empty.append(text,link);resultBox.append(empty);
    }
  }
  async function search(){
    more.hidden=true;
    try{
      if(!directory){status.textContent='Loading Canadian locations…';const response=await fetch('/assets/locations.json');if(!response.ok)throw new Error();directory=await response.json();}
      const term=normalize(query.value.trim());
      filtered=directory.filter(p=>(!province.value||p.province===province.value)&&(!term||normalize(p.name).includes(term)));
      filtered.sort((a,b)=>Number(b.featured)-Number(a.featured)||a.name.localeCompare(b.name,'en-CA')||a.province.localeCompare(b.province));
      paint();
    }catch{status.textContent='The directory could not load. Try searching again, browse a province below, or enter your city in the quote form.';}
  }
  searchForm.addEventListener('submit',event=>{event.preventDefault();clearTimeout(timer);search();});
  query.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(search,180);});
  province.addEventListener('change',search);more.addEventListener('click',()=>paint(false));
  if(query.value||province.value)search();
}
