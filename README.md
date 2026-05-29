# BlogIt

Simple blogger application. Inspiration: Reddit. Main goal is to gain experience working with the Flask framework.

## Deployed with Heroku
https://protected-earth-03499.herokuapp.com/

## Introduction
This application is my first attempt using the Flask web framework. I made it a goal to use as many Flask modules as I could in order to learn all that Flask has to offer.

Some flask specific modules I used are as follows:
- flask_migrate: database migrations
- flask_bcrypt: password hashing
- flask_login: authorization/authentication
- flask_sqlalchemy: database ORM
- flask_wtf: form creation and validation

I also focused on implementing common Flask design patterns including an application factory, blueprints for modularity, template inheritance, message flashing, and a login decorator.

## Getting Started
  Clone the REPO:

`` git clone git@github.com:Stoovles/BlogIt.git ``

  Install requirements w/ pip:
  
`` pip install -r requirements.txt ``

  Spin up the server locally:
  
`` python run_dev.py ``

## Testing
Cursory testing with unittest. Refer to issues.

Run this in your command line:

``python -m unittest discover tests``

## Added Feature: Comments REST API
This fork adds a dedicated comments REST API for the BlogIt application. The new API provides full CRUD support for comments tied to blog posts.

### API routes
- `POST /api/posts/<post_id>/comments` - create a comment for a post (created as hardcoded user id 3)
- `GET /api/posts/<post_id>/comments` - list comments for a post
- `GET /api/comments/<comment_id>` - read a single comment
- `PUT /api/comments/<comment_id>` - update a comment
- `DELETE /api/comments/<comment_id>` - delete a comment
- `GET /api/openapi.json` - retrieve the OpenAPI specification

### Request format
All API requests and responses use JSON.

Example create request:
```json
{
  "content": "Great post!"
}
```

Comments are created using a hardcoded "rest_api" user account with `user_id=3`.

### Status codes
- `200` - OK for successful reads, updates, and deletes
- `201` - Created for successful comment creation
- `400` - Bad request for invalid JSON or missing fields
- `404` - Not found for missing post, user, or comment

### OpenAPI documentation
The OpenAPI spec is available at:
- `http://localhost:5000/api/openapi.json`

## Testing for Comments REST API
The new comments API tests use unittest and cover positive and negative CRUD behavior.

Run the test file:

```bash
python -m unittest tests.test_api
```

## Additional Changes
Some files/codes are edited to make the original old program be able to install and run on modern devices.

Also some small changes to avoid depreciation warnings, specifically on testing.


