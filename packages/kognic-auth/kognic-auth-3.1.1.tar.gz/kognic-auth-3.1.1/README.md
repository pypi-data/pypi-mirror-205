# Kognic Authentication

Python 3 library providing foundations for Kognic Authentication
on top of the `requests` or `httpx` libraries.

Install with `pip install kognic-auth[requests]` or `pip install kognic-auth[httpx]` 

Builds on the standard OAuth 2.0 Client Credentials flow. There are a few ways to provide auth credentials to our api
 clients. Kognic Python clients such as in `kognic-io` accept an `auth` parameter that
  can be set explicitly or you can omit it and use environment variables. 

There are a few ways to set your credentials in `auth`. 
1. Set the environment variable `KOGNIC_CREDENTIALS` to point to your Api Credentials file. 
The credentials will contain the Client Id and Client Secret.
2. Set to the credentials file path like `auth="~/.config/kognic/credentials.json"` 
3. Set environment variables `KOGNIC_CLIENT_ID` and`KOGNIC_CLIENT_SECRET`
4. Set to credentials tuple `auth=(client_id, client_secret)` 

API clients such as the `InputApiClient` accept this `auth` parameter.

Under the hood, they commonly use the AuthSession class which is implements a `requests` session with automatic token
 refresh. An `httpx` implementation is also available. 
```python
from kognic.auth.requests.auth_session import RequestsAuthSession

sess = RequestsAuthSession()

# make call to some Kognic service with your token. Use default requests 
sess.get("https://api.app.kognic.com")
```

## Changelog

### 3.0.2 (2022-12-07)
- Support read credentials from dict

### 3.0.0 (2022-09-26)
- Rebranded from Annotell to Kognic. 
- Dropped deprecated `FaultTolerantAuthRequestSession`

### 2.0.0 (2022-05-02)
Refactor for backend separation, with optional dependencies for either `httpx` or `requests`. 

### 1.8.0 (2022-04-12)
- Initial support for httpx (BETA). Solves refresh token expiry by reset without the `FaultTolerantAuthRequestSession`  
- The library will be refactored by a breaking 2.0 release, and make the same changes to the requests version. 
The `authsession` module backed by `requests` is untouched for now.   

### 1.7.0 (2022-04-11)
- Fix compatibility issue with authlib >= 1.0.0. Resetting the auth session failed, when the refresh token had expired.   

### 1.6.0 (2021-02-21)
- Expose underlying `requests.Session` on `FaultTolerantAuthRequestSession`
- Fix some thread locks

### 1.5.0 (2020-10-20)
- Add `FaultTolerantAuthRequestSession` that handles token refresh on long running sessions. 

### 1.4.0 (2020-04-16)
- Add support for `auth` parameter, with path to credentials file or `AnnotellCredentials` object
- Drop support for legacy API token

