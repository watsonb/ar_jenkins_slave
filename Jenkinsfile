#!groovy

pipeline {
    agent any

    options {
        ansiColor('xterm')
    }

    environment {
        _userName = 'jenkins'

        //tool is defined inside Jenkins server Global tools config.
        //the name below relates to a path where the tool is located
        ansible_home = tool('venv_ansible')
    }

    stages {
        stage('Startup') {
            agent {
                node {
                    label 'master'
                }
            }
            steps {
                echo "\u001B[31mStage= ${STAGE_NAME}\u001B[0m"
                echo "Pipeline defined by Jenkinsfile has been triggered: Job Name - ${env.JOB_NAME}, Build Number - ${env.BUILD_NUMBER}"
                echo " , Promoted URL - ${env.PROMOTED_URL}, Branch - ${env.BRANCH_NAME}, ID - ${env.BUILD_ID}, USR - ${_userName}"
                echo ", Node Name - ${env.NODE_NAME}, Workspace - ${env.WORKSPACE}, Jenkins URL - ${env.JENKINS_URL}"
            }
        }

        // Slack notifies slack server of pending pipeline, but only in environments with Slack environment defined.
        stage('Slack') {
            agent {
                node {
                    label 'master'
                }
            }
            steps {
                echo "\u001B[31mStage= ${STAGE_NAME}\u001B[0m"
                echo "Preparing to CI pipeline for: Job Name - ${env.JOB_NAME}"
                slackSend channel: "#chatops",
                        botUser: false,
                        failOnError: false,
                        teamDomain: "",
                        token: "${SLACK_TOKEN}",
                        baseUrl: "${SLACK_URL}",
                        message: "CI pipeline for: Job Name - ${env.JOB_NAME}, Build Number - ${env.BUILD_NUMBER}, Branch - ${env.BRANCH_NAME}, Build URL - ${env.BUILD_URL}"
            }
            when {
                allOf {
                    not {
                        environment name: 'SLACK_TOKEN', value: ''
                    }
                    not {
                        environment name: 'SLACK_URL', value: ''
                    }
                }
            }
        }

        /**
         * TODO: the 2 node labels below are hard-coded to prevent both stages
         * from running on the same slave at the same time.  Some sort of
         * resource constraint keeps the Windows test from passing when it runs
         * on the same as the Linux ones at the same time.  See the article
         * below for hints on how to do this better
         * https://stackoverflow.com/questions/50811176/jenkins-declarative-pipeline-job-how-to-distribute-parallel-steps-across-slave
        */
        stage('Molecule Test') {
            parallel {
                stage('default') {
                    agent {
                        node {
                            label 'ansible'
                        }
                    }
                    steps {
                        echo "\u001B[31mStage= ${STAGE_NAME}\u001B[0m"
                        echo 'checkout out role code'
                        checkout scm
                        sh """
                                export ANSIBLE_FORCE_COLOR=true
                                export DO_SLACK_NOTIFY=true
                                echo "activating ansible virtualenv..."
                                . ${ansible_home}/bin/activate
                                echo "executing molecule test..."
                                molecule test
                                echo "deactivating ansible virtualenv..."
                                deactivate
                            """
                    }
                    when {
                        allOf {
                            not {
                                environment name: 'VCENTER_PASSWORD', value: ''
                            }
                        }
                    }
                    post {
                        success {
                            slackSend channel: "#chatops",
                                    botUser: false,
                                    failOnError: false,
                                    teamDomain: "",
                                    token: "${SLACK_TOKEN}",
                                    baseUrl: "${SLACK_URL}",
                                    message: "Role passed: Job Name - ${env.JOB_NAME}, Build Number - ${env.BUILD_NUMBER}, Branch - ${env.BRANCH_NAME}, Build URL - ${env.BUILD_URL}"
                        }
                        failure {
                            slackSend channel: "#chatops",
                                    botUser: false,
                                    failOnError: false,
                                    teamDomain: "",
                                    token: "${SLACK_TOKEN}",
                                    baseUrl: "${SLACK_URL}",
                                    message: "Role failed: Job Name - ${env.JOB_NAME}, Build Number - ${env.BUILD_NUMBER}, Branch - ${env.BRANCH_NAME}, Build URL - ${env.BUILD_URL}"
                        }
                        always {
                            junit 'molecule/reports/**/*.xml'
                        }
                    }
                } // end default stage
                stage('windows') {
                    agent {
                        node {
                            label 'vagrant'
                        }
                    }
                    steps {
                        echo "\u001B[31mStage= ${STAGE_NAME}\u001B[0m"
                        lock(resource: 'ansible_vagrant_vbox') {
                            sh """
                                echo "[pre-test] powering down any running Virtual Box VMs..."
                                VBoxManage list runningvms | awk '{print \$2;}' | xargs -I vmid VBoxManage controlvm vmid poweroff
                                echo "[pre-test] deleting all Virtual Box VMs..."
                                VBoxManage list vms | awk '{print \$2;}' | xargs -I vmid VBoxManage unregistervm --delete vmid
                                """

                            echo 'checkout out role code'
                            checkout scm
                            sh """
                                    export ANSIBLE_FORCE_COLOR=true
                                    export DO_SLACK_NOTIFY=true
                                    echo "activating ansible virtualenv..."
                                    . ${ansible_home}/bin/activate
                                    echo "executing molecule test..."
                                    molecule test --scenario-name windows
                                    echo "deactivating ansible virtualenv..."
                                    deactivate
                                """

                            sh """
                                echo "[post test] powering down any running Virtual Box VMs..."
                                VBoxManage list runningvms | awk '{print \$2;}' | xargs -I vmid VBoxManage controlvm vmid poweroff
                                echo "[post test] deleting all Virtual Box VMs..."
                                VBoxManage list vms | awk '{print \$2;}' | xargs -I vmid VBoxManage unregistervm --delete vmid
                                """
                        } //end lock
                    }
                    post {
                        success {
                            slackSend channel: "#chatops",
                                    botUser: false,
                                    failOnError: false,
                                    teamDomain: "",
                                    token: "${SLACK_TOKEN}",
                                    baseUrl: "${SLACK_URL}",
                                    message: "Role passed: Job Name - ${env.JOB_NAME}, Build Number - ${env.BUILD_NUMBER}, Branch - ${env.BRANCH_NAME}, Build URL - ${env.BUILD_URL}"
                        }
                        failure {
                            slackSend channel: "#chatops",
                                    botUser: false,
                                    failOnError: false,
                                    teamDomain: "",
                                    token: "${SLACK_TOKEN}",
                                    baseUrl: "${SLACK_URL}",
                                    message: "Role failed: Job Name - ${env.JOB_NAME}, Build Number - ${env.BUILD_NUMBER}, Branch - ${env.BRANCH_NAME}, Build URL - ${env.BUILD_URL}"
                        }
                        always {
                            junit 'molecule/reports/**/*.xml'
                        }
                    }
                } // end windows stage
            }
        }
    }
}