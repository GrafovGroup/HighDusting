/* Shared Formspree AJAX transport. The browser creates the multipart boundary. */
globalThis.sendQuoteRequest = async function (endpoint, data, request = fetch) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 40000);
  try {
    const response = await request(endpoint, {
      method: 'POST', body: data, headers: {Accept: 'application/json'},
      signal: controller.signal
    });
    const result = await response.json().catch(() => null);
    if (!response.ok || !result || result.ok === false || result.errors?.length || result.error) {
      const error = new Error('submission_failed');
      error.status = response.status;
      error.fields = Array.isArray(result?.errors)
        ? result.errors.map(item => item.field).filter(field => typeof field === 'string') : [];
      throw error;
    }
    return result;
  } finally {
    clearTimeout(timeout);
  }
};
