// No outbound requests: exercise the production transport with mocked responses.
const assert = require('node:assert/strict');
const test = require('node:test');
require('./formspree.js');
const endpoint = 'https://formspree.io/f/mqpkndrp';

test('sends multipart fields and multiple attachments to the configured endpoint', async () => {
  const data = new FormData();
  data.set('email', 'test@example.com');
  data.set('city', 'Montréal, QC');
  data.set('source_page', '/locations/quebec/montreal/');
  data.set('selected_service', 'rafter-beam-cleaning');
  data.append('photos', new Blob(['test image'], {type:'image/jpeg'}), 'overhead.jpg');
  data.append('photos', new Blob(['test video'], {type:'video/mp4'}), 'access.mp4');
  let calls = 0;
  const result = await sendQuoteRequest(endpoint, data, async (url, init) => {
    calls++;
    assert.equal(url, endpoint);
    assert.equal(init.method, 'POST');
    assert.deepEqual(init.headers, {Accept:'application/json'});
    assert.equal(init.body, data);
    assert.equal(init.body.get('email'), 'test@example.com');
    assert.equal(init.body.get('city'), 'Montréal, QC');
    assert.equal(init.body.get('selected_service'), 'rafter-beam-cleaning');
    assert.deepEqual(init.body.getAll('photos').map(file => file.name), ['overhead.jpg', 'access.mp4']);
    return new Response(JSON.stringify({ok:true}), {status:200});
  });
  assert.deepEqual(result, {ok:true});
  assert.equal(calls, 1);
});

test('exposes provider validation fields without treating errors as success', async () => {
  await assert.rejects(sendQuoteRequest(endpoint, new FormData(), async () =>
    new Response(JSON.stringify({errors:[{field:'email',message:'Invalid email'}, {message:'Missing data'}]}), {status:422})),
    error => error.status === 422 && error.fields.length === 1 && error.fields[0] === 'email');
  await assert.rejects(sendQuoteRequest(endpoint, new FormData(), async () =>
    new Response(JSON.stringify({ok:false,error:'Not accepted'}), {status:200})));
});

test('HTTP limits, HTML error pages, and invalid JSON never report success', async () => {
  for (const status of [403,413,429,500]) {
    await assert.rejects(sendQuoteRequest(endpoint, new FormData(), async () =>
      new Response('<html>Unavailable</html>', {status})), error => error.status === status);
  }
  await assert.rejects(sendQuoteRequest(endpoint, new FormData(), async () =>
    new Response('<html>Not a submission receipt</html>', {status:200})));
});

test('network failure preserves payload and does not automatically resubmit', async () => {
  const data = new FormData();data.set('company','Test company');
  let calls = 0;
  await assert.rejects(sendQuoteRequest(endpoint, data, async () => {calls++;throw new TypeError('Failed to fetch');}));
  assert.equal(calls, 1);
  assert.equal(data.get('company'), 'Test company');
});
