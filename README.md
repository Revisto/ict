# Campaign Generator

## Overview

Welcome to Campaign Generator! 🎉 Our platform allows various companies to display games, events, and campaigns as widgets on their websites. This comprehensive system is designed to provide interactive advertising solutions with a range of features to enhance user engagement and business growth.

![](https://cdn.dribbble.com/userupload/4241215/file/original-bca940d4e3854d68987c787e740f1cb8.jpg?resize=1024x768)


## Key Features

- **Discount Codes**: Generate and provide discount codes, either pre-generated or on-the-fly. 🎟️
- **User Scores**: Share user game scores with the host for future services. 🏆
- **Widgets**: Display campaigns, games, and more as widgets. 📊
- **User Profiles**: Provide dedicated user profiles to the host via web services. 👤
- **Campaign Lists**: Offer ready-made campaign lists or allow third parties (developers and companies) to create and provide custom games and campaigns. 📋
- **No Login Required**: Users can access services on the host website without needing to log in. 🚪
- **Leaderboards**: Provide leaderboards as needed by the host or tailored to the campaign. 🥇
- **Campaign Analytics**: Collect and process unique campaign data crucial for business insights. 📈
- **Public Discount Codes**: Offer discount codes from other companies for general use. 🎫
- **Admin Panel**: Provide a simple admin panel for the host (or web services if time is limited). 🛠️
- **Real-time Stats**: Deliver real-time and comprehensive statistics to the host, such as visit counts and the number of participants in a campaign. 📊
- **Scalability**: Build a scalable system to serve a large number of hosts and their users. 🌐
- **Security**: Adhere to security best practices. 🔒
- **Documentation**: Provide relevant and appropriate documentation along with the solution architecture. 📚

## Software Design

Our software design focuses on modularity and scalability, using a microservices architecture to ensure each component can be developed, deployed, and scaled independently.

### Frontend

- **Framework**: Tailwind CSS for a beautiful and responsive UI.
- **Templates**: HTML templates for rendering dynamic content.

### Backend

- **Framework**: Flask, a lightweight WSGI web application framework in Python.
- **ORM**: SQLAlchemy for ORM and Alembic for database migrations.
- **Database**: PostgreSQL for its robustness and scalability.

### APIs

- **RESTful APIs**: Used for communication between frontend and backend services.

## Endpoints

### Campaigns

- `POST /create_campaign`: Create a new campaign.
- `POST /upload_coupons/<int:campaign_id>`: Upload coupons for a campaign.
- `POST /update_webservice_url/<int:campaign_id>`: Update the web service URL for a campaign.
- `POST /delete_webservice_url/<int:campaign_id>`: Delete the web service URL for a campaign.
- `POST /select_games/<int:campaign_id>`: Select games for a campaign.
- `GET /campaigns`: List all campaigns.
- `GET /leaderboard/<int:campaign_id>`: Get the leaderboard for a campaign.

### Games

- `GET /popup/<int:campaign_id>/<int:game_id>`: Show a popup for a game.
- `GET /game/get_coupon/<int:campaign_id>`: Get a coupon for a game.
- `POST /game/add_score/<int:campaign_id>`: Add a score for a game.
- `GET /game/get_user_score/<int:campaign_id>`: Get the user score for a game.
- `POST /upload_custom_game/<int:campaign_id>`: Upload a custom game.
- `GET /game-test`: Test the game endpoint.

## Conclusion

Campaign Generator is designed to provide a comprehensive solution for companies to display games, events, and campaigns as widgets on their websites. We focus on providing high-quality interactive advertising systems with features like discount codes, user scores, widgets, user profiles, campaign lists, and more. Our system is scalable, secure, and well-documented to ensure ease of use and integration.

---

For more details, please refer to our documentation. If you have any questions, feel free to reach out to our support team. ��
