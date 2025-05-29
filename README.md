# Anti-Rieltor Flat Trade Platform

- Full-scale platform which users can use to see, analyze and trade flats without rieltors
  
  According to this aim system must have the same requirements:
  - Good auth and authorization system
  - Antifrod rieltor system
  - DDoS defence functionality
  - Static parameters using which we can analyze current market
  - Platform for trading and rent flats with maximum account

## System description and main parts: 
  - Analyzis platform where users can see and read analysis about real estate market in certain cities 
  - Platform to trade flats, alghoritm which gives user the most prefered flat to buy
  - Rieltor antifrod system
  - Posibility to wtite to lessor on platform via chat

  Firstly we must do analysis platform as MVP to deliver actual data about real estate market in certain city of Ukraine. Also it must deliver top-offers in certain area and cities

## Функціонал торгової площадки

Об'єкти квартир, їх можна відкрити подивитись і т.п. Також можна на сторінці знайти контакти продавця, загалом мають бути фільтри по району, ціні, кількості кімнат і т.п. також можна додатии коючові слова по квартирі і фільтрувати по ним наприклад, якщо юзер вибрав опцію персоналізований пошук і т.п.

Апішки які треба для створення торгової платформи

**GET-запити**
```
flats/<city> #повертає всі квартири по указаному місту, також в залежності від параметрів має повертати квартири в певному ціновому діапазоні і т.п.
```
**POST-запити**
```
flats/<city> - створення квартири та запис в БД
```
**PATCH-запит**
```
Для редагування інформації про квартиру
```
**DELETE-запит**
```
Для видалення квартири
```
Об'єкт квартири в предметній області
```

```