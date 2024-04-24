# Contributing

## Contribute

- [Fork the repository](https://github.com/trfore/ansible-smallstep/fork) on github and clone it.
- Create a new branch and add your code.
- Write test that cover the changes and expected outcome.
- Test your changes locally using `tox`.
- Push the changes to your fork and submit a pull-request on github.

```sh
git clone https://github.com/USERNAME/ansible-smallstep && cd ansible-smallstep
git checkout -b MY_BRANCH
# add code and test
tox run-parallel
git push -u origin MY_BRANCH
gh pr create --title 'feature: add ...'
```

### Setup a Dev Environment

```sh
cd ansible-smallstep
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements/dev-requirements.txt
pre-commit install
```

### Tox: Test Suite

- A local installation of [Docker](https://docs.docker.com/engine/installation/) is required to run the `molecule` test scenarios.
- All `tox` environments are created within the project directory under `.tox`.
- The collection is tested using the last three versions of `ansible-core` on a Ubuntu image. Additionally, the collection is tested using the latest `ansible-core` on CentOS and Debian.
  - NOTE: Some molecule scenarios, `multiple_certs` and `step_ssh`, will generate a docker bridge network for each `tox` environment using the next available subnet, e.g. `172.18.0.0/16`. The default docker network is `172.17.0.0/16`.
- Extensive code modifications that change how a playbook is written need to be accompanied by test, e.g. molecule scenario, that covers the changes. This will help avoid end-user frustration with faulty code examples in the documentation.
  - Follow best practices for creating playbooks and handling variables within `playbooks/`, but avoid encrypting files. This will keep encrypted files out of the collection build and avoid issues with [`ansible-lint` #2889](https://github.com/ansible/ansible-lint/issues/2889).

```sh
cd ansible-smallstep
# list environments and test
tox list
# lint all files
tox -e lint run
# run a specific test environment
tox -e py-ansible2.16-default run
# run a group of tests, e.g. the default molecule scenario
tox -f default run
# run all test in parallel
tox run-parallel
```

- You can also pass environment variables to tox for: `MOLECULE_IMAGE`, `STEP_CA_VERSION`, and `STEP_CLI_VERSION`. When running multiple test, we highly recommend using `STEP_*_VERSION` variables to avoid hitting GitHub's API rate limiter.

```sh
MOLECULE_IMAGE='trfore/docker-debian12-systemd' tox -e py-ansible2.16-default run
STEP_CA_VERSION='0.26.0' STEP_CLI_VERSION='0.26.0' tox -e py-ansible2.16-default run
# highly recommended
STEP_CA_VERSION='0.26.0' STEP_CLI_VERSION='0.26.0' tox run-parallel
```

- For iterative development and testing, the tox molecule environments are written to accept `molecule` arguments. This allows for codebase changes to be tested as you write across multiple distros and versions of `ansible-core`.

```sh
# molecule converge
tox -e py-ansible2.16-default run -- converge -s default
# molecule test w/o destroying the container
tox -e py-ansible2.16-default run -- test -s default --destroy=never

# exec into the container via tox
tox -e py-ansible2.16-default run -- login -s default
# exec into the container
docker exec -it py-ansible2.16-default bash

# parallel testing
tox -f default run-parallel -- test -s default --destroy=never
# remove all containers
tox -f default run-parallel -- destroy -s default
```

### Tox: Docsite Preview

- If you are making changes to the docsite, `docs/`, or adding variables, e.g. `argument_specs.yml`, you can build the docsite locally and preview the changes.

```sh
cd ansible-smallstep
# build site using tox
tox -e docs
# preview the docsite
python3 -c 'import webbrowser; webbrowser.open_new(".tox/docs/tmp/build/html/index.html")'
```

### Documentation

- New features or extensive code changes need to be accompanied by documentation in a `argument_specs.yml` and README. This information can be redundant, yet it is often helpful to start with the argument_specs then copy it to a README.
- Adding a scenario guide, `docs/docsite/rst/guide_*.rst`, to the documentation is also nice for features with many arguments or different configurations.

### Pull Request

- All pull request are run through a more extensive test suite that will validate the collection on multiple OSs and releases, yet local `pre-commit` and `tox` test should provide a good proxy for the github tests.

## Additional References

- [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html)
- [Github Docs: Forking a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#forking-a-repository)
- [Ansible Docs: `ansible-core` support matrix](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix)
