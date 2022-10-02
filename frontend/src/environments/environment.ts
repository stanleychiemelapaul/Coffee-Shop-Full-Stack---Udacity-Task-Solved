/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-c1v0nd71.us', // the auth0 domain prefix
    audience: 'coffeeshopapi', // the audience set for the auth0 app
    clientId: 'AutGjYRzwbQbqNgeBycYqsMgYVVCEZIx', // the client id generated for the auth0 app
    callbackURL: 'https://127.0.0.1:8100', // the base url of the running ionic application.
  }
};
