# Overview

This document outlines how you can update, test and release the Wagtail ReoAko module.

The repository comes with a provisioning setup that allows you to spin up a Wagtail environment and see ReoAko in action as you build.

# Building the test environment

1. Spin up the virtual machine

        vagrant up

2. Create yourself a superuser

        ./manage.sh createsuperuser

3. Build the test front end

        nvm use
        npm install
        npm run build:testfrontend

    This will give you a CMS previewable implemetation of https://www.npmjs.com/package/@octavenz/reoako

4. Run the site

      ./run.sh

   The site will be visible at localhost:8000/admin

Once logged in you can edit the "HomePage" and add ReoAko words to the "content" field.

# Switching between Wagtail and Django Versions

There is a helper that will allow you to easily switch between Wagtail and Django versions. This script will update the
virtual environment packages, recreate the database, and spit you out into creating a superuser. Examples:

      ./change_versions.sh -w "~2.16" -d "~3.2"  # -w == Wagtail version -d == Django version

   or 

      ./change_versions.sh -w "~3" -d "~4.2"  # -w == Wagtail version -d == Django version

   etc etc...

Beware that running this command will update the pyproject.toml and poetry.lock files with the updated versions so if you then commit those files the next developer will be spinning up whatever version you've committed.

# Changing the core ReoAko codebase

The core ReoAko code is located in the "wagtail_reoako" directory. Anything you change in here will eventually be packaged up and released on PyPI

This code is included as the "wagtail_reoako" app in the "build_test" test application so if you have that running you will see the changes happening in real time.

The front end for this application can be built and watched by doing the following

      nvm use
      npm install
      npm run watch


