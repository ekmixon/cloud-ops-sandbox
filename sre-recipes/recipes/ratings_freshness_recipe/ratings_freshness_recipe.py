#
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""
This module contains the implementation of rating2 recipe
"""

import logging
import subprocess
from recipe import Recipe


class RatingsFreshnessRecipe(Recipe):
    """
    This class implements 'rating2' which purposefully
    stops recollect API calls to rating service.
    """

    name = "recipe2"

    def get_name(self):
        return self.name

    def is_active(self):
        return True

    def break_service(self):
        """
        Pause Cloud scheduler job to stop calls to recollect API of
        the rating service
        """
        logging.info("Pausing scheduled job of the rating service")
        print("Breaking service operations...")
        project_id = Recipe._get_project_id()
        if not project_id:
            print("Failed: cannot find project id.")
            logging.error("Failed pausing scheduled job: no project id.")
            exit(1)
        pause_command = "gcloud scheduler jobs pause ratingservice-recollect-job --project {pid}".format(
            pid=project_id
        )
        _, err_str = Recipe._run_command(pause_command)
        if "ERROR:" in str(err_str, "utf-8"):
            print(err_str)
            logging.error(f"Failed executing service breaking command:{err_str}")
        else:
            print("...done")
            logging.info("Scheduled job of the rating service paused")

    def restore_service(self):
        """
        Resume Cloud scheduler job to restore calls to recollect API of
        the rating service
        """
        logging.info("Resuming scheduled job of the rating service")
        print("Restoring broken operations...")
        project_id = Recipe._get_project_id()
        if not project_id:
            print("Failed: cannot find project id.")
            logging.error("Failed pausing scheduled job: no project id.")
            exit(1)
        resume_command = "gcloud scheduler jobs resume ratingservice-recollect-job --project {pid}".format(
            pid=project_id
        )
        _, err_str = Recipe._run_command(resume_command)
        if "ERROR:" in str(err_str, "utf-8"):
            print(err_str)
            logging.error(f"Failed executing service restoring command:{err_str}")
        else:
            print("...done")
            logging.info("Scheduled job of the rating service resumed")

    def hint(self):
        """
        Provides a hint about the root cause of the issue
        """
        project_id = Recipe._get_project_id()
        print(
            "\n".join(
                (
                    'Product ratings are managed by the "rating service", hosted on Google AppEngine.',
                    "The service provides APIs that allow other services to get and update products' ratings.",
                    "The rating data is kept up-to-date by periodically calling an API endpoint that collects",
                    "all recently sent new rating scores for each product and calculates the new rating",
                    "based on the old value and the new scores. Try to check if the rating service operates normally.",
                )
            )
        )

    def verify_broken_service(self):
        """
        Displays a multiple choice quiz to the user about which service
        broke and prompts the user for an answer
        """
        prompt = "Which service has a breakage?"
        choices = [
            "email service",
            "frontend service",
            "ad service",
            "rating service",
            "recommendation service",
            "currency service",
        ]
        answer = "rating service"
        Recipe._generate_multiple_choice(prompt, choices, answer)

    def verify_broken_cause(self):
        """
        Displays a multiple choice quiz to the user about the cause of
        the breakage and prompts the user for an answer
        """
        prompt = "What is the cause of the break?"
        choices = [
            "rating service does not run",
            "rating votes data is missing in the database",
            "scheduler job that sends recollect request to rating service does not work",
            "new ratings are calculated incorrectly",
        ]
        answer = (
            "scheduler job that sends recollect request to rating service does not work"
        )
        Recipe._generate_multiple_choice(prompt, choices, answer)

    def verify(self):
        """Verifies the user found the root cause of the broken service"""
        print(
            """
        This is a multiple choice quiz to verify that 
        you have found the root cause of the break.
        """
        )
        self.verify_broken_service()
        self.verify_broken_cause()
