import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import gql from 'graphql-tag';

// Mock booking data
const bookings = [
  { id: '1', userId: 'user1', hotelId: '1', promoCode: 'SUMMER10', discountPercent: 10 },
  { id: '2', userId: 'user1', hotelId: '3', promoCode: null, discountPercent: 0 },
  { id: '3', userId: 'user2', hotelId: '2', promoCode: 'WINTER15', discountPercent: 15 },
  { id: '4', userId: 'user1', hotelId: '4', promoCode: 'VIP20', discountPercent: 20 },
  { id: '5', userId: 'user3', hotelId: '5', promoCode: null, discountPercent: 0 }
];

const typeDefs = gql`
  type Booking @key(fields: "id") {
    id: ID!
    userId: String!
    hotelId: String!
    hotel: Hotel
    promoCode: String
    discountPercent: Int
  }

  type Hotel @key(fields: "id") {
    id: ID!
  }

  type Query {
    bookingsByUser(userId: String!): [Booking]
  }
`;

const resolvers = {
  Query: {
    bookingsByUser: async (_, { userId }, { req }) => {
      // ACL: Check if user is authorized by checking userid header
      const requestUserId = req.headers['userid'];

      if (!requestUserId) {
        throw new Error('Unauthorized: userid header is required');
      }

      // Only return bookings for the requesting user or if they match the requested userId
      if (requestUserId !== userId) {
        throw new Error('Forbidden: You can only access your own bookings');
      }

      // Filter bookings by userId
      return bookings.filter(booking => booking.userId === userId);
    },
  },
  Booking: {
    __resolveReference: async ({ id }, { req }) => {
      // ACL: Check if user is authorized
      const requestUserId = req.headers['userid'];

      if (!requestUserId) {
        return null; // Don't throw error, just return null for federation
      }

      const booking = bookings.find(b => b.id === id);

      // Only return booking if it belongs to the requesting user
      if (booking && booking.userId === requestUserId) {
        return booking;
      }

      return null;
    },
    hotel: async (booking) => {
      // Return a reference to the hotel, Apollo Federation will resolve it
      return { __typename: 'Hotel', id: booking.hotelId };
    }
  },
};

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});

startStandaloneServer(server, {
  listen: { port: 4001 },
  context: async ({ req }) => ({ req }),
}).then(() => {
  console.log('✅ Booking subgraph ready at http://localhost:4001/');
});
