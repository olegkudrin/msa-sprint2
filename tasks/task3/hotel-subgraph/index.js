import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import gql from 'graphql-tag';

// Mock hotel data
const hotels = [
  { id: '1', name: 'Grand Hotel Moscow', city: 'Moscow', stars: 5 },
  { id: '2', name: 'Hotel Europe', city: 'St. Petersburg', stars: 4 },
  { id: '3', name: 'Radisson Blu', city: 'Moscow', stars: 4 },
  { id: '4', name: 'Astoria Hotel', city: 'St. Petersburg', stars: 5 },
  { id: '5', name: 'Metropol Hotel', city: 'Moscow', stars: 5 }
];

const typeDefs = gql`
  type Hotel @key(fields: "id") {
    id: ID!
    name: String
    city: String
    stars: Int
  }

  type Query {
    hotelsByIds(ids: [ID!]!): [Hotel]
  }
`;

const resolvers = {
  Hotel: {
    __resolveReference: async ({ id }) => {
      // Find hotel by ID from mock data
      const hotel = hotels.find(h => h.id === id);
      return hotel || null;
    },
  },
  Query: {
    hotelsByIds: async (_, { ids }) => {
      // Filter hotels by provided IDs
      return hotels.filter(hotel => ids.includes(hotel.id));
    },
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

startStandaloneServer(server, {
  listen: { port: 4002 },
}).then(() => {
  console.log('✅ Hotel subgraph ready at http://localhost:4002/');
});
