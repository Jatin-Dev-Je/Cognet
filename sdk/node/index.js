async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  const body = text ? JSON.parse(text) : {};

  if (!response.ok) {
    const detail = body?.detail || body?.message || response.statusText;
    throw new Error(detail);
  }

  return body;
}

class Cognet {
  constructor(apiKey, options = {}) {
    this.apiKey = apiKey || options.apiKey || process.env.COGNET_API_KEY || "";
    this.baseUrl = options.baseUrl || process.env.COGNET_API_URL || "http://localhost:8000/api/v1";
  }

  async send(message) {
    return requestJson(`${this.baseUrl}/chat`, {
      method: "POST",
      body: JSON.stringify({ message }),
      headers: this.apiKey
        ? {
            Authorization: `Bearer ${this.apiKey}`,
          }
        : {},
    });
  }

  async next() {
    return this.send("what should I do next?");
  }
}

module.exports = Cognet;