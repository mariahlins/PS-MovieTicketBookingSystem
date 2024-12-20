# Movie Ticket Booking System

## Project Overview
Este projeto é um Sistema de Reserva de Ingressos de Cinema abrangente desenvolvido como projeto para matéria de Projeto de Software. O sistema permite que os usuários naveguem por filmes, selecionem assentos e comprem ingressos online, junto com recursos adicionais como avaliações, descontos.

## Features

### 1. User Account Management

### 2. Cinema and Movie Listings

### 3. Real-Time Seat Availability

### 4. Payment Processing

### 5. Booking History and Cancellations

### 6. Promotions and Discounts

### 7. Mobile Ticketing

### 8. Notification and Alerts

### 9. Customer Reviews and Ratings

### 10. Seat Selection and Booking

## Design Patterns

### Template Method - Reserva de Ticket
O padrão Template Method é utilizado no processo de reserva de tickets, onde temos uma estrutura genérica que define a sequência de etapas para realizar a reserva, mas permite que subclasses especifiquem a implementação de alguns passos específicos. Por exemplo, o processo de reserva envolve várias etapas como a seleção de assentos, verificação de disponibilidade e confirmação.

### Strategy - Método de Pagamento
O padrão Strategy é aplicado no processamento de pagamentos, onde diferentes métodos de pagamento (como cartão de crédito, PIX, etc.) são implementados como estratégias intercambiáveis. Cada método de pagamento é encapsulado em uma classe separada que implementa uma interface comum de pagamento. Dessa forma, o sistema permite que o usuário escolha seu método de pagamento preferido, e o processamento é delegado à classe correspondente, garantindo flexibilidade e expansão para novos métodos de pagamento sem modificar o código principal de reserva.

## Observer - Notificação de compra de ticket
O padrão observer é utilizado no processo de reserva de tickets, mais especificamente na confirmação de pagamento do ticket. Após a reserva e pagamento efetuados com sucesso, há um update de evento e um email é enviado para o email cadastrado no perfil do cliente.

## Installation

1. **Clone the Repository**  
   Open your terminal and run the following command to clone the project repository:
   ```bash
   git clone https://github.com/mariahlins/PS-MovieTicketBookingSystem.git

2. **Navigate to the Project Directory**
    Move into the project directory:
    ```bash
    cd PS-MovieTicketBookingSystem

3. **Create and Activate a Virtual Environment**
    It's recommended to use a virtual environment to manage dependencies. Create and activate it with the following commands:
    ```bash
    pip install virtualenv
    virtualenv psenv
    source psenv/bin/activate  # On Windows use `. psenv\Scripts\activate`

4. **Install Dependencies**
    Install all the required dependencies from the requirements.txt file:
    ```bash
    pip install -r requirements.txt

5. **Apply Migrations**
    Apply the necessary migrations to set up the database:
    ```bash
    python manage.py migrate

6. **Run the Development Server**
    Start the development server:
    ```bash
    python manage.py runserver

7. **Access the application:**
    Open your browser and navigate to http://localhost:8000.
    Log in with the superuser credentials to access the admin panel or create a regular user account to start booking tickets.