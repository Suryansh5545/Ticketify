/**
 * Environment URL for local development
 */

const apiEndpoint = process.env["API_ENDPOINT"];
const isLocalhost = apiEndpoint === 'http://localhost:8000/api/';

export const environment = {
  production: !isLocalhost, // Set production to true if it's not localhost
  api_endpoint: apiEndpoint || 'http://localhost:8000/api/', // Fallback to localhost if API_ENDPOINT is not set
};

  