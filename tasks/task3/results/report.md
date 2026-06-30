# Сделанные изменения

1. Hotel Subgraph (hotel-subgraph/index.js)

- Добавлены mock данные: 5 отелей с реалистичной информацией
- Реализован __resolveReference: Резолвинг отелей по ID для Federation
- Реализован hotelsByIds: Query для получения отелей по массиву ID

2. Booking Subgraph (booking-subgraph/index.js)

- Добавлены mock данные: 5 бронирований для разных пользователей
- Реализован bookingsByUser с ACL: проверка заголовка userid, авторизация доступа только к собственным бронированиям
- Реализован __resolveReference с ACL: Резолвинг бронирований с контролем доступа
- Добавлена связь с Hotel: Federation reference для получения данных об отелях

3. Gateway (gateway/index.js)

- Исправлена передача заголовков: Реализован AuthenticatedDataSource для проброса всех заголовков в subgraph
- Настроена Federation: Правильная конфигурация для работы с двумя subgraph
