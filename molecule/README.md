# Test Requirements

These are some notes for setting up CI testing via Jenkins.  These notes need
some work!

- This role leverages [Molecule](http://molecule.readthedocs.io/en/stable-1.25/) 
  for local and CI testing
- Automated CI/CD platform is Jenkins (see [Jenkinsfile](./Jenkinsfile))
- Jenkins is configured with an `ansible` labeled slave
  - You can change the label to another slave, but ensure the slave has the
    following:
    - `ansible` executor has a Python virtual environment with the following required
      python modules: see [molecule_pip_requirements.txt](molecule_pip_requirements.txt)
    - `ansible` executor has Docker installed and executor-user can use Docker
    - `ansible` executor has Vagrant and VirtualBox installed
    - `ansible` executor has access to Git repos (machine-level) and via Jenkins
      to `git clone` and `ansible-galaxy install` code and role dependencies
- Jenkins (server) configures a tool named `venv_ansible` to the root path of 
  the Python virtual environment containing above listed required modules
- The role author must create a symlink to the root of the role inside the 
  `molecule\default\roles` directory.  This allows the molecule test (and 
  Ansible) to find the role as it is not assumed to be installed.
- The [.gitignore](default/.gitignore) in scenario (e.g. [default](default)) directory 
  must be updated to ensure that the symlink is not ignored (e.g. 
  !roles/<name_of_role>)
- Review the [molecule.yml](default/molecule.yml) and adjust accordingly
- Rename the `no_prepare.yml` and/or `no_requirements.yml` files in the default
  scenario (and add them to other scenarios) if your test needs to prepare hosts
  or needs to download/install Ansible roles as part of the test.
- This specific test has two (2) scenarios:
  - default - tests Linux instances
  - windows - test Windows instances