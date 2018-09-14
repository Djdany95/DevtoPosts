# APIDevto

Simple API made with Flask to get posts from Dev.to passing an username as parameter.

### Endpoints
- /getallposts/*user*: Get all posts of this user, is very slow, uses selenium with chromedriver.
- /getlastposts/*user*: Get 5 lasts post of this user, is quick enough.
- /cheklastpost/*user*: Return the name of last post of the user, instant.
- /getntotalposts/*user*: Return the total number of posts of the user, instant.

## TODOs
- [ ] Test in Linux and MacOS.