# Ansible setup

This role targets an Ubuntu/Debian host with systemd. The included inventory uses
`localhost` for a local Linux/WSL environment. Run from the repository root:

```bash
cd ansible
ansible-playbook -i inventory playbook.yml --ask-become-pass
```

The playbook installs Python, copies the application, creates a virtual environment,
installs dependencies, installs/enables a systemd service, and restarts it when
the source, requirements, or service template changes.

Note: WSL distributions may not have systemd enabled by default. If `systemctl`
is unavailable, enable systemd in WSL or use a separate Ubuntu VM as the Ansible
target. Do not run this playbook against a production hospital server.
