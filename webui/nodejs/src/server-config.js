export const config =
{
  "port": process.env.WEBUI_PORT, // Port the webserver listens on
  "restApiBaseUrl": `http://${process.env.API_BASE_URL}`, // Address with port of the REST API server
  "restApiAdminKey": process.env.ADMIN_API_KEY, // Admin key for the REST API server
  "restApiWebSocketUrl": `ws://${process.env.API_BASE_URL}/ws/events/`, // WebSocket URL of the REST API server
};
