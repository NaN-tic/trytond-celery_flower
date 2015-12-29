Flower API (Celery) Module
##########################

The Flower API (Celery) module add new model to view Celery Tasks

http://flower.readthedocs.org/en/latest/api.html

Flower version 0.8.3.

Remember to patch with those PR:

* Extracted search terms safely to fix /api/tasks:
  - https://github.com/mher/flower/pull/460
  - https://github.com/mher/flower/commit/79ef3fe160322781f567bbf88a3289803d1fe2e7
* Add received and started in API list tasks + Add task-id parameter in API list tasks
  - https://github.com/mher/flower/pull/505
