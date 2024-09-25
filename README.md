# Anime Precision Recommendation System

## Introduction

The **Anime Precision Recommendation System** is an intelligent recommendation system based on user behavior and anime characteristics. It aims to provide personalized anime recommendations to users. The system includes multiple modules such as recall, ranking, and similarity-based recommendations, which leverage the user's historical behavior and preferences to recommend anime content that the user may be interested in.

## Features

- **Recall Service**: Recall a batch of potentially interesting anime based on the user's past behavior.
- **Ranking Service**: Rank the recalled anime to prioritize those the user is most likely to enjoy.
- **Similar Recommendation**: Recommend other anime similar to the ones the user likes.
- **Comprehensive Recommendation**: Combine recall, ranking, and similarity recommendations to provide the final recommendation list.
- **Anime Details**: Provide detailed information about an anime, including genres, number of episodes, ratings, etc.
- **User Behavior Data**: Record user click and view behavior to continuously optimize the recommendation algorithm.

## Technology Stack

The project uses the following technologies and tools:

### Backend
- **Python Flask**: Flask is used as the backend framework to handle API requests and manage business logic.
- **Pandas**: For efficient data analysis and manipulation of user behavior and anime characteristics.
- **Spark & Flink**: To perform distributed data processing and real-time stream processing for large-scale datasets.
- **Kafka**: Kafka is used as a message broker to handle real-time data pipelines, ensuring high availability and scalability.
- **Cassandra**: A NoSQL database used to store and retrieve large volumes of user interaction data with high availability.

### Frontend
- **Vue.js**: Vue is the framework used for the frontend, providing a responsive and interactive user interface to display anime recommendations to users.

### Machine Learning & AI
- **TensorFlow**: TensorFlow is used to build and train machine learning models that analyze user behavior and predict anime preferences for personalized recommendations.

## API Endpoints

### 1. Recall Service

**GET Recall "You May Like" Results**

**Endpoint**: `GET /recall/{user_id}`

**Request Parameters**:

- `user_id` (path, integer, required): The ID of the user requesting recommendation service.

**Response**:

- **Status Code**: 200, indicating the request was successful.
- **Response Body**: An array of recalled anime IDs.

### 2. Ranking Service

**GET Ranked "You May Like" Results**

**Endpoint**: `GET /rank/{user_id}`

**Request Parameters**:

- `user_id` (path, integer, required): The ID of the user requesting ranking service.

**Response**:

- **Status Code**: 200, indicating the request was successful.
- **Response Body**: An array of ranked anime IDs.

### 3. Similar Recommendation

**GET Similar Anime Recommendations**

**Endpoint**: `GET /sim/{anime_id}`

**Request Parameters**:

- `anime_id` (path, integer, required): The anime ID for which to find similar anime.

**Response**:

- **Status Code**: 200, indicating the request was successful.
- **Response Body**: An array containing detailed information of similar anime.

### 4. Comprehensive Recommendation

**GET Comprehensive "You May Like" Recommendations**

**Endpoint**: `GET /recommends/{user_id}`

**Request Parameters**:

- `user_id` (path, integer, required): The ID of the user requesting comprehensive recommendation.

**Response**:

- **Status Code**: 200, indicating the request was successful.
- **Response Body**: An array containing detailed information of recommended anime.

### 5. Anime Details

**GET Anime Details**

**Endpoint**: `GET /anime/{anime_id}`

**Request Parameters**:

- `anime_id` (path, integer, required): The ID of the anime for which to fetch details.

**Response**:

- **Status Code**: 200, indicating the request was successful.
- **Response Body**: An object containing detailed information about the anime.

### 6. User Behavior Data

#### Record Click Event

**POST Record Click Event**

**Endpoint**: `POST /clicks`

**Request Parameters**:

- `user_id` (body, string, required): The ID of the user who clicked on an anime.
- `anime_id` (body, string, required): The ID of the clicked anime.

**Response**:

- **Status Code**: 200, indicating the request was successful.

#### Record View Event

**POST Record View Event**

**Endpoint**: `POST /views`

**Request Parameters**:

- `user_id` (body, string, required): The ID of the user who viewed an anime.
- `anime_id` (body, string, required): The ID of the viewed anime.

**Response**:

- **Status Code**: 200, indicating the request was successful.

