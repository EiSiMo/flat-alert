# Flat Alert

## Description

Finding an apartment in Berlin is notoriously difficult. However, those with a WBS (housing entitlement certificate) can access state-subsidized housing via inberlinwohnen.de. New listings appear daily, but there is no waiting list; applicants are selected at random. Crucially, the number of applications per listing is capped, often causing ads to disappear within an hour. This necessitates constant monitoring of the website.

Flat Alert solves this problem by automating the search process. This Telegram bot scans for new listings every minute, 24/7, and sends instant notifications. It supports customizable filters for size, price, location, and public transport connectivity.

## Features

*   **Real-time Monitoring:** Scans inberlinwohnen.de every minute.
*   **Instant Notifications:** Receive alerts via Telegram immediately when a flat becomes available.
*   **Advanced Filtering:** Filter by size, price, region, and more.
*   **Commute Analysis:** Uses the Google Maps API to calculate public transport connections to important hubs.

## Technology Stack

*   **Containerization:** Docker for easy deployment and cross-platform compatibility.
*   **Scraping:** Playwright for reliable website interaction.
*   **Geolocation:** Google Maps API for transport connectivity analysis.
*   **Messaging:** Telegram Bot API for user interaction.

## Requirements

To run this project, you will need:

*   An account on inberlinwohnen.de
*   A Telegram Bot Token
*   A Google Maps API Key
*   Docker installed on the host machine

## Project Status

This project is currently in early development and primarily designed for personal use. Customizing filters currently requires technical knowledge, but user-friendly configuration options are planned for future updates. Contributions are welcome.

## Quickstart

Follow these steps to run the program on your machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/eisimo/flat-alert.git
    ```
    ```bash
    cd flat-alert
    ```

2.  **Configure the environment:**
    Create a `.env` file in the root directory. Refer to `.env.example` for the required variables.

3.  **Run the application:**
    ```bash
    docker compose up -d
    ```

## Related Projects

*   [flat-apply](https://github.com/EiSiMo/flat-apply): A tool currently in development to automate the application process for flats found by Flat Alert.
