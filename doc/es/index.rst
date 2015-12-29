===================
Flower API (Celery)
===================

Añade un nuevo modelo para la visualización de tareas de Celery (API Flower)

http://flower.readthedocs.org/en/latest/api.html

Flower versión 0.8.3.

Recuerde de aplicar estos PR:

* Extracted search terms safely to fix /api/tasks:
  - https://github.com/mher/flower/pull/460
  - https://github.com/mher/flower/commit/79ef3fe160322781f567bbf88a3289803d1fe2e7
* Add received and started in API list tasks + Add task-id parameter in API list tasks
  - https://github.com/mher/flower/pull/505
