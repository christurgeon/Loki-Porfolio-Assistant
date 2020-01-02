# Git Overview

## GitFlow

For contributing to this project, we will utilize GitFlow as our method for version control. We have a branch off of ```master``` called ```develop```. All of our features that we work on are contained in their own separate branches that stem off of ```develop```. When you finish working on your feature branch, you will merge the changes into ```develop```. Then, once ```develop``` is working properly, develop will be merged into ```master``` by an admin. By utilizing GitFlow, we will ensure that we always have a working version of the code base (master).

## Step by Step Guide

1. Clone the repository: ```git clone <repo-link>```
2. Switch to the ```develop``` branch: ```git branch develop```
3. Create your feature branch off of ```develop```: ```git checkout -b <my-feature-branch-name> develop```
4. When you're finished with your feature and ready to merge into develop, switch into develop and then merge: ```git checkout develop``` then ```git merge <my-feature-branch-name>```

* We will never push changes or merge directly into master!