# REST Checker
##### Simple API Automation framework 
#

### Definition 
Build a lightweight automation framework that can be used to write API Automation test cases fast and assert them easily. 

### Directory & File structure 
There should be one directory that should contain all the endpoints in the form of `.json` as described below. 
```
├── src
│   ├── endpoints               → directory which contains all the endpoints  
|   │   ├── getUsers.json       → Request json file to get all the users endpoint 
|   │   ├── getSingleUser.json  → Request json file to get a single user endpoint 
|   |   └── createUser.json     → Request json file to create a  new user 
```
Example endpoints json files are attached under the `endpoints/` directory.  

### Functional Acceptance Criteria 
- Framework should be able to test all the endpoint one by one under the `endpoints/*` directory 
- Every assertions mentioned in `endpoints/**.json` file should be asserted

### Technical Acceptance Criteria 
- Framework should be able to generate request **dynamically** based on the configuration mentioned under `endpoints/**.json` file >> `request` key 
- If a new configuration file is added under `endpoints/*` framework should automatically run the assertions as per mentioned in the configuration without writing an additional line of code 
- You can use [reqres](https://reqres.in/) - to build and test this framework. Other API platforms are also acceptable

### Coding standards 
- You can use whatever directory/file structure you want, but there should be an `endpoints/` directory where we can post new endpoint 
- Every line of code should be clean, well-commented, and self-explanatory. Code has to be scalable & maintainable in the long run. 

### Submission 
- All the code has to be submitted via the public GitHub repository 
- Sumitted code should contains simple instructions about how to setup the project & how to run the test cases easily 
- Code needs to be sumitted withing conveyed timeline 

### Explaiiner Video
[![Explainer Video](https://i.postimg.cc/tCwgpC06/Screenshot-2022-12-02-at-2-26-36-PM.png)](https://app.usebubbles.com/fqp2dvoRvsJV6CHbLEJdWB/rest-checker-practical-test-explainer)
