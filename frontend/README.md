# Front-end application

- React application created using [Create React App](https://github.com/facebook/create-react-app).

## Requirements

- Docker needs to be installed on your machine.
- See [here](https://docs.docker.com/engine/install/) to find the download instructions that best fit your operating system.
- environment variable: 
   There are 3 .env files, local.env, dev.env and prod.env. For local development, please use local.env file which gets referenced bby Dockerfile.dev
```REACT_APP_API_URL= https://wwcode-chtools-api-dev.herokuapp.com/api```
## Steps to run the application

- In the terminal, navigate to the 'frontend' directory in the project.

- To clear all previous versions of this container:  

  - To see the created images, use:
    ```
    docker images
    ```
    If you see an image called **frontend_web**, run
    ```
    docker rmi frontend_web
    ```
    to remove that image.

  - To see the containers, use:
    ```
    docker ps -a
    ```
    If you see a container called **frontend_web**, remove it using:
    ```
    docker rm frontend_web
    ```
- To start up the project, use this command:

  ```
  docker-compose up
  ```

  This will install all the dependencies and run the application

- Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## To add features

- Create a new branch for your feature. Your branch name should follow this pattern: `FESprint<sprint_num><feature_description>` eg. FESprint5ErrorHandling
- Base branch: `master`


## Git workflow using the terminal

1. Clone the repo

- Ensure that the current branch is the **master** branch and **in the frontend directory**

2. Create a new branch for your feature

   `git checkout -b <branchname>`

3. Push your feature branch up.

   `git push --set-upstream origin <branchname>`

   **NOTE:** Use this command only the first time you are pushing the feature branch up. For the other times `git push` will suffice. Just ensure you are in the feature branch when running `git push`

4. Make changes in your feature branch only.

5. Commit changes often.

   To stage changes- `git add .`
   To commit changes- `git commit . -m "<message>"`
   
   Commit message should include `fix #<issue_number>`
   [https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)

6. When the feature is ready, push changes up.

   `git push`

7. On the repo, initiate a pull request.

8. On the Pull request screen:

- Tag leads and other team members. You will see everyone in the Reviewers section on the right.
- Leave a comment explaining the changes.
- Press the 'Create pull request' button

9. Share your pull request in FE channel for awareness. 

## Test

- When you add new component or work on new feature, please try to add test cases. 
- All tests will be run when you create a pull request as well as when you merge to master branch.

## Heroku Setup and Deployment
   1. Login to Railway
```
   railway login
```
   This will open a browser. Please use a provided credntial to login. If you don't, ask FE leaders.

   2. Associate the project with the current directory. Make sure you are running the command from frontend directory.
```
   railway link
```
   Follow the steps. FE project is <b>wwcode-chtools-fe</b>.

   3. Deploy
```
   railway up
```
   
## Heroku Setup and Deployment(Deprecated)

* Initial Setup(one time only)
```
  1. Create your Heroku account
  2. Install Heroku CLI in your computer
         $ npm install -g heroku
  3. In the terminal, navigate to the frontend directory in the WWCode-SV project
     Log in to Heroku:
         $ heroku login
  4. Log in to Container Registry:
         $ heroku container:login
  4. Create the Heroku app 
     heroku create <unique-app-name>  --buildpack mars/create-react-app
     heroku create my-heroku-react-app --buildpack mars/create-react-app 

  This will ceate new empty application on Heroku using the buildpack for create-react-app.
```
* Deployment Steps

1. Login to heroku
```
heroku login
```
2. Login to heroku container registry
```
heroku container:login
```
3. Build the image and push to Container Registry:
```
heroku container:push web -a <unique-app-name>
heroku container:push web -a my-heroku-react-app
```
* Release the image to your app:
```
heroku container:release web -a <unique-app-name>
heroku container:release web -a my-heroku-react-app
```
* Now open the app in your browser:
```
heroku open -a <unique-app-name>
heroku open -a my-heroku-react-app
```
* Check releases
```
heroku releases -a <unique-app-name>
heroku releases -a my_heroku_react_app
```
* Check logs
```
heroku logs --tail -a <unique-app-name>
heroku logs --tail -a my-heroku-react-app
```

## DockerFiles
Note:  
1. Dockerfile.dev is used by docker-compose.yml for local dev deployment
2. Dockerfile is used for production build deployment to Heroku app

## Deployment

There are 2 Heroku app, dev and prod. dev app is scheduled to get updated every merge to master. prod will be a manual update for now. We will create new branch to deploy to prod app when all the sprint features are ready. 