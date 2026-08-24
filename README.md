<img width="150" src="https://user-images.githubusercontent.com/48166553/200232307-f539464b-522e-4771-8f1b-8ad5e430e918.png" />

Samaaja is an open source software solution for rapidly building location based
civic services connected with volunteer, human interactions. It comes with all
necessary UI and management features and can be easily extended into web
applications and external mobile apps and systems via built-in APIs.

Visit [Samaaja.org](https://samaaja.org/)

---

### What is in this repository

A single Frappe app that contains both halves of Samaaja:

| Directory | Contents |
|---|---|
| `samaaja/` | the Frappe app — doctypes, API, background jobs, setup |
| `frontend/` | the Vue 3 application users see |

The Vue app is built as part of `bench build` and served by the Frappe site
itself, so there is one repository, one build and one deployment.

| Address | Serves |
|---|---|
| `/` | the Vue application |
| `/desk` | the Frappe admin interface |
| `/api/*` | the Frappe API, same-origin — no CORS configuration required |

For how this is put together and why, see
[Monorepo migration: Vue frontend into the Frappe app](https://wiki.impactyaan.com/doc/monorepo-migration-vue-frontend-into-the-frappe-app-KZEtQWLvWz).

---

### Requirements

| | |
|---|---|
| Frappe | `version-16` |
| Energy Points | [`frappe/eps`](https://github.com/frappe/eps), branch `version-16` |
| Python | 3.11 or newer |
| Node | 20 or newer |
| MariaDB | 10.6 or newer |

Energy Points was removed from Frappe core in v16. Samaaja adds custom fields to
its doctypes, so `eps` must be present in the bench before Samaaja is installed.

---

### Installation

* [**Install Bench & Frappe**](https://github.com/frappe/bench#installation), on
  the `version-16` branch

* Fetch the Energy Points app first

      bench get-app eps https://github.com/frappe/eps.git --branch version-16

* Download the Samaaja app

      bench get-app https://github.com/Impactyaan-Solutions/Samaaja

* Install both on your site

      bench --site <your-site-name-here> install-app eps
      bench --site <your-site-name-here> install-app samaaja

* Build the frontend

      bench build --app samaaja

**Redis must be running before `install-app`.** Installation queues a background
job, and Frappe's queues are started by `bench start`. On a bench that has never
been started, start Redis first.

---

### Development

Rebuild after changing anything under `frontend/`:

    bench build --app samaaja

Clear the cache after changing routes, hooks or Python:

    bench --site <your-site-name-here> clear-cache

Check that no Vue route collides with an address Frappe serves:

    bench --site <your-site-name-here> execute samaaja.utils.route_check.check_conflicts

The frontend's own dev server is available for rapid UI work. It proxies API
calls to a running bench, configured through `VITE_DEV_PROXY_TARGET` — see
`frontend/.env.example`.

    cd frontend && npm run dev

---

#### License

MIT
