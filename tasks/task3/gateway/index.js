import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { ApolloGateway, RemoteGraphQLDataSource } from '@apollo/gateway';

class AuthenticatedDataSource extends RemoteGraphQLDataSource {
  willSendRequest({ request, context }) {
    // Forward all headers from the original request
    if (context.req && context.req.headers) {
      Object.keys(context.req.headers).forEach(key => {
        request.http.headers.set(key, context.req.headers[key]);
      });
    }
  }
}

const gateway = new ApolloGateway({
  serviceList: [
    { name: 'booking', url: 'http://booking-subgraph:4001' },
    { name: 'hotel', url: 'http://hotel-subgraph:4002' }
  ],
  buildService({ url }) {
    return new AuthenticatedDataSource({ url });
  }
});

const server = new ApolloServer({ gateway, subscriptions: false });

startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async ({ req }) => ({ req }), // headers пробрасываются
}).then(({ url }) => {
  console.log(`🚀 Gateway ready at ${url}`);
});
