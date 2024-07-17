<template>
    <div class="card-holder-left card-holder">
    <div class="card-format card-appear" id="card-initial" :style="{animationDuration: '1s'}">
        <h1 class="title-card-holder-full">APG Asset Management</h1>
        <h3>2021-now</h3>
        <p>
            After completing my studies, I began my career as a DevOps Engineer at APG Asset Management.
            In this role, I support our business with data analytics tools, including Posit, R, and Python.
            My responsibilities involve consulting with our business units on developing and deploying Python, R, and Alteryx applications, as well as maintaining our infrastructure.
            This experience has significantly enhanced my technical skills and provided me with valuable insights into the operations of a large financial institution.
            I find the most satisfaction in my work when assisting our portfolio managers with their data challenges and helping them improve their technical skills.
        </p>
    </div>
    </div>

    <div class="card-holder-right card-holder">
    <div class="card-format card-appear" :style="{animationDuration: '1.5s'}">
        <h2 class="title-card-holder-full">Skills/Tools used</h2>
        <p>
           In my role at APG, I have worked with a variety of tools and technologies, some of which are:
           <ul>
               <li>Python (Streamlit/Fastapi/Poetry/Pytest)</li>
               <li>R (Shiny/testthat/tidyverse)</li>
               <li>Posit (workbench/connect)</li>
               <li>Databricks</li>
               <li>Azure Devops (Azure Pipelines/ci/cd)</li>
               <li>VUE</li>
               <li>LLMs</li>
               <li>SQL</li>
               <li>Git</li>
               <li>Ansible</li>
               <li>Linux</li>
               <li>Docker/Kubernetes</li>
               <li>Alteryx</li>
            </ul>
            I further gained relevant experience with the agile way of working and the scrum methodology.
        </p>
    </div>
    </div>

    <div class="card-holder-left card-holder">
    <div class="card-format card-appear" :style="{animationDuration: '2s'}">
        <h2 class="title-card-holder-full">Projects</h2>
        <p>
            I have worked on several projects during my time at APG, some of which are:

            <ul>
                <li>
                    <b>Initiated the development of a chatbot using the openai api.</b>
                    <p>
                        Due to our teams responsibility of maintaining several platforms we have to create/maintain/distrubte a lot of documentation.
                        This results in a lot of questions from users where to find this documentation on confluence.
                        I Initiated the development of a chatbot which utilizes the openai api for answering user questions (similar to the chat app of this website).
                        This solution was matured in collaboration with one of my colleagues, and has been the most fun project to work on at apg.
                    </p>
                </li>
                <li>
                    <b>Developed a Data interface for Bloomberg Market data.</b>
                    <p>
                        As APG was moving away from excel sheets to a more mature data platform, there was a requirment for obtaining static reference market data on an adhoc basis from the Bloomberg Data License platform.
                        I developed an API which serves our portfolio manager market data on a per request basis. Individual requests were matched against a caching database to ensure no unnecessary costs were made when requesting data.
                        The api was build in Fastapi and utilized a distributed worker system using celery for completing individual requests. All hosted on rhel8 servers on premise.
                    </p>
                </li>
                <li>
                    <b>Developed and maintained a complex ansible stack for our platforms.</b>
                    <p>
                        Our teams responsibilities grew rapidly during my years at APG asset management.  It was therefore instrumental to be in full control of all our tools and applications, and ensure predictability for the uptime of our platforms.
                        I made signifcant improvements on our Ansible stack to manage all our linux servers (20 + ) allowing our team to deploy changes to dev/acceptance and production.
                        I futher created several automated test suites which would notify our team if any service or functionality was offline for ensuring functionial continuity of our platform.
                    </p>
                </li>
                </ul>
        </p>
    </div>
    </div>


</template>
